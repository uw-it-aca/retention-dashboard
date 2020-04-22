<template>
  <b-container class="rd-main-container" fluid>
    <b-row class="rd-listactions-container">
      <b-col>
        <p role="alert">
          Table contains <span class="rd-student-count">{{ selected_count }}</span> students:
          <b-link v-b-modal.email-modal class="rd-action-link">
            get e-mail addresses
          </b-link> or
          <b-link id="csv_download" class="rd-action-link" @click="download_filtered">
            download results
          </b-link>
        </p>
        <b-modal id="email-modal" title="E-Mail Addresses" ok-only>
          <div class="container">
            <textarea id="email_area" v-model="email_list_text" readonly />
            <button v-clipboard:copy="email_list_text">
              copy
            </button>
          </div>
        </b-modal>
      </b-col>
    </b-row>
    <b-row class="rd-filters-container justify-content-center">
      <span class="rd-filter-group">
        <b-form-group
          label="Activity"
        >
          <b-form-checkbox-group id="activity_filters" v-model="activity_filter" stacked>
            <b-form-checkbox value="high">High</b-form-checkbox>
            <b-form-checkbox value="average">Average</b-form-checkbox>
            <b-form-checkbox value="low">Low</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group
          label="Assignments"
        >
          <b-form-checkbox-group id="assignment_filters" v-model="assignment_filter" stacked>
            <b-form-checkbox value="high">High</b-form-checkbox>
            <b-form-checkbox value="average">Average</b-form-checkbox>
            <b-form-checkbox value="low">Low</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <div class="rd-form-note"><span class="rd-form-key"><strong>Low</strong> -5 to -3</span><span class="rd-form-key"><strong class="rd-label">Average</strong> -2 to +2</span><span><strong>High</strong> +3 to +5</span></div>
      </span>
      <span class="rd-filter-group rd-filter-group-bottom">
        <b-form-group
          class="rd-grades-filters"
          label="Grades"
        >
          <b-form-checkbox-group id="grade_filters" v-model="grade_filter" stacked>
            <b-form-checkbox value="high">High</b-form-checkbox>
            <b-form-checkbox value="average">Average</b-form-checkbox>
            <b-form-checkbox value="low">Low</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-form-group
          class="rd-major-filters"
          label="Major Type"
          label-class="rd-vis-hidden"
        >
          <b-form-checkbox v-model="premajor_filter">Is Pre-Major</b-form-checkbox>
          <!-- <b-form-checkbox v-model="stem_filter">Is STEM</b-form-checkbox> -->
          <b-form-group
            class="rd-keyword-filter"
            label="Keyword"
          >
            <b-form-input v-model="keyword_filter" size="sm" placeholder="Student name, #, NetID" />
          </b-form-group>
        </b-form-group>
      </span>
    </b-row>
    <b-row class="rd-table-container">
      <b-col cols="5" md="9">
        <dataselect />
      </b-col>
      <b-col cols="7" md="3" class="rd-pagination-container">
        <b-pagination
          v-model="currentPage"
          align="right"
          class="pagination-sm"
          :total-rows="rows"
          :per-page="perPage"
          aria-controls="data_table"
          first-number
          last-number
        />
      </b-col>
    </b-row>
    <b-table
      id="data_table"
      no-border-collapse
      responsive
      show-empty
      sticky-header
      :items="items"
      :fields="fields"
      :per-page="perPage"
      :current-page="currentPage"
      sort-icon-left
    >
      <template v-slot:head(activity)="data">
        {{ data.label }}<a id="activity_info" href="#" class="rd-info-link" role="button" title="What is the Activity score?"><span class="sr-only">What is the Activity Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="activity_info" triggers="hover focus">
          <template v-slot:title>
            Activity Score
          </template>
          This score is indicative of the level a student is interacting with Canvas relative to her classmates. Any number above or below zero indicates a student has greater or less than average activity, respectively. If a student is taking more than one course in Canvas, her score is an average across the courses she is taking.
        </b-popover>
      </template>

      <template v-slot:head(assignments)="data">
        {{ data.label }}<a id="assignments_info" href="#" class="rd-info-link" role="button" title="What is the Assignments score?"><span class="sr-only">What is the Assignments Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="assignments_info" triggers="hover focus">
          <template v-slot:title>
            Assignments Score
          </template>
          This score is indicative of how the student is doing relative to her classmates with regards to the status of assignments (e.g. # of missing assignments). Any number above or below zero indicates a student is doing better or worse than average. If the student is taking more than one course in Canvas, her score is an average across the courses she is taking.
        </b-popover>
      </template>

      <template v-slot:head(grades)="data">
        {{ data.label }}<a id="grades_info" href="#" class="rd-info-link" role="button" title="What is the Grades score?"><span class="sr-only">What is the Grades Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="grades_info" triggers="hover focus">
          <template v-slot:title>
            Grades Score
          </template>
          This score represents the student’s grade in Canvas relative to her classmates. Any number above or below zero indicates a student has a better or worse grade than the course average. If the student is taking more than one course in Canvas, her grades are averaged across the courses she is taking.
        </b-popover>
      </template>

      <template v-slot:cell(grades)="row">
        <span v-if="row.item.grades === -99">No data</span>
        <span v-else>{{ row.item.grades }}</span>
      </template>

      <template v-slot:cell(activity)="row">
        <span v-if="row.item.activity === -99">No data</span>
        <span v-else>{{ row.item.activity }}</span>
      </template>

      <template v-slot:cell(assignments)="row">
        <span v-if="row.item.assignments === -99">No data</span>
        <span v-else>{{ row.item.assignments }}</span>
      </template>

      <template v-slot:cell(premajor)="row">
        <span v-if="row.item.premajor === true"><b-icon icon="check-box" scale="1.5" /><span class="sr-only">{{ row.item.premajor }}</span></span>
        <span v-else class="sr-only">{{ row.item.premajor }}</span>
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      align="right"
      class="pagination-sm"
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="data_table"
      first-number
      last-number
    />
  </b-container>
</template>
<script>
  import DataSelect from "./DataSelect.vue";
  import Vuex from 'vuex';
  import {_} from 'vue-underscore';
  import axios from 'axios';
  export default {
    name: "DataView",
    components: {
      dataselect: DataSelect
    },
    data: function() {
      return {
        fields: [
          {
            key: 'student_name_lowc',
            label: "Student Name",
            sortable: true
          },
          {
            key: 'student_no',
            label: "Student Number",
            class: 'text-center'
          },

          {
            key: 'uw_netid',
            label: 'UWNetid',
            class: 'text-center'
          },
          {
            key: 'activity',
            label: 'Activity',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'assignments',
            label: 'Assignments',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'grades',
            label: 'Grades',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'premajor',
            label: 'Pre-Major',
            class: 'text-center',
            sortable: true
          }
        ],
        items: [],
        raw_items: [],
        csv_data: "",
        perPage: 200,
        currentPage: 1,
        selected: {},
        activity_filter: [],
        assignment_filter: [],
        grade_filter: [],
        premajor_filter: false,
        keyword_filter: "",
        low_min: -5,
        low_max: -3,
        average_min: -2.999999999999999,
        average_max: 2.999999999999999,
        high_min: 3,
        high_max: 5
      };
    },
    computed: {
      filename (){
        return this.$store.state.current_file;
      },
      rows (){
        return this.items.length;
      },
      selected_count (){
        return this.items.length;
      },
      email_list_text () {
        var selected = this.get_filtered_emails();
        return selected.join(", ");
      },
      ...Vuex.mapState({
        current_week: state => state.dataselect.current_week,
        current_file: state => state.dataselect.current_file
      })
    },
    watch: {
      csv_data: function (csv){
        var parsed_csv = this.$papa.parse(csv, {header: true}),
            csv_data = parsed_csv.data,
            vue = this;
        csv_data.forEach(function(item){
          item["premajor"] = (item["premajor"] === "1" ? true: false);
          item["student_no"] = Number(item["student_no"]);

          item['activity'] = vue.get_rounded(item['activity']);
          item['assignments'] = vue.get_rounded(item['assignments']);
          item['grades'] = vue.get_rounded(item['grades']);
        });
        this.items = csv_data;
        this.raw_items = csv_data.slice();
        this.run_filters();
      },
      assignment_filter: function () {
        this.run_filters();
      },
      grade_filter: function () {
        this.run_filters();
      },
      activity_filter: function () {
        this.run_filters();
      },
      premajor_filter: function () {
        this.run_filters();
      },
      keyword_filter: function () {
        this.debouncedRunFilters();
      }

    },
    mounted: function(){
      this.$store.watch(
        state => state.dataselect.current_file,
        () => {
          this.load_file();
        }
      );
      this.$store.watch(
        state => state.dataselect.current_week,
        () => {
          this.load_file();
        }
      );
      this.$store.dispatch('dataselect/set_file', "international-students.csv");
      this.$store.dispatch('dataselect/set_week', "2");
    },
    created: function () {
      this.debouncedRunFilters = _.debounce(this.run_filters, 1000);
    },
    methods: {
      get_filtered_emails(){
        var emails = [];
        this.items.forEach(function(item){
          emails.push(item['uw_netid'] + "@uw.edu");
        });
        return emails;
      },
      load_file(){
        var vue = this,
            filename = this.current_week + "/" + this.current_file;
        axios.get('/api/data/' + filename + "/")
          .then(function(response){
            vue.csv_data = response.data.data;
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      download_filtered() {
        var to_download = this.items,
            hiddenElement = document.createElement('a'),
            timestamp = Math.round(Date.now()/1000),
            csv_string = "";

        // Header
        var fields = Object.keys(to_download[0]);
        csv_string += fields.join(",");
        csv_string += "\n";

        // Data
        to_download.forEach(function(item){

          var row_string = "";
          fields.forEach(function(field){
            if(item[field] === -99){
              row_string += "NA,";
            } else {
              row_string += item[field] + ",";
            }
          });
          //remove trailing comma
          csv_string += row_string.slice(0, -1) + "\n";
        });

        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv_string);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'rentention_export_'+timestamp+'.csv';
        hiddenElement.click();
      },
      run_filters(){
        // Start by resetting items
        this.items = this.raw_items.slice();

        //Activity Filters
        if(this.activity_filter.includes("low") || this.activity_filter.includes("average") || this.activity_filter.includes("high")){
          var activity_items = [];
          if(this.activity_filter.includes("low")){
            activity_items = activity_items.concat(this.filter_by_range('activity', this.low_min, this.low_max));
          }
          if(this.activity_filter.includes("average")){
            activity_items = activity_items.concat(this.filter_by_range('activity', this.average_min, this.average_max));
          }
          if(this.activity_filter.includes("high")){
            activity_items =activity_items.concat(this.filter_by_range('activity', this.high_min, this.high_max));
          }
          this.items = activity_items;
        }

        //Assignment Filters
        if(this.assignment_filter.includes("low") || this.assignment_filter.includes("average") || this.assignment_filter.includes("high")) {
          var assignment_items = [];
          if (this.assignment_filter.includes("low")) {
            assignment_items = assignment_items.concat(this.filter_by_range('assignments', this.low_min, this.low_max));
          }
          if (this.assignment_filter.includes("average")) {
            assignment_items = assignment_items.concat(this.filter_by_range('assignments', this.average_min, this.average_max));
          }
          if (this.assignment_filter.includes("high")) {
            assignment_items = assignment_items.concat(this.filter_by_range('assignments', this.high_min, this.high_max));
          }
          this.items = assignment_items;
        }

        //Grade Filters
        if(this.grade_filter.includes("low") || this.grade_filter.includes("average") || this.grade_filter.includes("high")) {
          var grade_items = [];
          if (this.grade_filter.includes("low")) {
            grade_items = grade_items.concat(this.filter_by_range('grades', this.low_min, this.low_max));
          }
          if (this.grade_filter.includes("average")) {
            grade_items = grade_items.concat(this.filter_by_range('grades', this.average_min, this.average_max));
          }
          if (this.grade_filter.includes("high")) {
            grade_items = grade_items.concat(this.filter_by_range('grades', this.high_min, this.high_max));
          }
          this.items = grade_items;
        }

        //Premajor Filter
        if(this.premajor_filter) {
          var premajor_items = this.filter_by_value("premajor", true);
          this.items = premajor_items;
        }

        //Keyword Filter
        if(this.keyword_filter.length > 0){
          var keyword_items = this.filter_by_text(this.keyword_filter);
          this.items = keyword_items;

        }
      },
      filter_by_range(attr, min_value, max_value){
        var items =  this.items,
            matches = [];
        items.forEach(function (item) {
          if(min_value <= parseFloat(item[attr]) && parseFloat(item[attr]) <= max_value){
            matches.push(item);
          }
        });
        return matches;
      },
      filter_by_value(attr, value){
        var items =  this.items,
            matches = [];
        items.forEach(function (item) {
          if(item[attr] == value){
            matches.push(item);
          }
        });
        return matches;
      },
      filter_by_text(text){
        var items =  this.items,
            matches = [];
        text = text.trim().toLowerCase();
        items.forEach(function (item) {
          Object.keys(item).forEach(function(key){
            if(item[key].toString().toLowerCase().includes(text)){
              matches.push(item);
            }
          });
        });

        return matches;
      },
      get_rounded(num_string){
        var number = Number(num_string);
        return Number(number.toFixed(1));
      }
    }
  };
</script>

<style lang="scss">
  /* Structure */

  .row.rd-listactions-container {
    background-color: #dedede;
    border-bottom: solid 2px #cdcdcd;
    line-height: 2;
    margin-bottom: 2rem;
    padding: 1rem 0;

    .col{
      text-align: center;
    }
  }

  /* Top banner styles */

  .rd-info-link {
    margin-left: 0.25rem;
  }

  a.rd-help-link:focus svg,a.rd-help-link:hover svg {
    color: lightslategrey !important;
  }

  /* filter styles */

  .rd-filters-container {
    padding: 0 15px 1rem;

    fieldset {
      border: 1px #ccc solid;
      border-style: none solid none none;
      float: left;
      margin: 0 2rem 0 0;
      padding: 0 2rem 0 0;

      &.rd-grades-filters {
        border: none;
        margin: 0;
        padding: 0;
      }

      &.rd-major-filters {
        border: 1px #ccc solid;
        border-style: none none none solid;
        float: left;
        margin: 0 0 0 2rem;
        padding: 0 0 0 2rem;

        .rd-keyword-filter {
          border: none;
          margin-right: 0;
          margin-top: 0.5rem;
          padding-right: 0;
        }
      }
    }
  }

  .rd-filters-container fieldset legend {
    font-weight: bold;
  }

  .rd-form-note {
    clear: both;
    font-size: 85%;
    padding-top: 1rem;
  }

  .rd-form-key {
    padding-right: 1rem;
  }

  /* Pagination */
  .rd-pagination-container {
    align-self: flex-end;
  }

  /* main content styles */
  .rd-student-count {
    background-color: #4b2e83;
    border-radius: 4px;
    color: white;
    margin: 0 2px;
    padding: 3px 6px;
  }

  .rd-table-container {
    margin-top: 2rem;
  }

  @media only screen and (max-width: 558px) {
    /* small screen filter styles */

    .rd-filters-container fieldset {
      border-style: none;
      margin: 0;
      padding: 0;
      width: 130px;

      &.rd-grades-filters {
        margin: 0;
        padding: 0;
      }

      &.rd-major-filters {
        border-style: none;
        margin: 0;
        padding: 0;
      }
    }

    .rd-filter-group-bottom {
      margin-top: 2rem;
    }

    .rd-form-note {
      padding-top: 1rem;
    }

  }
</style>
