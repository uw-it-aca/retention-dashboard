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
    <filters />
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
      <template v-slot:head(pred)="data">
        {{ data.label }}<a id="pred_info" href="#" class="rd-info-link" role="button" title="What is the Priority score?"><span class="sr-only">What is the Priority Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="pred_info" triggers="hover focus">
          <template v-slot:title>
            Priority Score
          </template>
          This score is derived from a model that predicts how well a student will do this quarter. Students with the greatest risk of having a poor quarter are considered top priority, while those who are predicted to have a good quarter are considered bottom priority.
        </b-popover>
      </template>

      <template v-slot:head(activity)="data">
        {{ data.label }}<a id="activity_info" href="#" class="rd-info-link" role="button" title="What is the Activity score?"><span class="sr-only">What is the Activity Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="activity_info" triggers="hover focus">
          <template v-slot:title>
            Activity Score
          </template>
          This score is indicative of the level a student is interacting with Canvas relative to her classmates. Any number above or below zero indicates a student has greater or less than average activity, respectively. If a student is taking more than one course in Canvas, her score is an average across the courses she is taking.<br><br><strong>No Data</strong> indicates Canvas use is not a course requirement.
        </b-popover>
      </template>

      <template v-slot:head(assignments)="data">
        {{ data.label }}<a id="assignments_info" href="#" class="rd-info-link" role="button" title="What is the Assignments score?"><span class="sr-only">What is the Assignments Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="assignments_info" triggers="hover focus">
          <template v-slot:title>
            Assignments Score
          </template>
          This score is indicative of how the student is doing relative to her classmates with regards to the status of assignments (e.g. # of missing assignments). Any number above or below zero indicates a student is doing better or worse than average. If the student is taking more than one course in Canvas, her score is an average across the courses she is taking.<br><br><strong>No Data</strong> indicates Canvas use is not a course requirement.
        </b-popover>
      </template>

      <template v-slot:head(grades)="data">
        {{ data.label }}<a id="grades_info" href="#" class="rd-info-link" role="button" title="What is the Grades score?"><span class="sr-only">What is the Grades Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="grades_info" triggers="hover focus">
          <template v-slot:title>
            Grades Score
          </template>
          This score represents the student’s grade in Canvas relative to her classmates. Any number above or below zero indicates a student has a better or worse grade than the course average. If the student is taking more than one course in Canvas, her grades are averaged across the courses she is taking.<br><br><strong>No Data</strong> indicates Canvas use is not a course requirement.
        </b-popover>
      </template>

      <template v-slot:cell(grade_score)="row">
        <span v-if="row.item.grade_score === -99">No data</span>
        <span v-else>{{ row.item.grade_score }}</span>
      </template>

      <template v-slot:cell(activity_score)="row">
        <span v-if="row.item.activity_score === -99">No data</span>
        <span v-else>{{ row.item.activity_score }}</span>
      </template>

      <template v-slot:cell(assignment_score)="row">
        <span v-if="row.item.assignment_score === -99">No data</span>
        <span v-else>{{ row.item.assignment_score }}</span>
      </template>

      <template v-slot:cell(is_premajor)="row">
        <span v-if="row.item.is_premajor === true"><b-icon icon="check-box" scale="1.5" /><span class="sr-only">{{ row.item.is_premajor }}</span></span>
        <span v-else class="sr-only">{{ row.item.is_premajor }}</span>
      </template>

      <template v-slot:cell(priority_score)="row">
        <span v-if="row.item.priority_score === -99" />
        <span v-else class="rd-pred-score">
          <span v-if="row.item.priority_score >= -5 && row.item.priority_score <= -3"><span class="rd-pred-label rd-pred-label-top">Top</span> {{ row.item.priority_score }}</span>
          <span v-else-if="row.item.priority_score >= -2.9 && row.item.priority_score <= 2.9"><span class="rd-pred-label rd-pred-label-medium">Medium</span> {{ row.item.priority_score }}</span>
          <span v-else-if="row.item.priority_score >= 3 && row.item.priority_score <= 5"><span class="rd-pred-label rd-pred-label-bottom">Bottom</span> {{ row.item.priority_score }}</span>
          <span v-else />
        </span>
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
  import Filters from "./Filters.vue";
  import Vuex from 'vuex';
  import axios from 'axios';
  import qs from 'qs';

  export default {
    name: "DataView",
    components: {
      dataselect: DataSelect,
      filters: Filters
    },
    data: function() {
      return {
        eop_fields: [
          {
            key: 'student_name',
            label: "Student Name",
            sortable: true
          },
          {
            key: 'student_number',
            label: "Student Number",
            class: 'text-center'
          },

          {
            key: 'netid',
            label: 'UWNetid',
            class: 'text-center'
          },
          {
            key: 'priority_score',
            label: 'Priority',
            sortable: true
          },
          {
            key: 'activity_score',
            label: 'Activity',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'assignment_score',
            label: 'Assignments',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'grade_score',
            label: 'Grades',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'is_premajor',
            label: 'Pre-Major',
            class: 'text-center',
            sortable: true
          }
        ],
        standard_fields: [
          {
            key: 'student_name',
            label: "Student Name",
            sortable: true
          },
          {
            key: 'student_number',
            label: "Student Number",
            class: 'text-center'
          },

          {
            key: 'netid',
            label: 'UWNetid',
            class: 'text-center'
          },
          {
            key: 'activity_score',
            label: 'Activity',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'assignment_score',
            label: 'Assignments',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'grade_score',
            label: 'Grades',
            class: 'text-center',
            sortable: true
          },
          {
            key: 'is_premajor',
            label: 'Pre-Major',
            class: 'text-center',
            sortable: true
          }
        ],
        items: [],
        csv_data: "",
        perPage: 200,
        currentPage: 1,
        selected: {},
        low_min: -5,
        low_max: -3,
        average_min: -2.999999999999999,
        average_max: 2.999999999999999,
        high_min: 3,
        high_max: 5
      };
    },
    computed: {
      fields (){
        if (this.current_file === "EOP"){
          return this.eop_fields;
        } else {
          return this.standard_fields;
        }
      },
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
      filter_params () {
        const params = {};
        params['week'] = this.current_week;
        params['type'] = this.current_file;

        if(this.grade_filter.length > 0){
          params['grade_filters'] = this.grade_filter;
        }
        if(this.assignment_filter.length > 0){
          params['assignment_filters'] = this.assignment_filter;
        }
        if(this.prediction_filter.length > 0){
          params['priority_filters'] = this.prediction_filter;
        }
        if(this.activity_filter.length > 0){
          params['activity_filters'] = this.activity_filter;
        }
        if(this.premajor_filter === true){
          params['premajor_filter'] = this.premajor_filter;
        }
        if(this.keyword_filter.length > 0){
          params['text_filter'] = this.keyword_filter;
        }
        return params;
      },
      ...Vuex.mapState({
        current_week: state => state.dataselect.current_week,
        current_file: state => state.dataselect.current_file,
        activity_filter: state => state.filters.filters.activity_filter,
        assignment_filter: state => state.filters.filters.assignment_filter,
        grade_filter: state => state.filters.filters.grade_filter,
        prediction_filter: state => state.filters.filters.prediction_filter,
        premajor_filter: state => state.filters.filters.premajor_filter,
        keyword_filter: state => state.filters.filters.keyword_filter,
      })
    },
    watch: {
      csv_data: function (csv){
        var vue = this;
        csv.forEach(function(item){
          item["student_number"] = Number(item["student_number"]);

          item['activity_score'] = vue.get_rounded(item['activity_score']);
          item['assignment_score'] = vue.get_rounded(item['assignment_score']);
          item['grade_score'] = vue.get_rounded(item['grade_score']);
        });
        this.items = csv;
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
      prediction_filter: function () {
        this.run_filters();
      },
      premajor_filter: function () {
        this.run_filters();
      },
      keyword_filter: function () {
        this.run_filters();
      },
      current_week: function () {
        this.run_filters();
      },
      current_file: function () {
        this.run_filters();
      },

    },
    methods: {
      get_filtered_emails(){
        var emails = [];
        this.items.forEach(function(item){
          emails.push(item['netid'] + "@uw.edu");
        });
        return emails;
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
        var vue = this;
        if(this.current_file.length < 1 || this.current_week.length < 1){
          // don't fire ajax unless week and type are set
          return;
        }
        axios({
          method: 'get',
          url: "/api/v1/filtered_data/",
          paramsSerializer: function (params) {
            return qs.stringify(params, {arrayFormat: 'repeat'});
          },
          params: this.filter_params,
        })
          .then(function(response){
            vue.csv_data = response.data.rows;
          });
      },
      get_rounded(num_string){
        var number = Number(num_string);
        return Number(number.toFixed(1));
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  /* Structure */

  .row.rd-listactions-container {
    background-color: $grey-bkgnd;
    border-bottom: solid 2px $grey-border;
    line-height: 2;
    margin-bottom: 2rem;
    padding: 1rem 0;

    .col {
      text-align: center;
    }
  }

  /* Top banner styles */

  .rd-info-link {
    margin-left: 0.25rem;
  }


  /* Pagination */
  .rd-pagination-container {
    align-self: flex-end;
  }

  /* main content styles */
  .rd-student-count {
    background-color: $uw-purple;
    border-radius: 4px;
    color: $white-text;
    margin: 0 2px;
    padding: 3px 6px;
  }

  .rd-table-container {
    margin-top: 2rem;
  }

  /* Prediction scores */
  .rd-pred-score {
    font-size: 0.75rem;
    text-transform: uppercase;
    white-space: nowrap;
  }

  .rd-pred-label {
    font-size: 1rem;
  }

  .rd-pred-label-top {
    color: #ca231d;
  }

  .rd-pred-label-medium {
    color: #b7961e;
  }

  .rd-pred-label-bottom {
    color: #129562;
  }
</style>
