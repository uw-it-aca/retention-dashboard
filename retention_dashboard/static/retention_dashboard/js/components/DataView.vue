<template>
  <b-container class="rd-main-container" fluid>
    <b-row class="rd-listactions-container">
      <b-col>
        <p role="alert">
          Table contains <span class="rd-student-count">{{ rowCount }}</span> students:
          <b-link v-b-modal.email-modal class="rd-action-link">
            get e-mail addresses
          </b-link> or
          <b-link id="csv_download" class="rd-action-link" @click="get_csv_file">
            download results
          </b-link>
          <b-spinner v-show="isDownloading" label="Spinning" small />
        </p>
        <b-modal id="email-modal" title="Copy E-Mail Addresses" ok-title="Done" ok-only>
          <div class="container rd-copy-email">
            <div>
              <textarea id="email_area" v-model="email_list_text" rows="10" readonly />
            </div>
            <div class="rd-copy-email-btn">
              <b-button v-clipboard:copy="email_list_text" variant="info">
                copy
              </b-button>
              <p class="small rd-copy-email-desc">
                Press 'copy' button to copy email addresses to clipboard
              </p>
            </div>
          </div>
        </b-modal>
      </b-col>
    </b-row>
    <filters />
    <span class="rd-pagination-container">
      <b-pagination
        v-model="currentPage"
        align="right"
        class="pagination-sm"
        :total-rows="rowCount"
        :per-page="perPage"
        first-number
        last-number
      />
    </span>
    <b-table
      id="data_table"
      no-border-collapse
      responsive
      show-empty
      :busy="isBusy"
      :items="items"
      :fields="fields"
      :sort-compare="customSorting"
      sort-icon-left
    >
      <template v-slot:head(priority_score)="data">
        {{ data.label }}<a id="pred_info" href="#" class="rd-info-link" role="button" title="What is the Priority score?"><span class="sr-only">What is the Priority Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="pred_info" triggers="hover focus">
          <template v-slot:title>
            Priority Score
          </template>
          This score is derived from a model that predicts how well a student will do this quarter. Students with the greatest risk of having a poor quarter are considered top priority, while those who are predicted to have a good quarter are considered bottom priority.
        </b-popover>
      </template>

      <template v-slot:head(signin_score)="data">
        {{ data.label }}<a id="sign_in_info" href="#" class="rd-info-link" role="button" title="What is the Sign-Ins score?"><span class="sr-only">What is the Sign-Ins Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="sign_in_info" triggers="hover focus">
          <template v-slot:title>
            Sign-Ins Score
          </template>
          This score represents how often a student is signing in to UW online systems that require a NetID <em>during the past week</em>. Any number above or below zero indicates a student is signing in more or less than other undergrads, respectively.<br><br><strong>No Data</strong> indicates that the student has not signed in to any UW system during the specific time range.
        </b-popover>
      </template>

      <template v-slot:head(activity_score)="data">
        {{ data.label }}<a id="activity_info" href="#" class="rd-info-link" role="button" title="What is the Activity score?"><span class="sr-only">What is the Activity Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="activity_info" triggers="hover focus">
          <template v-slot:title>
            Activity Score
          </template>
          This score is indicative of the level a student is interacting with Canvas relative to her classmates <em>up to this point in the quarter</em>. Any number above or below zero indicates a student has greater or less than average activity, respectively. If a student is taking more than one course in Canvas, her score is an average across the courses she is taking.<br><br><strong>No Data</strong> indicates Canvas use is not a course requirement.
        </b-popover>
      </template>

      <template v-slot:head(assignment_score)="data">
        {{ data.label }}<a id="assignments_info" href="#" class="rd-info-link" role="button" title="What is the Assignments score?"><span class="sr-only">What is the Assignments Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="assignments_info" triggers="hover focus">
          <template v-slot:title>
            Assignments Score
          </template>
          This score is indicative of how the student is doing relative to her classmates with regards to the status of assignments (e.g. # of missing assignments) <em>up to this point in the quarter</em>. Any number above or below zero indicates a student is doing better or worse than average. If the student is taking more than one course in Canvas, her score is an average across the courses she is taking.<br><br><strong>No Data</strong> indicates Canvas use is not a course requirement.
        </b-popover>
      </template>

      <template v-slot:head(grade_score)="data">
        {{ data.label }}<a id="grades_info" href="#" class="rd-info-link" role="button" title="What is the Grades score?"><span class="sr-only">What is the Grades Score?</span><b-icon icon="info-circle-fill" variant="primary" /></a>
        <b-popover target="grades_info" triggers="hover focus">
          <template v-slot:title>
            Grades Score
          </template>
          This score represents the student’s grade in Canvas relative to her classmates <em>up to this point in the quarter</em>. Any number above or below zero indicates a student has a better or worse grade than the course average. If the student is taking more than one course in Canvas, her grades are averaged across the courses she is taking.<br><br><strong>No Data</strong> indicates Canvas use is not a course requirement.
        </b-popover>
      </template>

      <template v-slot:cell(student_name)="row">
        <span>{{ row.item.student_last_name }}, {{ row.item.student_first_name }}</span>
        <div class="rd-student-meta">
          {{ row.item.netid }}
          <div>
            <small>
              <b-badge variant="light">{{ row.item.class_desc }}</b-badge>
              <b-badge v-if="row.item.is_eop" variant="light">EOP</b-badge>
              <b-badge v-if="row.item.is_international" variant="light">International</b-badge>
              <b-badge v-if="row.item.is_stem" variant="light">Stem</b-badge>
              <b-badge v-if="row.item.is_athlete" variant="light">Athlete</b-badge>
            </small>
          </div>
        </div>
        <div v-if="is_summer" class="rd-student-meta rd-italic">
          {{ row.item.summer_term_string }}
        </div>
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

      <template v-slot:cell(signin_score)="row">
        <span v-if="row.item.signin_score === -99">No data</span>
        <span v-else>{{ row.item.signin_score }}</span>
      </template>

      <template v-slot:cell(priority_score)="row">
        <span v-if="row.item.priority_score === -99 || row.item.priority_score === null" />
        <span v-else class="rd-pred-score">
          <span v-if="row.item.priority_score >= -5 && row.item.priority_score <= -3"><span class="rd-pred-label rd-pred-label-top">Top</span> {{ row.item.priority_score }}</span>
          <span v-else-if="row.item.priority_score > -3 && row.item.priority_score < 3"><span class="rd-pred-label rd-pred-label-medium">Medium</span> {{ row.item.priority_score }}</span>
          <span v-else-if="row.item.priority_score >= 3 && row.item.priority_score <= 5"><span class="rd-pred-label rd-pred-label-bottom">Bottom</span> {{ row.item.priority_score }}</span>
          <span v-else />
        </span>
      </template>

      <template v-slot:table-busy>
        <div class="text-center text-info">
          <b-spinner class="align-middle" />
          <strong>Loading...</strong>
        </div>
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      align="right"
      class="pagination-sm"
      :total-rows="rowCount"
      :per-page="perPage"
      first-number
      last-number
    />
  </b-container>
</template>
<script>
  import Filters from "./Filters.vue";
  import Vuex from 'vuex';
  import axios from 'axios';
  import qs from 'qs';


  export default {
    name: "DataView",
    components: {
      filters: Filters
    },
    data: function() {
      return {
        standard_fields: [
          {
            key: 'student_name',
            label: "Student Name",
            sortable: true
          },
          {
            key: 'student_number',
            label: "Student Number",
          },
          {
            key: 'priority_score',
            label: 'Priority',
            sortable: true
          },
          {
            key: 'signin_score',
            label: 'Sign-Ins',
            sortable: true
          },
          {
            key: 'activity_score',
            label: 'Activity',
            sortable: true
          },
          {
            key: 'assignment_score',
            label: 'Assignments',
            sortable: true
          },
          {
            key: 'grade_score',
            label: 'Grades',
            sortable: true
          },
          {
            key: 'advisor_name',
            label: 'Adviser',
            sortable: true
          }
        ],
        items: [],
        isBusy: false,
        isDownloading: false,
        perPage: 50,
        currentPage: 1,
        rowCount: 0,
        selected: {},
        low_min: -5,
        low_max: -3,
        average_min: -2.999999999999999,
        average_max: 2.999999999999999,
        high_min: 3,
        high_max: 5,
        request_id: 0,
        is_summer: false,
        download: {
          fields: [
            "student_last_name",
            "student_first_name",
            "student_number",
            "netid",
            "advisor_name",
            "advisor_netid",
            "activity_score",
            "assignment_score",
            "grade_score",
            "signin_score",
            "priority_score",
            "summer_term_string",
            "is_stem",
            "is_premajor",
            "is_iss",
            "is_eop",
            "is_international",
            "is_athlete",
            "campus_code",
            "class_desc"
          ],
        }
      };
    },
    computed: {
      fields (){
        var fields;
        if (this.current_file === "Athletics"){
          fields = this.standard_fields.filter(
            item => !(item.key == "advisor_name"));
        } else if (this.current_file == "Premajor" ||
          this.current_file == "International" ||
          this.current_file == "ISS" ||
          this.current_file == "Tacoma") {
          fields = this.standard_fields.filter(
            item => !(item.key == "priority_score") &&
              !(item.key == "advisor_name"));
        } else {
          fields = this.standard_fields;
        }
        if (!this.is_summer) {
          fields = fields.filter(
            item => !(item.key == "summer_term_string"));
        }
        return fields;
      },
      download_fields () {
        if(this.is_summer){
          return this.download.fields;
        } else {
          return this.download.fields.filter(
            item => !(item.key == "summer_term_string"));
        }
      },
      filename (){
        return this.$store.state.current_file;
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
        if(this.stem_filter === true){
          params['stem_filter'] = this.stem_filter;
        }
        if(this.freshman_filter === true){
          params['freshman_filter'] = this.freshman_filter;
        }
        if(this.keyword_filter.length > 0){
          params['text_filter'] = this.keyword_filter;
        }
        if(this.advisor_filter.length > 0){
          params['advisor_filter'] = this.advisor_filter;
        }
        if(this.summer_filter.length > 0){
          params['summer_filters'] = this.summer_filter;
        }
        if(this.signins_filter.length > 0){
          params['signins_filters'] = this.signins_filter;
        }
        if(this.class_standing_filter){
          params['class_standing_filter'] = this.class_standing_filter;
        }
        if(this.sport_filter){
          params['sport_filter'] = this.sport_filter;
        }
        params['current_page'] = this.currentPage;
        params['per_page'] = this.perPage;
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
        stem_filter: state => state.filters.filters.stem_filter,
        freshman_filter: state => state.filters.filters.freshman_filter,
        keyword_filter: state => state.filters.filters.keyword_filter,
        advisor_filter: state => state.filters.filters.advisor_filter,
        summer_filter: state => state.filters.filters.summer_filter,
        signins_filter: state => state.filters.filters.signins_filter,
        class_standing_filter: state =>
          state.filters.filters.class_standing_filter,
        sport_filter: state => state.filters.filters.sport_filter
      })
    },
    watch: {
      filter_params: function () {
        if (this.current_file && this.current_week)
          this.get_page();
      },
    },
    methods: {
      customSorting(a, b, key) {
        if (key === 'student_name') {
          let a_name = a.student_last_name + ", " + a.student_first_name;
          let b_name = b.student_last_name + ", " + b.student_first_name;
          return a_name < b_name ? -1 : a_name > b_name ? 1 : 0;
        } else {
          return a[key] < b[key] ? -1 : a[key] > b[key] ? 1 : 0;
        }
      },
      get_filtered_emails(){
        var emails = [];
        this.items.forEach(function(item){
          emails.push(item['netid'] + "@uw.edu");
        });
        return emails;
      },
      format_data(rows) {
        var vue = this;
        rows.forEach(function(item){
          item["student_number"] = Number(item["student_number"]);
          item['priority_score'] = vue.get_rounded(item['priority_score']);
          item['signin_score'] = vue.get_rounded(item['signin_score']);
          item['activity_score'] = vue.get_rounded(item['activity_score']);
          item['assignment_score'] = vue.get_rounded(item['assignment_score']);
          item['grade_score'] = vue.get_rounded(item['grade_score']);
        });
        return rows;
      },
      download_data(downloadParams) {
        return axios({
          method: 'get',
          url: "/api/v1/filtered_data/",
          paramsSerializer: function (params) {
            return qs.stringify(params, {arrayFormat: 'repeat'});
          },
          params: downloadParams,
        });
      },
      get_page(){
        var vue = this;
        this.isBusy = true;
        this.download_data(this.filter_params).then(function(response){
          vue.isBusy = false;
          vue.is_summer = response.data.is_summer;
          vue.rowCount = response.data.count;
          vue.items = vue.format_data(response.data.rows);
        }).catch(() => {
          vue.isBusy = false;
        });
      },
      get_csv_file() {
        var vue = this;
        // remove pagination to download all data
        let csv_filter_params = this.filter_params;
        delete csv_filter_params['per_page'];
        delete csv_filter_params['current_page'];

        var hiddenElement = document.createElement('a'),
            timestamp = Math.round(Date.now()/1000),
            csv_string = "";

        // Header
        var fields = this.download_fields;
        csv_string += fields.join(",");
        csv_string += "\n";

        // Data
        this.isDownloading = true;
        this.download_data(csv_filter_params).then(function(response){
          vue.format_data(response.data.rows).forEach(function(item){
            var row_string = "";
            fields.forEach(function(field){
              if (item[field] === null || item[field] === -99 ) {
                row_string += "NA,";
              } else if (field === "summer_term_string") {
                var term_string = item[field].replace(/ /g,'');
                term_string = term_string.replace(/,/g,'-');
                row_string += term_string + ",";
              } else {
                row_string += JSON.stringify(item[field]) + ",";
              }
            });
            //remove trailing comma
            csv_string += row_string.slice(0, -1) + "\n";
            vue.isDownloading = false;
          });
          hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv_string);
          hiddenElement.target = '_blank';
          hiddenElement.download = 'rentention_export_'+timestamp+'.csv';
          hiddenElement.click();
        }).catch(() => {
          vue.isDownloading = false;
        });
      },
      get_rounded(num_string){
        if (num_string === null) {
          return -99;
        }
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
    background-color: $grey-light-bkgnd;
    line-height: 2;
    margin-bottom: 2rem;
    padding: 0.5rem 0;

    .col {
      text-align: center;
    }
  }

  /* Generic Styles */
  .rd-italic {
    font-style: italic;
  }

  /* Top banner styles */

  .rd-info-link {
    margin-left: 0.25rem;
  }


  /* Pagination */
  .rd-pagination-container {
    float: right;
  }

  /* main content styles */
  .rd-student-count {
    background-color: $uw-purple;
    border-radius: 4px;
    color: $white-text;
    margin: 0 2px;
    padding: 3px 6px;
  }

  .rd-copy-email {
    display: inline-flex;

    .rd-copy-email-btn {
      padding-left: 1rem;
    }

    .rd-copy-email-desc {
      padding-top: 0.5rem;
    }
  }

  .rd-table-container {
    margin-top: 2rem;
  }

  .table td {
    vertical-align: middle;
  }

  .rd-student-meta {
    font-size: 90%;
  }

  /* Loading message */
  .b-table[aria-busy='true'] .b-table-busy-slot .text-info {
    padding: 3rem 0;
  }

  .spinner-border,
  .b-table-busy-slot .text-info,
  .aat-processing-text {
    color: $uw-purple !important;
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

  @media only screen and (max-width: 768px) {
    /* Pagination */
    .rd-pagination-container {
      clear: both;
    }
  }
</style>
