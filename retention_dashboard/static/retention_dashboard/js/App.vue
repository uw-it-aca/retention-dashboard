<template>
  <b-container id="app" class="rd-content-container" fluid>
    <b-row class="rd-app-banner" role="banner">
      <b-col class="col-10 col-md-8">
        <h1 class="rd-app-title sr-only">
          <span>Retention Analytics Dashboard</span>
        </h1>
        <a href="/" class="nav-link p-0 rd-action-link"><img src="/static/retention_dashboard/img/RAD-logo.png" alt="RAD Logo" class="rd-logo" /></a>
      </b-col>
      <b-col class="rd-login-info col-2 col-md-4">
        <h3 id="rd_login_header" class="sr-only">
          Your information
        </h3>
        <span aria-labelledby="rd_login_header" class="hide-lg"><b-icon icon="person-circle" /></span><span id="netid"> {{ netid }}</span>
        <a href="/saml/logout" tabindex="0" class="rd-logout-link">Sign Out</a>
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
        <div>© 2021 University of Washington  |  Seattle, WA</div>
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
      return {
        netid: '',
      };
    },
    computed: {},
    watch: {
      $route(){ },
    },
    mounted() {
      this.netid = window.user_netid;
    },
    methods: {}
  };
</script>

<style lang="scss">
  // import base.scss which inherits the custom theme
  @import '../css/base.scss';

  /* Structure */

  .rd-content-container {
    background-color: $app-bkgnd;
    overflow: hidden;
  }

  /* override styles */

  .rd-action-link {
    font-weight: bold;
    white-space: nowrap;
  }

  .rd-vis-hidden {
    visibility: hidden;
  }

  /* Top banner styles */
  .rd-app-banner {
    background-color: $uw-purple;
    /*background-image: url('/static/retention_dashboard/img/uw-logo-white.png');
    background-position: left 18px;
    background-repeat: no-repeat;
    background-size: 60px;*/
    color: $white-text;
    min-height: 60px;
    padding: 0.5rem 0;

    a {
      color: $uw-metallic;
    }

    a:focus,
    a:hover {
      color: $white-text;
      text-decoration: underline;
    }
  }

  .rd-app-title {
    font-size: 2rem;
    margin-bottom: 0;
    padding-left: 55px;
    padding-top: 12px;
  }

  .rd-login-info {
    text-align: right;
    padding-top: 0.5rem;
  }

  /* branding styles */
  .rd-page-header {
    font-size: 2rem;
    padding: 1.5rem 0;
  }

  .rd-logo {
    width:250px;
  }

  /* footer styles */

  .rd-footer {
    background-color: $uw-purple;
    border-top: 3px solid $banner-border;
    color: $white-text;
    font-size: 0.75rem;
    min-height: 100px;
    min-width: 100%;
    padding: 1.5rem 0;
    text-align: center;

    a {
      color: $white-text;
      text-decoration: underline;
    }

    a:hover,
    a:focus {
      color: $uw-metallic;
    }
  }

  .rd-footer-wordmark {
    background: url('/static/retention_dashboard/img/uw-sprite.svg') no-repeat 0 -434px transparent;
    display: inline-block;
    margin-bottom: 1rem;
    min-height: 16px;
    overflow: hidden;
    text-indent: -9999px;
    width: 335px;
  }

  .rd-footer-links {
    font-size: 0.8725rem;
    padding: 0.5rem 0;
  }

  .rd-logout-link {
    display: block;
    font-size: 0.75rem;
  }

</style>
