import Vue from 'vue'
import Vuex from 'vuex'
import dataselect from './modules/dataselect'

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
    dataselect
  },
})