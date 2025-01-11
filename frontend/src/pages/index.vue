<script>
  export default {
    data() {
      return {
        itemsCount: 0,
        deviceTypesCount: 0,
        networksCount: 0
      }
    },
    methods: {
      async summaryCounts() {
        const itemResults = await fetch("http://localhost:8000/items");
        const items = await itemResults.json();
        this.itemsCount = items.length

        const deviceTypesResult = await fetch("http://localhost:8000/deviceTypes");
        const deviceTypes = await deviceTypesResult.json();
        this.deviceTypesCount = deviceTypes.length

        const networkResult = await fetch("http://localhost:8000/networks");
        const networks = await networkResult.json();
        this.networksCount = networks.length
      }
    },
    mounted() {
      this.summaryCounts();
    }
  }
</script>

<template>
  <navigation />
  
  <!-- first row of content with a summary count dashboard-->
  <v-container>
    <v-layout class="justify-center">
      <v-flex>
        <v-card class="box text-center" color="blue">
          <v-card-title class="text-h2 item">Items</v-card-title>
          <v-card-text class="text-h2 text-center">
            {{ itemsCount }}
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex>
        <v-card class="box text-center" color="green">
          <v-card-title class="text-h2 item">Types</v-card-title>
          <v-card-text class="text-h2 text-center">
            {{ deviceTypesCount }}
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex>
        <v-card class="box text-center" color="red">
          <v-card-title class="text-h2 item">VLANs</v-card-title>
          <v-card-text class="text-h2 text-center">
            {{ networksCount }}
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container>

  <!-- second row of boxes for IPAM summaries, WIP-->

  <!-- <v-container>
    <v-layout class="justify-center">
      <v-flex>
        <v-card class="box text-center" color="blue">
          <v-card-title class="text-h2 item">IPAM Networks</v-card-title>
          <v-card-text class="text-h2 text-center">
            3
          </v-card-text>
        </v-card>
      </v-flex>
      <v-flex>
        <v-card class="box text-center" color="green">
          <v-card-title class="text-h2 item">IPAM Networks 2</v-card-title>
          <v-card-text class="text-h2 text-center">
            4
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </v-container> -->

</template>

<style scoped>
  .item {
    min-height: 50px;
    min-width: 200px;
    margin: 5px;
  }

  .box {
    border: 2px solid;
    margin: 20px;
    border-radius: 10px;
  }
</style>
