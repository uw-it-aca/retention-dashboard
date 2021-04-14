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
        <b-modal id="email-modal" title="Copy E-Mail Addresses" ok-title="Done" ok-only>
          <div class="container rd-copy-email">
            <div>
              <textarea id="email_area" v-model="email_list_text" rows="10" readonly />
            </div>
            <div class="rd-copy-email-btn">
              <b-button variant="info" v-clipboard:copy="email_list_text">
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
        :total-rows="rows"
        :per-page="perPage"
        aria-controls="data_table"
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
      :per-page="perPage"
      :current-page="currentPage"
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

      <template v-slot:cell(is_premajor)="row">
        <span v-if="row.item.is_premajor === true"><b-icon icon="check2-square" scale="1.5" /><span class="sr-only">{{ row.item.is_premajor }}</span></span>
        <span v-else class="sr-only">{{ row.item.is_premajor }}</span>
      </template>

      <template v-slot:cell(priority_score)="row">
        <span v-if="row.item.priority_score === -99" />
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
      :total-rows="rows"
      :per-page="perPage"
      aria-controls="data_table"
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
            key: 'priority_score',
            label: 'Priority',
            sortable: true
          },
          {
            key: 'signin_score',
            label: 'Sign-Ins',
            class: 'text-center',
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
          },
          {
            key: 'advisor_name',
            label: 'Adviser',
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
            key: 'signin_score',
            label: 'Sign-Ins',
            class: 'text-center',
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
        items: [],
        isBusy: false,
        csv_data: "",
        perPage: 200,
        currentPage: 1,
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
            "activity_score",
            "assignment_score",
            "grade_score",
            "is_premajor",
            "is_freshman",
            "is_stem",
            "signin_score"
          ],
          summer_fields: [
            "student_last_name",
            "student_first_name",
            "student_number",
            "netid",
            "activity_score",
            "assignment_score",
            "grade_score",
            "is_premajor",
            "summer_term_string",
            "is_freshman",
            "is_stem",
            "signin_score"
          ],
          fields_eop: [
            "student_last_name",
            "student_first_name",
            "student_number",
            "netid",
            "activity_score",
            "assignment_score",
            "grade_score",
            "priority_score",
            "is_premajor",
            "advisor_name",
            "advisor_netid",
            "is_freshman",
            "is_stem",
            "signin_score"
          ],
          summer_fields_eop: [
            "student_last_name",
            "student_first_name",
            "student_number",
            "netid",
            "activity_score",
            "assignment_score",
            "grade_score",
            "priority_score",
            "is_premajor",
            "advisor_name",
            "advisor_netid",
            "summer_term_string",
            "is_freshman",
            "is_stem",
            "signin_score"
          ]
        }
      };
    },
    computed: {
      fields (){
        var fields;
        if (this.current_file === "EOP"){
          fields = this.eop_fields;
        } else if (this.current_file === "ISS"){
          fields = this.eop_fields.filter(
            item => !(item.key == "is_premajor"));
        } else {
          fields = this.standard_fields;
        }
        return fields;
      },
      download_fields () {
        if (this.current_file === "EOP"){
          if(this.is_summer){
            return this.download.summer_fields_eop;
          } else {
            return this.download.fields_eop;
          }
        } else if (this.current_file === "ISS"){
          if(this.is_summer){
            return this.download.summer_fields_eop.filter(
              item => !(item.key == "is_premajor"));
          } else {
            return this.download.fields_eop.filter(
              item => !(item.key == "is_premajor"));
          }
        } else {
          if(this.is_summer){
            return this.download.summer_fields;
          } else {
            return this.download.fields;
          }
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
        return params;
      },
      filter_trigger () {
        return (
          this.assignment_filter,
          this.grade_filter,
          this.activity_filter,
          this.prediction_filter,
          this.premajor_filter,
          this.stem_filter,
          this.freshman_filter,
          this.keyword_filter,
          this.advisor_filter,
          this.current_week,
          this.current_file,
          this.summer_filter,
          this.signins_filter
        );
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
      filter_trigger: function () {
        this.run_filters();
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
      download_filtered() {
        var to_download = this.items,
            hiddenElement = document.createElement('a'),
            timestamp = Math.round(Date.now()/1000),
            csv_string = "";

        // Header
        var fields = this.download_fields;
        csv_string += fields.join(",");
        csv_string += "\n";
        // Data
        to_download.forEach(function(item){

          var row_string = "";
          fields.forEach(function(field){
            if (item[field] === -99) {
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
        });

        hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(csv_string);
        hiddenElement.target = '_blank';
        hiddenElement.download = 'rentention_export_'+timestamp+'.csv';
        hiddenElement.click();
      },
      run_filters(){
        var vue = this,
            query_token = Date.now();
        this.request_id = query_token;
        if(this.current_file.length < 1 || this.current_week.length < 1){
          // don't fire ajax unless week and type are set
          return;
        }
        this.isBusy = true;

        axios({
          method: 'get',
          url: "/api/v1/filtered_data/",
          paramsSerializer: function (params) {
            return qs.stringify(params, {arrayFormat: 'repeat'});
          },
          params: this.filter_params,
        }).then(function(response){
          if(query_token === vue.request_id){
            vue.isBusy = false;
            vue.csv_data = response.data.rows;
            vue.is_summer = response.data.is_summer;
          }
        }).catch(() => {
          vue.isBusy = false;
          vue.csv_data = [];
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
