<script>
  export default {
    data() {
      return {
        network: {}
      }
    },
    methods: {
      async getSingleNetwork(id) {
        const res = await fetch("http://localhost:8000/networks/" + id)
        const networkResult = await res.json()

        if( res.status == 404 ) {
          console.error("A network with that ID wasn't found")
          this.$router.push('/404')
        }

        this.network = networkResult;
      }
    },
    mounted() {
      this.getSingleNetwork(this.$route.params.id)
    }
  }

</script>

<template>
  <navigation />
  <v-card class="mx-auto" min-width="400" max-width="700">
    <v-card-title class="text-h2">{{ network.name }}</v-card-title>
    <v-divider :thickness="2">Network classification</v-divider>
    <v-card-text>{{ network.classification }}</v-card-text>
    <v-divider :thickness="2">VLAN</v-divider>
    <v-card-text>{{ network.vlan }}</v-card-text>
    <v-divider :thickness="2">Network</v-divider>
    <v-card-text>{{ network.network }}</v-card-text>
    <v-divider :thickness="2">Subnet Mask Bits</v-divider>
    <v-card-text>{{ network.subnetMaskBits }}</v-card-text>
    <v-divider :thickness="2"></v-divider>
  </v-card>
</template>

<style scoped>
  .infotext {
    font-size: 16px;
  }
</style>
