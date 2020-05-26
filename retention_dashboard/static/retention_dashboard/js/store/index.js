import Vue from 'vue';
import Vuex from 'vuex';
import dataselect from './modules/dataselect';
import filters from './modules/filters';
import advisors from './modules/advisors';

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
    dataselect,
    filters,
    advisors
  },
});
