<template>
  <div>
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
    <span class="rd-summer-term-select">
      <b-dropdown id="dropdown-form" class="rd-select-dropdown" :text="summerterm + ' Term'" ref="dropdown" size="sm">
        <b-dropdown-form>
            <b-form-checkbox-group
              v-model="summerterm"
              :options="summer_terms"
              stacked
            ></b-form-checkbox-group>

            <!-- checkboxes (devights created in filters) 

            <b-form-group v-if="is_summer">
              <b-form-checkbox-group id="summer_filters" v-model="summer_filter" stacked>
                  <b-form-checkbox value="a">
                    A
                  </b-form-checkbox>
                  <b-form-checkbox value="b">
                    B
                  </b-form-checkbox>
                  <b-form-checkbox value="full">
                    Full
                  </b-form-checkbox>
                </b-form-checkbox-group>
            </b-form-group>

            -->

        </b-dropdown-form>
      </b-dropdown>
    </span>
  </div>
</template>

<script>

  import Vuex from 'vuex';
  import axios from 'axios';
  export default {
    name: "DataSelect",
    components: {},
    props: {},
    data(){
      return {
        weeks: [],
        auth_list: [],
        advisors: [],
        type: '',
        currentweek: '',
        summerterm: ['a', 'b', 'full'],
        summer_terms: [
          { value: 'a', text: 'A Term' },
          { value: 'b', text: 'B Term' },
          { value: 'full', text: 'Full Term' }
        ],
      };
    },
    computed: {
      sorted_weeks () {
        var sorted = this.weeks;
        if(sorted.length > 0){
          sorted.sort((a, b) => (a.value > b.value) ? 1 : -1);
        }
        return sorted;
      },
      ...Vuex.mapState({
        current_file: state => state.dataselect.current_file,
        current_week: state => state.dataselect.current_week
      })
    },
    watch: {
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
    mounted: function(){
      this.get_weeks();
      this.get_types();
    },
    methods: {
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

  .rd-file-select,.rd-date-select {
    float: left;
    margin-right: 0.5rem;
  }

  /* summer term select  */
  .rd-summer-term-select {
    float: left;
  }

  .rd-select-dropdown button, .rd-select-dropdown button:hover, .rd-select-dropdown button:focus, .rd-select-dropdown.show button.btn-secondary.dropdown-toggle {
    background-color: white;
    color: #495057;
    border-color: #ced4da;
  }

  @media only screen and (max-width: 768px) {
    /* small screen date picker*/
    .rd-file-select {
      margin-bottom: 0.5rem;
    }

    .rd-date-select {
      margin: 0 0 1rem;
    }

    .rd-file-select .form-group,
    .rd-date-select .form-group {
      margin-bottom: 0;
    }
  }
</style>
