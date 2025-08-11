<script>
  export default {
    data() {
      return {
        searchResults: "",
        itemSearchResults: [],
        itemSearchResultsHeaders: [
          { title: 'ID', value: 'id' },
          { title: 'Name', value: 'name' },
          { title: 'Description', value: 'description' },
          { title: 'Device Type Name', value: 'deviceType.name' },
          { title: 'Serial Number', value: 'serialNumber' },
        ],
        networkSearchResults: [],
        dhcpRangeSearchResults: []
        // I'm probably also going to need headers for each of these
      };
    },
    methods: {
      async getSearchResults(searchParam) {
        this.searchResults = searchParam
        // item search API call
        this.getItemSearchResults()

        // network search API call

        // dhcp range search API call

      },
      async getItemSearchResults() {
        const res = await fetch("http://localhost:8000/search/items/" + this.$route.query.q);
        const itemsMatchingQuery = await res.json();
        this.itemSearchResults = itemsMatchingQuery
      },
      async goToItem(click, row) {
        this.$router.push('/items/' + row.item.id)
      }
      // , dont think this function getDeviceTypeName is needed...
      // async getDeviceTypeName(id) {
      //   const res = await fetch("http://localhost:8000/deviceTypes/" + id );
      // }
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

    <v-data-table :items="itemSearchResults" :headers="itemSearchResultsHeaders" item-key="id" @click:row=goToItem>
    </v-data-table>

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
