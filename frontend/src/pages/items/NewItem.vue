<script setup>
  import { useDate } from 'vuetify'

  // const purchaseDate = useDateFormat(purchaseDate, 'YYYY-MM-DD')
  // const warrantyExpiration = useDateFormat(warrantyExpiration, 'YYYY-MM-DD')
</script>

<script>
  export default {
    data() {
      return {
        form: {
          name: null,
          description: null,
          // deviceTypeId: null,
          serialNumber: null,
          purchaseDate: null,
          warrantyExpiration: null,
          notes: null
        }
      }
    },
    methods: {
      async createNewInventoryItem() {
        // send data to the backend
        const res = await fetch('http://localhost:8000/items/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        })
        const newItem = await res.json()
        this.$router.push('/items/' + newItem.id)
      },
      async formatToMmmmDdYy( inputDate ) {
        return inputDate
      }
    }
  }
</script>

<template>
  <navigation />
  <v-btn class="ma-6" prepend-icon="mdi-arrow-left" color="yellow" :to="{ name: 'AllItems' }">Back to all items</v-btn>

  <v-container class="d-flex justify-center py-10 h-auto">
    <v-card :width="1000">
      <v-card title="New Inventory Item">
        <v-form @submit.prevent="createNewInventoryItem()">
          <v-text-field v-model="form.name" label="Device Name"></v-text-field>
          <v-text-field v-model="form.description" label="Description"></v-text-field>
          <v-text-field v-model="form.deviceTypeId" label="deviceTypeId"></v-text-field>
          <v-text-field v-model="form.serialNumber" label="Serial Number"></v-text-field>
          <v-date-picker v-model="form.purchaseDate" show-adjacent-months :format-data="formatToMmmmDdYy"></v-date-picker>
          <v-date-picker v-model="form.warrantyExpiration" show-adjacent-months :format-data="formatToMmmmDdYy"></v-date-picker>
          <v-textarea v-model="form.notes" label="Notes"></v-textarea>
          <v-btn class="ma-6" prepend-icon="mdi-content-save-outline" color="green" type="submit">Create Item</v-btn>
        </v-form>
      </v-card>
    </v-card>
  </v-container>
</template>
