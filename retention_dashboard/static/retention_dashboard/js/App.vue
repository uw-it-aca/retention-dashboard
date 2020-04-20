<template>
  <b-container fluid>
    <p>App Wrapper</p>
    <main ref="main" aria-labelledby="" class="col">
      <b-col cols="5" md="9">
        <dataselect />
      </b-col>

      <dataview />
    </main>
  </b-container>
</template>

<script>
  import DataSelect from "./components/DataSelect.vue";
  import DataView from "./components/DataView.vue";
  const axios = require("axios");
  export default {
    name: "LandingPage",
    components: {
      dataselect: DataSelect,
      dataview: DataView
    },
    data(){
      return {};
    },
    computed: {},
    watch: {
      $route(){ },
    },
    mounted() {
    },
    methods: {}
  };
</script>

<style lang="scss">
  // import base.scss which inherits the custom theme
  @import '../css/base.scss';

</style>
