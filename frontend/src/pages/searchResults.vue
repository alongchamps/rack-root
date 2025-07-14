<script>
  export default {
    data() {
      return {
        searchResults: ''
      };
    },
    methods: {
      async getSearchResults(searchParam) {
        this.searchResults = searchParam
      }
    },
    mounted() {
      this.getSearchResults(this.$route.query.q)
    }
  }  
</script>

<template>
  <navigation />
  
  <v-container>
    <h1>Search results</h1>
    {{ this.searchResults }}
  </v-container>

</template>
