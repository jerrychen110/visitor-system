import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueQriously from 'vue-qriously'
import './plugins/axios'
import './plugins/element.js'

Vue.use(VueQriously)
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
