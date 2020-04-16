import Vue from 'vue';
import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue';
import VueRouter from 'vue-router';
import VueAnalytics from 'vue-analytics';
import VuePluralize from 'vue-pluralize';
import VueMoment from 'vue-moment';
import moment from 'moment-timezone';
import underscore from 'vue-underscore';
import store from './store';
import App from "./App.vue";
import DataView from "./components/DataView.vue";
import VueClipboard from 'vue-clipboard2';
import VuePapaParse from 'vue-papa-parse'


// import the bootstrap / bootstrap-vue base css
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

//TODO: Replace with real key, vue analytics requires *a* key!
//const gaCode = $("body").data("google-analytics");
const gaCode = "UA-12345-6";
const debugMode = $("body").data("django-debug");

Vue.use(VueRouter);
Vue.use(BootstrapVue);
Vue.use(BootstrapVueIcons);
Vue.use(VuePluralize);
Vue.use(VueMoment, {moment});
Vue.use(underscore);
Vue.use(VueClipboard);
Vue.use(VuePapaParse);


export const EventBus = new Vue();

var router = new VueRouter({
  mode: "history",
  routes: [
    { path: '/', component: DataView },
  ]
});


Vue.use(VueAnalytics, {
  id: gaCode,
  router,
  set: [
    { field: 'anonymizeIp', value: true }
  ],
  debug: {
    // enabled: false
    enabled: debugMode
  }
});

// vue app will be rendered inside of #main div found in index.html using webpack_loader
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#main");
