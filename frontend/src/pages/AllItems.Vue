<script setup>
    export default {
        data() {
            return {
                items: [],
                headers: [
                    { title: 'ID', value: 'id' },
                    { title: 'Name', value: 'name' },
                    { title: 'Description', value: 'description' },
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
                this.items = finalItems;
            }
        },
        mounted() {
            this.getItems()
        }
    }
</script>

<template>
    <navigation />
    <v-data-table :items="items" :headers="headers" item-key="id"></v-data-table>
    <!-- <v-btn @click="newItem()">New Item</v-btn> -->
    <!-- <v-btn class="ma-6" :to="{ name: 'NewItem' }">New Item</v-btn> -->
</template>



<!-- <script setup>
  import { useRoute } from "vue-router/auto"
  const route = useRoute("/items")
  
  export default {
    data() {
      return {
        items: [],
        headers: [
          { title: 'ID', value: 'id' },
          { title: 'Name', value: 'name' },
          { title: 'Description', value: 'description' },
          { title: 'itemType', value: 'itemType' },
          { title: 'serialNumber', value: 'serialNumber' },
          { title: 'purchaseDate', value: 'purchaseDate' },
          { title: 'warrantyExpiration', value: 'warrantyExpiration' },
          { title: 'operatingSystem', value: 'operatingSystem' },
          { title: 'notes', value: 'notes' },
        ]
      }
    },
    methods: {
      async getItems() {
        const res = await fetch("http://localhost:8000/items/")
        const finalItems = await res.json()
        this.items = finalItems;
      },
      async goToItem(click, row) {
        this.$router.push('/items/' + row.item.id)
      },
      async deleteItem(id) {
        fetch('http://localhost:8000/items/' + id, {
          method: 'DELETE'
        })
        this.items = this.getItems()
      }
    },
    mounted() {
      this.getItems()
    }
  }
</script> -->