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
    <v-card-subtitle class="text-h4">Device type: {{ item.description }}</v-card-subtitle>
    <v-divider :thickness="2"></v-divider>
    <v-card-text class="text-h5">Serial Number:</v-card-text>
    <v-divider :thickness="2"></v-divider>
    <v-card-text class="text-h5">Purchase date:</v-card-text>
    <v-divider :thickness="2"></v-divider>
    <v-card-text class="text-h5">Warranty expiration:</v-card-text>
    <v-divider :thickness="2"></v-divider>

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



<!-- <v-card-text>
      <p class="text-h4 font-weight-black">Name: {{ item.name }}</p>
      <p>Description: {{ item.description }}</p>
      <p>Type: {{ item.deviceType }}</p>
      <p>Serial: {{ item.serialNumber }}</p>
      <p>Notes: {{ item.notes }}</p>
      <p>Purchase Date: {{ item.purchaseDate }}</p>
      <p>Warranty Expiration: {{ item.warrantyExpiration }}</p>
    </v-card-text> -->
