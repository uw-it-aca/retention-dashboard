import Vue from 'vue';
import Vuex from 'vuex';
import dataselect from './modules/dataselect';
import filters from './modules/filters';
import advisors from './modules/advisors';
import sports from './modules/sports';
import class_standings from './modules/class_standings';

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
    dataselect,
    filters,
    advisors,
    sports,
    class_standings
  },
});
