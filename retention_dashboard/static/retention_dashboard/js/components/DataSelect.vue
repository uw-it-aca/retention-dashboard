<template>
<b-col cols="5" md="9">
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
  <span>
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
          class="rd-date-select"
          :options="weeks"
          aria-controls="data_table"
          size="sm"
        />
      </b-form-group>
    </b-form>
  </span>
</b-col>
</template>

<script>

  import Vuex from 'vuex';
  export default {
    name: "DataSelect",
    components: {},
    props: {},
    data(){
      return {
        weeks: [1, 2],
        currentweek: 1
      };
    },
    computed: {
      ...Vuex.mapState({
        current_week: state => state.dataselect.current_week,
        current_file: state => state.dataselect.current_file
      })
    },
    watch: {},
    methods: {
      selectPage(page){
        this.$store.dispatch('dataselect/set_file', page);
      }
    },
  };
</script>

<style lang="scss">

    /* date select  */
    .rd-date-select {
    float: left;
    margin-right: 0.5rem;
    }

    /* main content styles */

    .rd-file-select {
    float:left;
    }


    @media only screen and (max-width: 768px) {
    /* small screen date picker*/
    .rd-date-select {
        margin: 0 0 0.5rem 0.5rem;
    }

    }
</style>
