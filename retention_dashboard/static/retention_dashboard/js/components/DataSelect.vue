<template>
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
</template>

<script>

  import Vuex from 'vuex';
  export default {
    name: "DataSelect",
    components: {},
    props: {},
    data(){
      return {
      };
    },
    computed: {
      ...Vuex.mapState({
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
  /* main content styles */

  .rd-file-select {
  float:left;
  }
</style>
