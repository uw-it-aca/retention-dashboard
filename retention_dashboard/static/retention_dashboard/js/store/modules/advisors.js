const state = {
  advisors: []
};

// getters
const getters = {};

// actions
const actions = {
  set_advisors ({ commit }, value) {
    commit('set_advisors', value);
  }
};

// mutations
const mutations = {
  set_advisors (state, payload) {
    state.advisors = payload;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
