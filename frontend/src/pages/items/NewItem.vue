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
  
  <div class="d-flex justify-center">
    <v-card class="align-center justify-center" width="50em">
      <v-card-title>
        New Item
      </v-card-title>
      <v-container class="text-center">
        <v-row class="margin">
          <v-form @submit.prevent="createNewInventoryItem()">
            <v-text-field v-model="form.name" label="Device Name" variant="outlined" width="45em" clearable></v-text-field>
            <v-text-field v-model="form.serialNumber" label="Serial Number" variant="outlined" width="45em" clearable></v-text-field>
            <v-select
              v-model="form.deviceTypeId"
              :items="deviceTypes"
              item-title="name"
              item-value="id"
              label="Device Type / Model"
              variant="outlined"
              width="45em"
              clearable
            ></v-select>
            <v-textarea v-model="form.description" label="Description" variant="outlined" width="45em" rows=2 clearable></v-textarea>
            <v-textarea v-model="form.notes" label="Notes" variant="outlined" width="45em" rows=2 clearable></v-textarea>
            <v-container class="d-flex">
              <v-date-picker color="blue" class="margin-smaller" v-model="form.purchaseDate" show-adjacent-months header="Purchase date"></v-date-picker>
              <v-date-picker color="blue" class="margin-smaller" v-model="form.warrantyExpiration" show-adjacent-months header="Warranty Expiration"></v-date-picker>
            </v-container>
            <v-checkbox label="Is on the network (placeholder)"></v-checkbox>
            <v-btn class="a-submit-1" prepend-icon="mdi-plus" color="green" type="Submit">Create New Item</v-btn>
          </v-form>
        </v-row>
        <v-row class="text-center">
          <v-card-actions>
            <v-btn class="a-submit-2" prepend-icon="mdi-arrow-left" color="yellow" :to="{ name: 'AllItems' }">Back to all items</v-btn>
          </v-card-actions>
        </v-row>
      </v-container>
    </v-card>
  </div>

  <!-- <v-form @submit.prevent="createNewInventoryItem()">
    <v-container>
      <v-row>
        <v-col cols="4">
          <v-text-field v-model="form.name" label="Device Name" variant="outlined"></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-text-field v-model="form.serialNumber" label="Serial Number" variant="outlined"></v-text-field>
        </v-col>
        <v-col cols="4">
          <v-textarea v-model="form.description" label="Description" variant="outlined" rows=2></v-textarea>
        </v-col>
        <v-col cols="4"> 
          <v-select
            v-model="form.deviceTypeId"
            label="Device Type / Model"
            :items="deviceTypes"
            item-title="name"
            item-value="id"
            variant="outlined"
            clearable
          ></v-select>
        </v-col>
        <v-col cols="4">
          <v-textarea v-model="form.notes" label="Notes" variant="outlined" rows=2></v-textarea>
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
  </v-form> -->
</template>

<!-- more specific styling for components -->
<style>

.a-submit-1 {
    color: white !important;
    background-color: rgb(0, 193, 0) !important;
    margin: 25px;
  }

  .a-submit-2 {
    color: black !important;
    background-color: yellow !important;
    margin: 25px;
  }

.margin {
  margin: 20px;
}

.margin-smaller {
  margin: 10px;
}

</style>
