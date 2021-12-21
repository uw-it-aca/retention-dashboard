const state = {
    class_codes: []
  };
  
  // getters
  const getters = {};
  
  // actions
  const actions = {
    set_class_codes ({ commit }, value) {
      commit('set_class_codes', value);
    }
  };
  
  // mutations
  const mutations = {
    set_class_codes (state, payload) {
      state.class_codes = payload;
    }
  };
  
  export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
  };
  