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
      }
    },
    mounted() {
      this.getSingleItem(this.$route.params.id)
    }
  }
</script>

<template>
  <navigation />
  <h1>Welcome to the single item page - ID: {{ item.id }}</h1>
  <v-card class="mx-auto" max-width="500">
    <v-card-text>
      <p class="text-h4 font-weight-black">Name: {{ item.name }}</p>
      <p>Description: {{ item.description }}</p>
      <p>Type: {{ item.itemType }}</p>
      <p>Serial: {{ item.serialNumber }}</p>
      <p>OS: {{ item.operatingSystem }}</p>
      <p>Notes: {{ item.notes }}</p>
      <p>Purchase Date: {{ item.purchaseDate }}</p>
      <p>Warranty Expiration: {{ item.warrantyExpiration }}</p>
    </v-card-text>
  </v-card>
</template>
