<script>
  export default {
    data() {
      return {
        networks: [],
        headers: [
          { title: 'ID', value: 'id'},
          { title: 'Network', value: 'network'},
          { title: 'VLAN', value: 'vlan'},
          { title: 'Subnet Mask Bits', value: 'subnetMaskBits'},
          { title: 'Classification', value: 'classification'}
        ]
      }
    },
    methods: {
      async getNetworks() {
        const res = await fetch("http://localhost:8000/networks/");
        const finalNetworks = await res.json();
        this.networks = finalNetworks;
      },
      async goToNetwork(click, row) {
        this.$router.push('/networks/' + row.item.id)
      }
    },
    mounted() {
      this.getNetworks();
    }
  }

</script>

<template>
    <navigation />
    <v-btn class="ma-6" prepend-icon="mdi-plus" color="green" :to="{ name: 'NewNetwork' }">New Network</v-btn>
    <v-data-table :items="networks" :headers="headers" item-key="id" @click:row=goToNetwork>
    </v-data-table>
</template>
