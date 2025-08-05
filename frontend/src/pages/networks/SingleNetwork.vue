<script>
  export default {
    data() {
      return {
        form: {
          ipAddress: ''
        },
        network: {},
        ipAddress: {},
        newGatewayDialog: false,
        invalidGatewayInput: false,
        totalIps: 0,
        availableIps: 0,
        dhcpIps: 0,
        dhcpRanges: [],
        dhcpRangeHeaders: [
          { title: 'ID', value: 'id' },
          { title: 'Name', value: 'name' },
          { title: 'Description', value: 'description' },
          { title: 'First IP', value: 'startIp' },
          { title: 'Last IP', value: 'lastIp' },
        ]
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
        this.totalIps = networkResult.ipRecord.length
        this.availableIps = networkResult.ipRecord.filter((ip) => ip.status == "Available").length
        this.dhcpIps = networkResult.ipRecord.filter((ip) => ip.status == "DHCP").length

        // This may return a 404, which is expected when no gateway is set on the network
        const resGateway = await fetch("http://localhost:8000/networks/" + id + "/gateway/")

        const gatewayResult = await resGateway.json()
        this.ipAddress = gatewayResult
        this.form.ipAddress = gatewayResult.ipAddress
      },
      async getDhcpRanges(id) {
        const res = await fetch("http://localhost:8000/networks/" + id + "/dhcp/")
        const dhcpResults = await res.json()

        this.dhcpRanges = dhcpResults
      },
      async setGateway() {

        // send the input to the backend and let that validate whether it's valid
        const res = await fetch("http://localhost:8000/networks/" + this.network.id + "/gateway/", {
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
          // refresh the data on this page
          this.getSingleNetwork(this.network.id)

          // hide device dialog and error message, if visible
          this.newGatewayDialog = false
          this.invalidGatewayInput = false
        }
      },
      async deleteGateway() {
        // run HTTP DELETE on the gateway on this network
        const res = await fetch("http://localhost:8000/networks/" + this.network.id + "/gateway/", {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json'
          },
        })

        // refresh the data on this page
        this.getSingleNetwork(this.$route.params.id)
      },
      async deleteNetwork() {
        // run HTTP delete on the network
        const res = await fetch("http://localhost:8000/networks/" + this.network.id, {
          method: 'DELETE'
        })

        // send the user back to /networks
        this.$router.push("/networks")
      }
    },
    mounted() {
      this.getSingleNetwork(this.$route.params.id)
      this.getDhcpRanges(this.$route.params.id)
    }
  }

</script>

<template>
  <navigation />
  <v-container>
    <h1>
      <div style="display:flex; justify-content:space-between">
        <div>
          {{ network.name }}
        </div>
        <div>
          <v-btn class="ma-6" prepend-icon="mdi-trash-can" color="red" @click="deleteNetwork()">Delete Network</v-btn>
        </div>
      </div>  
    </h1>
    <v-row>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Network</b>: {{ network.network }}
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
              <b>Gateway:</b> {{ ipAddress.ipAddress }}
            </div>
            <div>
              <v-btn v-if="ipAddress.ipAddress == null" icon="mdi-plus" color="green" variant="outlined" size="small" @click.stop="newGatewayDialog = true"></v-btn>
              <v-btn v-else icon="mdi-trash-can-outline" color="red" variant="outlined" size="small" @click.stop="deleteGateway()"></v-btn>
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
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5 mb-10">
        Total IPs: {{ this.totalIps }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5 mb-10">
        Available IPs: {{ this.availableIps }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5 mb-10">
        DHCP IPs: {{ this.dhcpIps }}
        </v-sheet>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="12">
        <h1>DHCP Ranges</h1>
        <v-sheet class="ma-5 pa-5 text-h5">
          <v-data-table :items="dhcpRanges" :headers="dhcpRangeHeaders" item-key="id">
          </v-data-table>
        </v-sheet>
      </v-col>
    </v-row>

    <!-- the below v-dialog opens a modal with one input - a gateway - and adds it to the relevant VLAN on the backend
         For user convenience, there is also a cancel button, submit button, and clicking outside the window should cause it to close. -->
    
      <v-dialog v-model="newGatewayDialog" max-width="500">
        <!-- <v-form @submit.prevent="handleGatewayChange()" id="newGatewayForm"> -->
        <v-form @submit.prevent="setGateway()" id="newGatewayForm">
          <v-card title="Set Gateway">
            <v-text-field v-model="form.ipAddress" label="Address" clearable></v-text-field>
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
