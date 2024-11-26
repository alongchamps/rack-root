<script>
  export default {
    data() {
      return {
        form: {
          name: null,
          vlan: null,
          classification: null,
          network: null,
          subnetMaskBits: null
        }
      }
    },
    methods: {
      async createNewNetwork() {
        // send data to the backend
        const res = await fetch('http://localhost:8000/networks/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        })
        const newNetwork = await res.json()
        this.$router.push('/networks/' + newNetwork.id)
      }
    }
  }
</script>

<template>
  <navigation />

  <div class="d-flex justify-center">
    <v-card class="align-center justify-center" width="50em">
      <v-card-title>
        New Network
      </v-card-title>
      <v-container class="text-center">
        <v-row class="margin">
          <v-form @submit.prevent="createNewNetwork()">
            <v-text-field v-model="form.name" label="Network name" variant="outlined" width="45em"></v-text-field>
            <v-text-field v-model="form.vlan" label="VLAN Number" variant="outlined" width="45em"></v-text-field>
            <v-text-field v-model="form.classification" label="Classification" variant="outlined" width="45em"></v-text-field>
            <v-text-field v-model="form.network" label="Network Address (e.g. 192.168.12.0)" variant="outlined" width="45em"></v-text-field>
            <v-text-field v-model="form.subnetMaskBits" label="Subnet Mask bits (e.g. 24)" variant="outlined" width="45em"></v-text-field>
            <v-btn class="a-submit-1" prepend-icon="mdi-plus" color="green" type="Submit">Create New Network</v-btn>
          </v-form>
        </v-row>
      </v-container>
    </v-card>
  </div>
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
