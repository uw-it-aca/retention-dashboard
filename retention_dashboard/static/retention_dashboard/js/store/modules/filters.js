const state = {
  filters: {
    activity_filter: [],
    assignment_filter: [],
    grade_filter: [],
    signins_filter: [],
    premajor_filter: false,
    stem_filter: false,
    freshman_filter: false,
    keyword_filter: "",
    prediction_filter: [],
    advisor_filter: "all",
    summer_filter: [],
    sports_filter: []
  }

};

// getters
const getters = {};

// actions
const actions = {
  set_activity_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'activity_filter',
      'value': value
    });
  },
  set_assignment_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'assignment_filter',
      'value': value
    });
  },
  set_grade_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'grade_filter',
      'value': value
    });
  },
  set_premajor_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'premajor_filter',
      'value': value
    });
  },
  set_stem_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'stem_filter',
      'value': value
    });
  },
  set_freshman_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'freshman_filter',
      'value': value
    });
  },
  set_keyword_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'keyword_filter',
      'value': value
    });
  },
  set_prediction_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'prediction_filter',
      'value': value
    });
  },
  set_advisor_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'advisor_filter',
      'value': value
    });
  },
  set_summer_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'summer_filter',
      'value': value
    });
  },
  set_signins_filter ({ commit }, value) {
    commit('set_filters', {
      'type': 'signins_filter',
      'value': value
    });
  },
  set_sports_filter ({ commit }, value) {
    commit('sports_filters', {
      'type': 'sports_filter',
      'value': value
    });
  },
};

// mutations
const mutations = {
  set_filters (state, payload) {
    state.filters[payload.type] = payload.value;
  }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
};
