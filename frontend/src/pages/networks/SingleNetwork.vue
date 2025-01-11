<script>
  export default {
    data() {
      return {
        form: {
          gateway: ''
        },
        network: {},
        newGatewayDialog: false,
        invalidGatewayInput: false
      }
    },
    methods: {
      async getSingleNetwork(id) {
        const res = await fetch("http://localhost:8000/networks/" + id)
        const networkResult = await res.json()

        if (res.status == 404) {
          console.error("A network with that ID wasn't found")
          this.$router.push('/404')
        }

        this.network = networkResult;

        this.form.gateway = networkResult.gateway
      },
      async setGateway() {

        // send the input to the backend and let that validate whether it's valid
        const res = await fetch("http://localhost:8000/networks/" + this.network.id + "/gateway", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.form)
        })
        const newlyAddedGw = await res.json()

        // look for a status code where we have invalid input
        if (res.status == 500) {
          // if so, hide the dialog and display an error
          this.newGatewayDialog = false
          this.invalidGatewayInput = true
        } else {          
          // refresh the data on this page - note this won't reload the page, just refresh the data rendered within
          this.getSingleNetwork(this.network.id)

          // hide device dialog and error message, if visible
          this.newGatewayDialog = false
          this.invalidGatewayInput = false
        }
      }
    },
    mounted() {
      this.getSingleNetwork(this.$route.params.id)
    }
  }

</script>

<template>
  <navigation />
  <v-container>
    <h1>
      {{ network.name }}
    </h1>
    <v-row>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Base IP</b>: {{ network.network }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Subnet Mask Bits:</b> {{ network.subnetMaskBits }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <div style="display:flex; justify-content:space-between">
            <div>
              <b>Gateway:</b> {{ network.gateway }}
            </div>
            <div>
              <v-btn icon="mdi-wrench" color="yellow" variant="outlined" size="small" @click.stop="newGatewayDialog = true"></v-btn>
            </div>
          </div>
          <v-alert v-if="invalidGatewayInput" class="ma-5" color="red" icon="mdi-alert-circle-outline" type="error" >Invalid input for gateway - record not updated</v-alert>
        </v-sheet>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>VLAN Number:</b> {{ network.vlan }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Classification:</b> {{ network.classification }}
        </v-sheet>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="12">
        <v-sheet class="ma-5 pa-5 text-h5">
          DHCP Range(s):
          name, start, end
        </v-sheet>
      </v-col>
    </v-row>

    <!-- the below v-dialog opens a modal with one input - a gateway - and adds it to the relevant VLAN on the backend
         For user convenience, there is also a cancel button, submit button, and clicking outside the window should cause it to close. -->
    
      <v-dialog v-model="newGatewayDialog" max-width="500">
        <!-- <v-form @submit.prevent="handleGatewayChange()" id="newGatewayForm"> -->
        <v-form @submit.prevent="setGateway()" id="newGatewayForm">
          <v-card title="Set Gateway">
            <v-text-field v-model="form.gateway" label="Address" clearable></v-text-field>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn form="newGatewayForm" text="Cancel" variant="plain" @click="newGatewayDialog = false"></v-btn>
              <v-btn form="newGatewayForm" text="Apply" variant="tonal" color="primary" type="submit"
                @click="newGatewayDialog = false"></v-btn>
            </v-card-actions>
          </v-card>
        </v-form>
      </v-dialog>
  </v-container>
</template>
