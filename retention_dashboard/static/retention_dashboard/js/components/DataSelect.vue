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
            :options="weeks"
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
        type: '',
        currentweek: ''
      };
    },
    computed: {
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
      },
      weeks: function(){
        this.currentweek = this.weeks[this.weeks.length-1].value;
      },
      auth_list: function(){
        this.type = this.auth_list[0];
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
      }
    }
  };
</script>

<style lang="scss">
  @import '../../css/_variables.scss';
  /* main content styles */

  .rd-file-select {
    float: left;
  }

  /* date select  */
  .rd-date-select {
    float: left;
    margin-right: 0.5rem;
  }

  @media only screen and (max-width: 768px) {
    /* small screen date picker*/
    .rd-date-select {
      margin: 0 0 0.5rem 0.5rem;
    }
  }
</style>
