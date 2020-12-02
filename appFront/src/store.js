import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLogin: window.sessionStorage.getItem('isLogin'),
    token: window.sessionStorage.getItem('token'),
    role: window.sessionStorage.getItem('role'),
    user: window.sessionStorage.getItem('user')
  },
  mutations: {
    setIsLogin(state, data) {
      state.isLogin = data;
      window.sessionStorage.setItem('isLogin', data)
    },
    setToken(state, data) {
      state.token = data;
      window.sessionStorage.setItem('token', data)
    },
    setRole(state, data) {
      state.role = data;
      window.sessionStorage.setItem('role', data)
    },
    setUser(state, data) {
      state.user = data;
      window.sessionStorage.setItem('user', data)
    }
  },
  actions: {

  }
})
