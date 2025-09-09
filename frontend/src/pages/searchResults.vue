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
        networkSearchResultsHeaders: [
          { title: 'ID', value: 'id'},
          { title: 'Name', value: 'name' },
          { title: 'Network', value: 'network'},
          { title: 'VLAN', value: 'vlan'},
          { title: 'Classification', value: 'classification'}
        ],
        dhcpRangeSearchResults: [],
        dhcpRangeSearchResultsHeaders: [
          { title: 'ID', value: 'id'},
          { title: 'Name', value: 'name' },
          { title: 'Description', value: 'description'},
          { title: 'Starting IP', value: 'startIp'},
          { title: 'Ending IP', value: 'endIp'},
        ]
      };
    },
    methods: {
      async getSearchResults(searchParam) {
        this.searchResults = searchParam
        // item search API call
        this.getItemSearchResults()

        // network search API call
        this.getNetworkSearchResults()

        // dhcp range search API call
        this.getDhcpRangeSearchResults()

      },
      async getItemSearchResults() {
        const res = await fetch("http://localhost:8000/search/items/" + this.$route.query.q);
        const itemsMatchingQuery = await res.json();
        this.itemSearchResults = itemsMatchingQuery
      },
      async goToItem(click, row) {
        this.$router.push('/items/' + row.item.id)
      },
      async getNetworkSearchResults() {
        const res = await fetch("http://localhost:8000/search/networks/" + this.$route.query.q);
        const networkMatchingQuery = await res.json();
        this.networkSearchResults = networkMatchingQuery
      },
      async getDhcpRangeSearchResults() {
        const res = await fetch("http://localhost:8000/search/dhcpRanges/" + this.$route.query.q);
        const dhcpSearchMatchingQuery = await res.json();
        this.dhcpRangeSearchResults = dhcpSearchMatchingQuery
      },
      async goToNetwork(click, row) {
        this.$router.push('/networks/' + row.item.id)
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
    
    <!-- TODO All of these tables will show up iff they have results -->
    <!-- 
      if length itemSearchResults > 0:
        item results table
    -->

    <v-data-table :items="itemSearchResults" :headers="itemSearchResultsHeaders" item-key="id" @click:row=goToItem>
    </v-data-table>
  
    <br />
    
    <!-- TODO
      if length networkSearchResults > 0:
        network results table
    -->
    <v-data-table :items="networkSearchResults" :headers="networkSearchResultsHeaders" item-key="id" @click:row=goToNetwork>
    </v-data-table>

    <br />

    <!--TODO
      if length dhcpRangeSearchResults > 0:
        dhcp range results table
    -->

    <!-- The next line is commented out until I have an actual DHCP details page -->
    <!-- <v-data-table :items="dhcpRangeSearchResults" :headers="dhcpRangeSearchResultsHeaders" item-key="id" @click:row=goToDhcpDetailsPage> -->
    <v-data-table :items="dhcpRangeSearchResults" :headers="dhcpRangeSearchResultsHeaders" item-key="id">      
    </v-data-table>

  </v-container>

</template>
