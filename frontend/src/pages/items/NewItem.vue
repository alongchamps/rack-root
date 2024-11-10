<script setup>
  import { useDate } from 'vuetify'

  // const purchaseDate = useDateFormat(purchaseDate, 'YYYYMMDD')
  // const warrantyExpiration = useDateFormat(warrantyExpiration, 'YYYYMMDD')
</script>

<script>
  export default {
    data() {
      return {
        form: {
          name: null,
          description: null,
          deviceTypeId: null,
          serialNumber: null,
          purchaseDate: null,
          warrantyExpiration: null,
          notes: null
        },
        deviceTypes: []
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
      async getDeviceTypes() {
        const res = await fetch("http://localhost:8000/deviceTypes/");
        const finalDeviceTypes = await res.json();
        this.deviceTypes = finalDeviceTypes
      }
    },
    mounted() {
      this.getDeviceTypes();
    }
  }
</script>

<template>
  <navigation />
  <v-btn class="ma-6" prepend-icon="mdi-arrow-left" color="yellow" :to="{ name: 'AllItems' }">Back to all items</v-btn>
  <v-form @submit.prevent="createNewInventoryItem()">
    <v-container>
      <v-row>
        <!-- <v-col class="col-4"> -->
        <v-col cols="4">
          <v-text-field v-model="form.name" label="Device Name"></v-text-field>
          <!-- <v-text-field v-model="form.name" label="Device Name" clearable></v-text-field> -->
        </v-col>
        <v-col cols="4"> <!-- <v-col class="col-4" > -->
          <v-text-field v-model="form.serialNumber" label="Serial Number"></v-text-field>
          <!-- <v-text-field v-model="form.serialNumber" label="Serial Number" clearable></v-text-field> -->
        </v-col>
        <v-col cols="4">
          <v-textarea v-model="form.description" label="Description" rows=2></v-textarea>
          <!-- <v-textarea v-model="form.description" label="Description" rows=2 clearable></v-textarea> -->
        </v-col>
      <!-- </v-row>
      <v-row> -->
        <v-col cols="4"> 
          <v-select
            v-model="form.deviceTypeId"
            label="Device Type"
            :items="deviceTypes"
            item-title="name"
            item-value="id"
            clearable
          ></v-select>
        </v-col>
        <v-col cols="4">
          <v-textarea v-model="form.notes" label="Notes" rows=2></v-textarea>
        </v-col>
        <v-col cols="4">
        </v-col>
      </v-row>
      <v-row>
        <v-col class="col-4">
          <v-date-picker v-model="form.purchaseDate" show-adjacent-months header="Purchase date"></v-date-picker>
        </v-col>
        <v-col class="col-4">
          <v-date-picker v-model="form.warrantyExpiration" show-adjacent-months header="Warranty Expiration"></v-date-picker>
        </v-col>
        <v-col class="col-4">
        </v-col>
      </v-row>
    </v-container>
    <v-btn class="ma-6" prepend-icon="mdi-plus" color="green" type="Submit">Create New Item</v-btn>
  </v-form>
</template>


<!-- 
{
  "detail": [
      {
          "type": "date_from_datetime_inexact",
          "loc": [
              "body",
              "purchaseDate"
          ],
          "msg": "Datetimes provided to dates should have zero time - e.g. be exact dates",
          "input": "2024-11-05T05:00:00.000Z"
      },
      {
          "type": "date_from_datetime_inexact",
          "loc": [
              "body",
              "warrantyExpiration"
          ],
          "msg": "Datetimes provided to dates should have zero time - e.g. be exact dates",
          "input": "2024-11-07T05:00:00.000Z"
      }
  ]
}

Input data from the form:

{
    "name": "asdf",
    "description": "asdf",
    "deviceTypeId": 2,
    "serialNumber": "asdf",
    "purchaseDate": "2024-10-08T04:00:00.000Z",
    "warrantyExpiration": "2024-11-07T05:00:00.000Z",
    "notes": null
}

-->
