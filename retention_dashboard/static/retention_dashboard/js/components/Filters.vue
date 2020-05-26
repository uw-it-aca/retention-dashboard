<template>
  <b-row class="rd-filters-container justify-content-center">
    <b-col order="1" />
    <b-col class="col-6 col-md-2 rd-filter-border" order="3" order-md="2" v-if="show_pred">
      <b-form-group
        label="Priority"
        aria-controls="data_table"
      >
        <b-form-checkbox-group id="pred_filters" v-model="prediction_filter" stacked>
          <b-form-checkbox value="low">
            Top
          </b-form-checkbox>
          <b-form-checkbox value="avg">
            Medium
          </b-form-checkbox>
          <b-form-checkbox value="high">
            Bottom
          </b-form-checkbox>
        </b-form-checkbox-group>
        <b-form-select
          id="advisor_filter"
          v-model="eop_advisor_selected"
          class="rd-advisor-filter"
          :options="eop_advisors"
          value-field="advisor_netid"
          text-field="advisor_name"
          size="sm"
        >
        <template v-slot:first>
          <b-form-select-option :value="1" selected>All advisors</b-form-select-option>
        </template>
        </b-form-select>
      </b-form-group>
    </b-col>
    <b-col class="col-12 col-md-auto" order="2" order-md="3">
      <b-row>
        <b-col class="col rd-filter-border">
          <b-form-group
            label="Activity"
          >
            <b-form-checkbox-group id="activity_filters" v-model="activity_filter" stacked>
              <b-form-checkbox value="high">
                High
              </b-form-checkbox>
              <b-form-checkbox value="avg">
                Average
              </b-form-checkbox>
              <b-form-checkbox value="low">
                Low
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
        </b-col>
        <b-col class="col rd-filter-border">
          <b-form-group
            label="Assignments"
          >
            <b-form-checkbox-group id="assignment_filters" v-model="assignment_filter" stacked>
              <b-form-checkbox value="high">
                High
              </b-form-checkbox>
              <b-form-checkbox value="avg">
                Average
              </b-form-checkbox>
              <b-form-checkbox value="low">
                Low
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
        </b-col>
        <b-col class="col">
          <b-form-group
            label="Grades"
          >
            <b-form-checkbox-group id="grade_filters" v-model="grade_filter" stacked>
              <b-form-checkbox value="high">
                High
              </b-form-checkbox>
              <b-form-checkbox value="avg">
                Average
              </b-form-checkbox>
              <b-form-checkbox value="low">
                Low
              </b-form-checkbox>
            </b-form-checkbox-group>
          </b-form-group>
        </b-col>
      </b-row>
      <b-row>
        <div class="rd-form-note">
          <span class="rd-form-key"><strong>Low</strong> -5 to -3</span><span class="rd-form-key"><strong class="rd-label">Average</strong> -2 to +2</span><span><strong>High</strong> +3 to +5</span>
        </div>
      </b-row>
    </b-col>
    <b-col class="col-6 col-md-2 rd-filter-border-end" order="4">
      <b-form-group
        class="rd-major-filters"
        label="Major Type"
        label-class="rd-vis-hidden"
      >
        <b-form-checkbox v-model="premajor_filter">
          Is Pre-Major
        </b-form-checkbox>
        <!-- <b-form-checkbox v-model="stem_filter">Is STEM</b-form-checkbox> -->
        <b-form-group
          class="rd-keyword-filter"
          label="Keyword"
        >
          <b-form-input v-model="keyword_filter" size="sm" placeholder="Student name, #, NetID" />
        </b-form-group>
      </b-form-group>
    </b-col>
    <b-col order="5" />
  </b-row>
</template>

<script>

  import {_} from "vue-underscore";
  import Vuex from "vuex";
  export default {
    name: "Filters",
    components: {},
    props: {},
    data(){
      return {
        activity_filter: [],
        assignment_filter: [],
        grade_filter: [],
        prediction_filter: [],
        premajor_filter: false,
        keyword_filter: "",
        eop_advisor_selected: "1",
        eop_advisors: []
      };
    },
    computed: {
      ...Vuex.mapState({
        current_file: state => state.dataselect.current_file,
        advisor_list: state => state.advisors.advisors,
      }),
      show_pred (){
        return this.current_file === "EOP";
      }

    },
    watch: {
      assignment_filter: function () {
        this.$store.dispatch('filters/set_assignment_filter', this.assignment_filter);
      },
      grade_filter: function () {
        this.$store.dispatch('filters/set_grade_filter', this.grade_filter);
      },
      activity_filter: function () {
        this.$store.dispatch('filters/set_activity_filter', this.activity_filter);
      },
      prediction_filter: function () {
        this.$store.dispatch('filters/set_prediction_filter', this.prediction_filter);
      },
      premajor_filter: function () {
        this.$store.dispatch('filters/set_premajor_filter', this.premajor_filter);
      },
      keyword_filter: function () {
        this.debouncedKeywordFilters();
      },
      eop_advisor_selected: function () {
        this.$store.dispatch('filters/set_advisor_filter', this.eop_advisor_selected);
      },
      advisor_list: function() {
        this.eop_advisors = this.advisor_list["EOP"];
      }
    },
    created: function () {
      this.debouncedKeywordFilters = _.debounce(this.run_keyword_filter, 1000);
    },
    methods: {
      run_keyword_filter() {
        this.$store.dispatch('filters/set_keyword_filter', this.keyword_filter);
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  /* main content styles */
  /* filter styles */

  .rd-filters-container {
    margin: auto;
    padding: 0 0 1rem;

    .rd-filter-border {
      border: 1px $grey-border solid;
      border-style: none solid none none;
    }

    .rd-filter-border-end {
      border: 1px $grey-border solid;
      border-style: none none none solid;
    }

    fieldset .rd-keyword-filter {
      margin-right: 0;
      margin-top: 0.5rem;
      padding-right: 0;
    }

    .rd-advisor-filter {
      margin-top: 0.5rem;
      width: 90%;
    }

    .form-group {
      min-width: 100px;
    }

  }

  .rd-filters-container fieldset legend {
    font-weight: bold;
  }

  .rd-form-note {
    clear: both;
    font-size: 85%;
    margin: 0 auto;
    padding-top: 1rem;
  }

  .rd-form-key {
    padding-right: 1rem;
  }

  /* input style */
  input::placeholder {
    font-size: 0.7rem;
  }

  @media only screen and (max-width: 800px) {
    /* small screen filter styles */

    .rd-filters-container {
      .rd-filter-border,
      .rd-filter-border-end {
        border-style: none;
      }

      fieldset {
        margin: 0;
        padding: 0;
      }

      .rd-grades-filters {
        margin: 0;
        padding: 0;
      }

      .rd-major-filters {
        border-style: none;
        margin: 0;
        padding: 0;
      }

      .form-group {
        min-width: auto;
      }
    }

    .rd-form-note {
      margin: 0;
      padding-bottom: 2rem;
      padding-left: 15px;
    }

  }
</style>
