const state = {
  sports: []
};

// getters
const getters = {};

// actions
const actions = {
  set_sports ({ commit }, value) {
    commit('set_sports', value);
  }
};

// mutations
const mutations = {
  set_sports (state, payload) {
    state.sports = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
