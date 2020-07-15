<template>
  <b-form-group
    :label="filterName"
  >
    <b-form-checkbox-group :id="filterName.toLowerCase() + '_filters'" v-model="filter_values" stacked>
      <b-form-checkbox value="high">
        High
      </b-form-checkbox>
      <b-form-checkbox value="avg">
        Average
      </b-form-checkbox>
      <b-form-checkbox value="low">
        Low
      </b-form-checkbox>
    </b-form-checkbox-group>
  </b-form-group>
</template>
<script>
  export default {
    name: "RangeFilter",
    props: {
      filterName: {
        type: String,
        default: "RangeFilter"
      },
      filterStore: {
        type: String,
        default: ""
      },
    },
    data: function() {
      return {
        filter_values: []
      };
    },
    computed: {
    },
    watch: {
      filter_values: function (){
        this.$store.dispatch(this.filterStore, this.filter_values);
      }

    },
    methods: {
    }
  };
</script>

<style lang="scss">
</style>
