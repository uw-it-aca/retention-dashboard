const params = new Proxy(new URLSearchParams(window.location.search), {
  get: (searchParams, prop) => searchParams.get(prop),
});

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

const state = {
  current_year: '',
  current_quarter: '',
  current_week: '',
  current_file: (params.type ? capitalizeFirstLetter(params.type) : ''),
  is_summer: false
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
  },
  set_summer ({ commit }, value) {
    commit('set_summer', value);
  }
};

// mutations
const mutations = {
  set_file (state, value){
    state.current_file = value;
  },
  set_week (state, value){
    state.current_week = value;
  },
  set_summer (state, value){
    state.is_summer = value;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
