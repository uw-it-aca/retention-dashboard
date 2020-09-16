<template>
  <span>
    <b-row class="rd-filters-container justify-content-center">
      <b-col order="1" />
      <b-col v-if="show_pred" class="col-6 col-md-2 rd-filter-border" order="3" order-md="2">
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
              <b-form-select-option :value="1" selected>
                All advisors
              </b-form-select-option>
            </template>
          </b-form-select>
        </b-form-group>
      </b-col>
      <b-col class="col-12 col-md-auto" order="2" order-md="3">
        <b-row>
          <b-col class="col rd-filter-border">
            <range-filter filter-name="Activity" filter-store="filters/set_activity_filter" />
          </b-col>
          <b-col class="col rd-filter-border">
            <range-filter filter-name="Assignments" filter-store="filters/set_assignment_filter" />
          </b-col>
          <b-col class="col">
            <range-filter filter-name="Grades" filter-store="filters/set_grade_filter" />
          </b-col>
        </b-row>
        <b-row>
          <div class="rd-form-note">
            <span class="rd-form-key"><strong>Low</strong> -5 to -3</span><span class="rd-form-key"><strong class="rd-label">Average</strong> -2.9 to +2.9</span><span><strong>High</strong> +3 to +5</span>
          </div>
        </b-row>
      </b-col>
      <b-col class="col-6 col-md-2 rd-filter-border-end" order="4">
        <b-form-group
          class="rd-student-filters"
          label="Student Type"
          label-class="rd-vis-hidden"
        >
          <b-form-checkbox v-model="premajor_filter">
            Is Pre-Major
          </b-form-checkbox>
          <b-form-checkbox v-model="stem_filter">
            Is STEM
          </b-form-checkbox>
          <b-form-checkbox v-model="freshman_filter">
            Is Freshman
          </b-form-checkbox>
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
    <div class="rd-table-container">
      <span class="rd-file-select">
        <b-form inline>
          <b-form-group
            id="file-dropdown"
            label="Select Data"
            label-class="sr-only"
            label-for="type_dropdown"
          >
            <b-form-select
              id="type_dropdown"
              v-model="type"
              :options="auth_list"
              aria-controls="data_table"
              size="sm"
            />
          </b-form-group>
        </b-form>
      </span>
      <span class="rd-date-select">
        <b-form inline>
          <b-form-group
            id="date_select"
            label="Select week"
            label-class="sr-only"
            label-for="week_dropdown"
          >
            <b-form-select
              id="week_dropdown"
              v-model="currentweek"
              :options="sorted_weeks"
              aria-controls="data_table"
              size="sm"
            />
          </b-form-group>
        </b-form>
      </span>
      <span v-if="is_summer" class="rd-summer-term-select">
        <b-dropdown id="dropdown-form" ref="dropdown" class="rd-select-dropdown" :text="summer_display" size="sm">
          <b-dropdown-form>
            <b-form-checkbox-group
              v-model="summer_filter"
              :options="summer_terms"
              stacked
            />
          </b-dropdown-form>
        </b-dropdown>
      </span>
    </div>
  </span>
</template>

<script>

  import {_} from "vue-underscore";
  import Vuex from "vuex";
  import axios from 'axios';
  import RangeFilter from "./RangeFilter";

  export default {
    name: "Filters",
    components: {RangeFilter},
    props: {},
    data(){
      return {
        prediction_filter: [],
        premajor_filter: false,
        stem_filter: false,
        freshman_filter: false,
        keyword_filter: "",
        eop_advisor_selected: 1,
        eop_advisors: [],
        summer_filter: [],
        weeks: [],
        auth_list: [],
        advisors: [],
        type: '',
        currentweek: '',
        summer_terms: [
          { value: 'a', text: 'A Term' },
          { value: 'b', text: 'B Term' },
          { value: 'full', text: 'Full Term' }
        ],
      };
    },
    computed: {
      ...Vuex.mapState({
        current_file: state => state.dataselect.current_file,
        current_week: state => state.dataselect.current_week,
        is_summer: state => state.dataselect.is_summer,
        advisor_list: state => state.advisors.advisors
      }),
      show_pred (){
        return this.current_file === "EOP";
      },
      sorted_weeks () {
        var sorted = this.weeks;
        if(sorted.length > 0){
          sorted.sort((a, b) => (a.value > b.value) ? 1 : -1);
        }
        return sorted;
      },
      summer_display () {
        var term_names = [],
            vue = this;
        if (this.summer_filter.length === 0){
          term_names = ["Summer"];
        } else {
          $(vue.summer_filter).each(function(idx, val){
            term_names.push(val.toUpperCase());
          });
        }
        term_names.sort();
        return term_names.join(", ") + " Term";
      }

    },
    watch: {
      prediction_filter: function () {
        this.$store.dispatch('filters/set_prediction_filter', this.prediction_filter);
      },
      premajor_filter: function () {
        this.$store.dispatch('filters/set_premajor_filter', this.premajor_filter);
      },
      stem_filter: function () {
        this.$store.dispatch('filters/set_stem_filter', this.stem_filter);
      },
      freshman_filter: function () {
        this.$store.dispatch('filters/set_freshman_filter', this.freshman_filter);
      },
      keyword_filter: function () {
        this.debouncedKeywordFilters();
      },
      eop_advisor_selected: function () {
        this.$store.dispatch('filters/set_advisor_filter', this.eop_advisor_selected);
      },
      advisor_list: function() {
        this.eop_advisors = this.advisor_list["EOP"];
      },
      summer_filter: function () {
        this.$store.dispatch('filters/set_summer_filter', this.summer_filter);
      },
      current_file: function() {
        this.reset_filters();
      },
      currentweek: function(){
        this.selectWeek(this.currentweek);
      },
      type: function(){
        this.selectPage(this.type);
        if(this.type === "EOP"){
          this.get_advisors();
        }
      },
      weeks: function(){
        this.currentweek = this.weeks[this.weeks.length-1].value;
      },
      auth_list: function() {
        this.type = this.auth_list[0];
      },
      advisors: function(){
        this.setAdvisors(this.advisors);
      }
    },
    created: function () {
      this.debouncedKeywordFilters = _.debounce(this.run_keyword_filter, 1000);
    },
    mounted: function(){
      this.get_weeks();
      this.get_types();
    },
    methods: {
      run_keyword_filter() {
        this.$store.dispatch('filters/set_keyword_filter', this.keyword_filter);
      },
      reset_filters() {
        this.eop_advisor_selected = 1;
      },
      selectPage(page){
        this.$store.dispatch('dataselect/set_file', page);
      },
      selectWeek(week){
        var week_idx = week-1;
        this.$store.dispatch('dataselect/set_week', week);
        if(this.weeks[week_idx] !== undefined && this.weeks[week_idx].text.includes("Summer")){
          this.$store.dispatch('dataselect/set_summer', true);
        } else {
          this.$store.dispatch('dataselect/set_summer', false);
        }
      },
      setAdvisors(advisors){
        this.$store.dispatch('advisors/set_advisors', advisors);
      },
      get_weeks(){
        var vue = this;
        axios.get('/api/v1/weeks/')
          .then(function(response){
            vue.weeks = response.data;
          });
      },
      get_types(){
        var vue = this;
        axios.get('/api/v1/data_auth/')
          .then(function(response){
            vue.auth_list = response.data;
          });
      },
      get_advisors(){
        var vue = this;
        axios.get('/api/v1/advisors/')
          .then(function(response){
            vue.advisors = response.data;
          });
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

  .rd-student-filters legend.rd-vis-hidden {
    margin-bottom: -2em;
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

      .rd-student-filters {
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

  .rd-file-select,
  .rd-date-select {
    float: left;
    margin-right: 0.5rem;
  }

  /* summer term select  */
  .rd-summer-term-select {
    float: left;
  }

  .rd-select-dropdown button,
  .rd-select-dropdown button:hover,
  .rd-select-dropdown button:focus,
  .rd-select-dropdown.show .btn.btn-secondary.dropdown-toggle {
    background-color: #fff;
    border-color: #ced4da;
    color: #495057;
  }

  @media only screen and (max-width: 768px) {
    /* small screen date picker*/
    .rd-file-select {
      margin-bottom: 0.5rem;
    }

    .rd-file-select .form-group,
    .rd-date-select .form-group {
      margin-bottom: 0;
    }
  }
</style>
