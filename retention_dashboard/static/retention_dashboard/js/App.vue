<template>
  <b-container fluid>
    <p>App Wrapper</p>
    <main ref="main" aria-labelledby="aat_page_header" class="col aat-main-container">
      <router-view />
    </main>
  </b-container>
</template>

<script>

  const axios = require("axios");
  export default {
    name: "LandingPage",
    components: {
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
