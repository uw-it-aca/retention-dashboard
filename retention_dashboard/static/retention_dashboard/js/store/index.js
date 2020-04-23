import Vue from 'vue';
import Vuex from 'vuex';
import dataselect from './modules/dataselect';
import filters from './modules/filters';

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
    dataselect,
    filters
  },
});
