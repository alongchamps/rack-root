<script>
  export default {
    data() {
      return {
        items: [],
        headers: [
          { title: 'ID', value: 'id' },
          { title: 'Name', value: 'name' },
          { title: 'description', value: 'description' },
          { title: 'itemType', value: 'itemType' },
          { title: 'serialNumber', value: 'serialNumber' },
          { title: 'purchaseDate', value: 'purchaseDate' },
          { title: 'warrantyExpiration', value: 'warrantyExpiration' },
          { title: 'operatingSystem', value: 'operatingSystem' },
          { title: 'notes', value: 'notes' }
        ]
      }
    },
    methods: {
      async getItems() {
        const res = await fetch("http://localhost:8000/items/");
        const finalItems = await res.json();
        this.items = finalItems
      },
      async goToItem(click, row) {
        this.$router.push('/item/' + row.item.id)
      }
    },
    mounted() {
      this.getItems();
    }
  }
</script>

<template>
    <navigation />
    <h1>Welcome to the all items page</h1>
    <v-data-table :items="items" :headers="headers" item-key="id" @click:row=goToItem></v-data-table>
</template>
