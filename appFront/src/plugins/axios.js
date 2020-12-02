"use strict";

import Vue from 'vue';
import axios from "axios";
import Router from '@/router';
import store from '@/store'
import  { getCookie }  from '@/plugins/components.js';

// Full config:  https://github.com/axios/axios#request-config
// axios.defaults.baseURL = process.env.baseURL || process.env.apiUrl || '';
// axios.defaults.headers.common['Authorization'] = AUTH_TOKEN;
// axios.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
//axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';
//axios.defaults.withCredentials = true;

let config = {
  //baseURL: process.env.baseURL || process.env.apiUrl || ""
  //timeout: 5 * 1000, // Timeout
  //headers: {'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'},
  withCredentials: true // Check cross-site Access-Control
};

const _axios = axios.create(config);
_axios.defaults.headers.post['Content-Type'] = 'multipart/form-data';
_axios.interceptors.request.use(
  function(config) {
    // Do something before request is sent
    config.headers['X-CSRFToken'] = getCookie('csrftoken');
    return config;
  },
  function(error) {
    // Do something with request error
    return Promise.reject(error);
  }
);

const errorCode = [{
  'name': 400,
  'message': '错误请求'
},{
  'name': 404,
  'message': '未找到'
},{
  'name': 408,
  'message': '请求超时'
}];

// Add a response interceptor
_axios.interceptors.response.use(
  function(response) {
    // Do something with response data
    const hide_message = response.config.headers['Hide-Message'];
    if(hide_message != true){
      switch (response.config.method) {
        case 'post':
          console.log(response.data);
          if(response.data.code == 301){
            Vue.prototype.$message({message: '开始录音！', type: 'success'});
            break;
          }else if(response.data.code == 302){
            Vue.prototype.$message({message: '停止录音！', type: 'success'});
            break;
          }else{
            Vue.prototype.$message({message: '创建成功！', type: 'success'});
            break;
          }
        case 'put':
          Vue.prototype.$message({message: '修改成功！', type: 'success'});
          break;
        case 'delete':
          Vue.prototype.$message({message: '删除成功！', type: 'success'});
          break;
      }
    }
    return response;
  },
  function(error) {
    if(error.response){
      // Do something with response error
      if(error.response.status == 401 || error.response.status == 403){
        if(store.state.isLogin) {
          store.commit('setIsLogin', false);
          Vue.prototype.$alert('登录信息超时，请重新登录', '登录超时', {
            confirmButtonText: '跳转至登录页面',
            callback: () => {
              Router.push({path: '/login'})
            }
          })
        }
      }else{
        let message = '请求错误';
        errorCode.forEach(e => {
          if(e.name == error.response.status) message = e.message;
        });
        Vue.prototype.$message({
          type: 'error',
          message: message + '！',
          duration: 2000
        })
      }
    }
    return Promise.reject(error);
  }
);

Plugin.install = function(Vue) { //Vue, options
  Vue.axios = _axios;
  window.axios = _axios;
  Object.defineProperties(Vue.prototype, {
    axios: {
      get() {
        return _axios;
      }
    },
    $axios: {
      get() {
        return _axios;
      }
    },
  });
};

Vue.use(Plugin)

export default Plugin;
