<script>
  export default {
    data() {
      return {
        items: [],
        headers: [
          { title: 'ID', value: 'id' },
          { title: 'Name', value: 'name' },
          { title: 'Description', value: 'description' },
          // { title: 'Device Type', value: 'deviceTypeId' },
          { title: 'Device Type Name', value: 'deviceType.name' },
          { title: 'Serial Number', value: 'serialNumber' },
          { title: 'Purchase Date', value: 'purchaseDate' },
          { title: 'Warranty Expiration', value: 'warrantyExpiration' },
          { title: 'Notes', value: 'notes' }
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
      },
      async getDeviceTypeName( id ) {
        const res = await fetch("http://localhost:8000/deviceTypes/" + id );
        
      }
    },
    mounted() {
      this.getItems();
    }
  }
</script>

<template>
    <navigation />
    <v-data-table :items="items" :headers="headers" item-key="id" @click:row=goToItem>
    </v-data-table>
    <v-btn class="ma-6" prepend-icon="mdi-plus" color="green" :to="{ name: 'NewItem' }">New Item</v-btn>
</template>
