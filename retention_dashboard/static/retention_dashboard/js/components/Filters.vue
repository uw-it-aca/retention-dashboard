<template>
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
</template>

<script>

  import {_} from "vue-underscore";
  export default {
    name: "Filters",
    components: {},
    props: {},
    data(){
      return {
        activity_filter: [],
        assignment_filter: [],
        grade_filter: [],
        premajor_filter: false,
        keyword_filter: "",
      };
    },
    computed: {
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
      premajor_filter: function () {
        this.$store.dispatch('filters/set_premajor_filter', this.premajor_filter);
      },
      keyword_filter: function () {
        this.debouncedKeywordFilters();
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
    padding: 0 15px 1rem;

    fieldset {
      border: 1px $grey-border solid;
      border-style: none solid none none;
      float: left;
      margin: 0 2rem 0 0;
      padding: 0 2rem 0 0;
    }

    .rd-grades-filters {
      border-style: none;
      margin: 0;
      padding: 0;
    }

    .rd-major-filters {
      border: 1px $grey-border solid;
      border-style: none none none solid;
      float: left;
      margin: 0 0 0 2rem;
      padding: 0 0 0 2rem;
    }

    fieldset .rd-keyword-filter {
      border-style: none;
      margin-right: 0;
      margin-top: 0.5rem;
      padding-right: 0;
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

  @media only screen and (max-width: 558px) {
    /* small screen filter styles */

    .rd-filters-container {
      fieldset {
        border-style: none;
        margin: 0;
        padding: 0;
        width: 130px;
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
    }

    .rd-filter-group-bottom {
      margin-top: 2rem;
    }

    .rd-form-note {
      padding-top: 1rem;
    }

  }
</style>