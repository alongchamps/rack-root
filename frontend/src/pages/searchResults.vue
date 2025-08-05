<script>
  export default {
    data() {
      return {
        itemSearchResults: [],
        networkSearchResults: [],
        dhcpRangeSearchResults: []
        // I'm probably also going to need headers for each of these
      };
    },
    methods: {
      async getSearchResults(searchParam) {
        // item search API call

        // network search API call

        // dhcp range search API call


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
    <br />
    You searched for: <b>{{ this.searchResults }}</b>
    
    <!-- All of these tables will show up IFF they have results -->
    <!-- 
      if length itemSearchResults > 0:
        item results table
    -->

    <!-- 
      if length networkSearchResults > 0:
        network results table
    -->

    <!--
      if length dhcpRangeSearchResults > 0:
        dhcp range results table
    -->

  </v-container>

</template>
