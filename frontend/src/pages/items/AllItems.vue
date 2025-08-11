<!-- <template>
  <v-data-table :headers="headers" :items="logs">
     <template #item.createdOn="{ item }">
        {{ date.format(item.createdOn, 'fullDateTime24h') }}
     </template>
  </v-data-table>
</template>
 -->


<script setup>
  import { useDate } from 'vuetify';
  const date = useDate()
</script>

<script>
  export default {
    data() {
      return {
        items: [],
        headers: [
          { title: 'ID', value: 'id' },
          { title: 'Name', value: 'name' },
          { title: 'Description', value: 'description' },
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
        this.$router.push('/items/' + row.item.id)
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
    <v-btn class="ma-6" prepend-icon="mdi-plus" color="green" :to="{ name: 'NewItem' }">New Item</v-btn>
    <v-data-table :items="items" :headers="headers" item-key="id" @click:row=goToItem>
      <template #item.purchaseDate="{ item }">
        {{ date.format(item.purchaseDate, 'fullDate') }}
      </template>
      <template #item.warrantyExpiration="{ item }">
        {{ date.format(item.warrantyExpiration, 'fullDate') }}
      </template>
    </v-data-table>
</template>
