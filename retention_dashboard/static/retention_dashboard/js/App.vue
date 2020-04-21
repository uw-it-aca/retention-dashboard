<template>
  <b-container id="app" class="rd-content-container" fluid>
    <b-row class="rd-app-banner" role="banner">
      <b-col>
        <h1 class="rd-app-title"><span>Retention Analytics Dashboard</span></h1>
      </b-col>
    </b-row>
    <b-row role="main">
      <dataview />
    </b-row>
    <b-row>
      <footer class="rd-footer" role="contentinfo">
        <a href="http://www.uw.edu" class="rd-footer-wordmark">University of Washington</a>
        <div class="rd-footer-links">
          <a href="https://www.washington.edu/online/privacy/">Privacy</a> / <a href="https://www.washington.edu/online/terms/">Terms</a> / <a href="mailto:lyle3@uw.edu?subject=Support: Retention Analytics Dashboard">Support</a>
        </div>
        <div>© 2020 University of Washington  |  Seattle, WA</div>
      </footer>
    </b-row>
  </b-container>
</template>

<script>
  import DataView from "./components/DataView.vue";
  export default {
    name: "LandingPage",
    components: {
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
