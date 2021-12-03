<template>
  <span>
    <b-row class="rd-filters-container justify-content-center">
      <b-col v-if="show_pred" class="col">
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
            v-model="advisor_filter"
            class="rd-advisor-filter"
            :options="current_advisors"
            value-field="advisor_netid"
            text-field="advisor_name"
            size="sm"
          >
            <template v-slot:first>
              <b-form-select-option :value="'all'">
                All advisers
              </b-form-select-option>
              <b-form-select-option :value="'no_assigned_adviser'">
                No assigned adviser
              </b-form-select-option>
            </template>
          </b-form-select>
        </b-form-group>
      </b-col>
      <b-col class="col">
        <range-filter filter-name="Sign-Ins" filter-store="filters/set_signins_filter" />
      </b-col>
      <b-col class="col">
        <range-filter filter-name="Activity" filter-store="filters/set_activity_filter" />
      </b-col>
      <b-col class="col">
        <range-filter filter-name="Assignments" filter-store="filters/set_assignment_filter" />
      </b-col>
      <b-col class="col">
        <range-filter filter-name="Grades" filter-store="filters/set_grade_filter" />
      </b-col>
      <b-col v-if="show_type" class="col">
        <b-form-group
          class="rd-student-filters"
          label="Student Type"
          label-class="rd-vis-hidden"
        >
          <b-form-checkbox v-model="premajor_filter">
            Is Pre-Major
          </b-form-checkbox>
          <b-form-checkbox v-model="stem_filter">
            Is STEM<span><a id="stem_info" href="#" class="rd-info-link" role="button" title="What is the 'Is STEM' filter?"><span class="sr-only"> What is the 'Is STEM' filter?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
              <b-popover target="stem_info" triggers="hover focus">
                <template v-slot:title>
                  Is STEM
                </template>
                Includes students in pre-science, pre-engineering and related pre-majors.
              </b-popover></span>
          </b-form-checkbox>
          <b-form-checkbox v-model="freshman_filter">
            Is Freshman
          </b-form-checkbox>
        </b-form-group>
      </b-col>
      <b-col class="col">
        <b-form-group
          v-if="current_sports && current_sports.length"
          label="Sport"
        >
          <b-form-select
            id="sport_filter"
            v-model="sport_filter"
            class="rd-sports-filter"
            :options="current_sports"
            value-field="sport_code"
            text-field="sport_desc"
            size="sm"
          >
            <template v-slot:first>
              <b-form-select-option :value="'all'">
                ALL STUDENTS
              </b-form-select-option>
            </template>
          </b-form-select>
        </b-form-group>
        <b-form-group
          class="rd-keyword-filter"
          label="Keyword"
        >
          <b-form-input v-model="keyword_filter" size="sm" placeholder="Student name, #, NetID" />
        </b-form-group>
      </b-col>
    </b-row>
    <b-row>
      <div class="rd-form-note">
        <span class="rd-form-key"><strong>Low</strong> -5 to -3</span><span class="rd-form-key"><strong class="rd-label">Average</strong> -2.9 to +2.9</span><span><strong>High</strong> +3 to +5</span>
      </div>
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
        weeks: [],
        auth_list: [],
        current_advisors: [],
        type: '',
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
        is_summer: state => state.dataselect.is_summer,
      }),
      advisors: {
        get () {
          return this.$store.state.advisors.advisors;
        },
        set (value) {
          this.$store.dispatch('advisors/set_advisors', value);
        }
      },
      sports: {
        get () {
          return this.$store.state.sports.sports;
        },
        set (value) {
          this.$store.dispatch('sports/set_sports', value);
        }
      },
      prediction_filter: {
        get () {
          return this.$store.state.filters.filters.prediction_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_prediction_filter', value);
        }
      },
      premajor_filter: {
        get () {
          return this.$store.state.filters.filters.premajor_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_premajor_filter', value);
        }
      },
      stem_filter: {
        get () {
          return this.$store.state.filters.filters.stem_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_stem_filter', value);
        }
      },
      freshman_filter: {
        get () {
          return this.$store.state.filters.filters.freshman_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_freshman_filter', value);
        }
      },
      advisor_filter: {
        get () {
          return this.$store.state.filters.filters.advisor_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_advisor_filter', value);
        }
      },
      summer_filter: {
        get () {
          return this.$store.state.filters.filters.summer_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_summer_filter', value);
        }
      },
      sport_filter: {
        get () {
          return this.$store.state.filters.filters.sport_filter;
        },
        set (value) {
          this.$store.dispatch('filters/set_sport_filter', value);
        }
      },
      keyword_filter: {
        get () {
          return this.$store.state.filters.filters.keyword_filter;
        },
        set: _.debounce(function(value) {
          this.$store.dispatch('filters/set_keyword_filter', 
                               value);
        }, 1000)
      },
      currentweek: {
        get () {
          if (this.$store.state.dataselect.current_week != '') {
            return this.$store.state.dataselect.current_week;
          } else if (this.weeks.length >= 1) {
            return this.weeks[this.weeks.length-1].value;
          } else {
            return this.$store.state.dataselect.current_week;
          }
        },
        set (value) {
          this.$store.dispatch('dataselect/set_week', value);
        }
      },
      show_pred () {
        return (this.current_file === "EOP" ||
          this.current_file == "ISS");
      },
      show_type () {
        return (this.current_file != "ISS");
      },
      sorted_weeks () {
        var sorted = this.weeks;
        if(sorted.length > 0){
          sorted.sort((a, b) => ((a.quarter, a.year, b.number) >
            (b.quarter, b.year, b.number)) ? -1 : 1);
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
      },
      current_sports: {
        get () {
          return this.sports[this.type];
        }
      },
    },
    watch: {
      advisors: function() {
        if(["ISS", "EOP"].includes(this.type)){
          this.current_advisors = this.advisors[this.type];
        }
      },
      currentweek: function(){
        this.selectWeek(this.currentweek);
        this.get_sports();
      },
      type: function(){
        this.advisor_filter = "all";
        this.sport_filter = "all";
        this.selectPage(this.type);
        if(this.type === "EOP"){
          this.get_advisors();
        } else if (this.type === "ISS"){
          this.stem_filter = false;
          this.freshman_filter = false;
          this.premajor_filter = false;
          this.get_advisors();
        }
      },
      auth_list: function() {
        this.type = this.auth_list[0];
      },
    },
    mounted: function(){
      this.get_weeks();
      this.get_types();
    },
    methods: {
      selectPage(page){
        this.$store.dispatch('dataselect/set_file', page);
      },
      selectWeek(week_value){
        let week = this.weeks.filter(e => e.value == week_value)[0];
        if(week.text.includes("Summer")){
          this.$store.dispatch('dataselect/set_summer', true);
        } else {
          this.$store.dispatch('dataselect/set_summer', false);
        }
      },
      get_weeks(){
        var vue = this;
        return axios.get('/api/v1/weeks/')
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
      },
      get_sports(){
        let week_num = this.weeks.filter(e => e.value == this.currentweek)[0];
        var vue = this;
        axios.get('/api/v1/sports/', {
          params: {
            week: week_num
          }
        }).then(function(response){
          vue.sports = response.data;
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
    margin: 0 10rem 0 10rem;
    padding: 0 0 1rem;

    fieldset .rd-keyword-filter {
      margin-right: 0;
      margin-top: 0.5rem;
      padding-right: 0;
    }

    .rd-advisor-filter {
      margin-top: 0.5rem;
      width: 90%;
    }

    .rd-student-filters .rd-info-link {
      font-size: 0.9rem;
    }

    .rd-student-filters .bi-info-circle-fill {
      transform: translateY(-4%);
    }

    .form-group {
      min-width: 100px;
    }

    .custom-control-label {
      width: 100%;
    }

  }

  .rd-filters-container > [class*='col']:before {
    background: $grey-border;
    bottom: 0;
    content: " ";
    left: 0;
    position: absolute;
    width: 1px;
    top: 0;
  }

  .rd-filters-container > [class*='col']:first-child:before {
    display: none;
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
