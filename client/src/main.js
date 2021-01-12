import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import CoreuiVue from '@coreui/vue';

Vue.use(CoreuiVue);

Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')
