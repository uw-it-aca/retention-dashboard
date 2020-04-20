const state = {
  current_year: '',
  current_quarter: '',
  current_week: '',
  current_file: ''
};

// getters
const getters = {};

// actions
const actions = {
  set_file ({ commit }, value) {
    commit('set_file', value);
  },
  set_week ({ commit }, value) {
    commit('set_week', value);
  }
};

// mutations
const mutations = {
  set_file (state, value){
    state.current_file = value;
  },
  set_week (state, value){
    state.current_week = value;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
