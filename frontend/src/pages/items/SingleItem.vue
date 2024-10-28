<script>
  export default {
    data() {
      return {
        item: {}
      }
    },
    methods: {
      async getSingleItem(id) {
        const res = await fetch("http://localhost:8000/items/" + id)
        const itemResult = await res.json()

        if( res.status == 404 ) {
          console.error("item not found")
          this.$router.push('/404')
        }

        this.item = itemResult;
      },
      async deleteItem() {
        // send a delete request to the backend
        const res = await fetch('http://localhost:8000/items/' + this.$route.params.id, {
          method: 'DELETE',
        })
        // send the user back to the all items page after that
        this.$router.push('/items/')
      },
    },
    mounted() {
      this.getSingleItem(this.$route.params.id)
    }
  }
</script>

<template>
  <navigation />
  <v-card class="mx-auto" min-width="400" max-width="700">
    <v-card-title class="text-h2">{{ item.name }}</v-card-title>
    <v-divider :thickness="2">Device Type</v-divider>
    <v-card-text>{{ item.description }}</v-card-text>
    <v-divider :thickness="2">Serial Number</v-divider>
    <v-card-text>{{ item.serialNumber }}</v-card-text>
    <v-divider :thickness="2">Purchase Date</v-divider>
    <v-card-text>{{ item.purchaseDate }}</v-card-text>
    <v-divider :thickness="2">Warranty Expiration</v-divider>
    <v-card-text>{{ item.warrantyExpiration }}</v-card-text>
    <v-divider :thickness="2"></v-divider>
    <!-- placeholder - add network zone here, if defined -->

    <v-card-actions>
      <v-btn
      class="ma-6" 
      prepend-icon="mdi-delete" 
      color="red" 
      variant="elevated"
      >
      <!-- @click.native="deleteItem()"> -->
      Delete device</v-btn>
    </v-card-actions>
  </v-card>
</template>

<style scoped>
  .infotext {
    font-size: 16px;
  }
</style>



<!-- <v-card-text>
      <p class="text-h4 font-weight-black">Name: {{ item.name }}</p>
      <p>Description: {{ item.description }}</p>
      <p>Type: {{ item.deviceType }}</p>
      <p>Serial: {{ item.serialNumber }}</p>
      <p>Notes: {{ item.notes }}</p>
      <p>Purchase Date: {{ item.purchaseDate }}</p>
      <p>Warranty Expiration: {{ item.warrantyExpiration }}</p>
    </v-card-text> -->
