import Vue from 'vue'
import Router from 'vue-router'
import store from '@/store'

import mgtRouter from './views/mgt/router'
import NotFoundPage from './components/NotFoundPage.vue'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    { 
      path: '*',
      component: NotFoundPage
    },
    {
      path: '/',
      name: 'Home',
      component: () => import('./views/Home.vue')
    },
    {
      path: '/index/apps',
      name: 'Apps',
      component: () => import('./views/index/apps/List.vue'),
      meta:{
        title: '更多应用'
      }
    },
    {
      path: '/apiTest',
      name: 'ApiTest',
      component: () => import('./views/ApiTest.vue'),
      meta:{
        title: '接口测试'
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('./views/Login.vue')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('./views/Register.vue')
    },
    {
      path: '/patientinfo',
      name: 'PatientInfo',
      component: () => import('./views/PatientInfo.vue')
    },
    mgtRouter
  ]
})

router.beforeEach((to, from, next) => {
  let stateRole = true;
  const role = store.state.role;
  const toMatched = to.matched;
  toMatched.forEach(e => {
    if(JSON.stringify(e.meta)!=="{}" && e.meta.role){
      stateRole = false;
      const roleArr = e.meta.role;
      roleArr.forEach(ee => {
        if (role == ee) stateRole = true
      })
    }
  });
  if(store.state.isLogin || to.name == 'Login' || to.name == 'Register'){
    if(stateRole){
      next()
    }else{
      Vue.prototype.$alert('该用户没有权限，预览此页面！', '没有权限', {
        callback: () => {
          router.push({path: '/'})
        }
      })
    }
  }else{
    Vue.prototype.$alert('请登录后预览该页面！', '未登录', {
      confirmButtonText: '跳转至登录页面',
      callback: () => {
        router.push({path: '/login'})
      }
    })
  }
})

export default router
