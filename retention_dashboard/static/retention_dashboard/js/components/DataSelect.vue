<template>
  <div>
    <span class="rd-file-select">
      <b-nav pills>
        <b-nav-item-dropdown
          id="file-dropdown"
          :text="current_file"
          toggle-class="nav-link-custom"
          aria-controls="data_table"
        >
          <b-dropdown-item href="#" @click.prevent="selectPage('international-students.csv')">
            International students
          </b-dropdown-item>
          <b-dropdown-item href="#" @click.prevent="selectPage('premajor-students.csv')">
            Premajor Students
          </b-dropdown-item>
          <b-dropdown-item href="#" @click.prevent="selectPage('eop-students.csv')">
            EOP students
          </b-dropdown-item>
        </b-nav-item-dropdown>
      </b-nav>
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
        currentweek: '3',
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
      }
    },
    mounted: function(){
      this.get_weeks();
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
            var weeks = [];
            response.data.forEach(function(week){
              var week_string = week.quarter + " " + week.year + ": Week" + week.number;
              weeks.push({value: week.id, text: week_string});
            });
            vue.weeks = weeks;
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
