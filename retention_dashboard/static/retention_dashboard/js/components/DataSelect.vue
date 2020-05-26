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
        currentweek: ''
      };
    },
    computed: {
      sorted_weeks () {
        var sorted = this.weeks;
        return sorted.sort((a, b) => (a.value > b.value) ? 1 : -1);
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
        this.$store.dispatch('dataselect/set_week', week);
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

  .rd-file-select {
    float: left;
    margin-right: 0.5rem;
  }

  /* date select  */
  .rd-date-select {
    float: left;
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
