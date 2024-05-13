/*!

=========================================================
* Vue Argon Design System - v1.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-design-system
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-design-system/blob/master/LICENSE.md)

* Coded by www.creative-tim.com

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import Argon from "./plugins/argon-kit";
import "./registerServiceWorker";
// import store from './store';
import Modal from "./components/Modal.vue";
import 'core-js/stable';
import 'regenerator-runtime/runtime';

import VueAxios from "vue-axios";
import axios from "axios";

Vue.prototype.$axios = axios;

Vue.use(VueAxios, axios);


Vue.prototype.$axios = axios;
Vue.use(VueAxios, axios)

//Configuración global
export const backendUrl = "http://localhost:8000/";

Vue.component("modal", Modal);

Vue.config.productionTip = false;
Vue.use(Argon);

new Vue({
  router,
  // store,
  render: (h) => h(App),
}).$mount("#app");
