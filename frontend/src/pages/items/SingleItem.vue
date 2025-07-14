<script>
  export default {
    data() {
      return {
        item: {},
        deviceTypeName: null,
        purchaseDate: null,
        warrantyExpiration: null
      }
    },
    methods: {
      // load the item from the backend, by the provided ID
      async getSingleItem(id) {
        const res = await fetch("http://localhost:8000/items/" + id)
        const itemResult = await res.json()

        if( res.status == 404 ) {
          console.error("item not found")
          this.$router.push('/404')
        }

        this.item = itemResult;
        this.deviceTypeName = itemResult.deviceType.name
        this.purchaseDate = itemResult.purchaseDate.split("T")[0]
        this.warrantyExpiration = itemResult.warrantyExpiration.split("T")[0]
      },
      // call HTTP DELETE on the item ID on this page
      async deleteItem() {
        // send a delete request to the backend
        const res = await fetch('http://localhost:8000/items/' + this.$route.params.id, {
          method: 'DELETE',
        })
        // send the user back to the all items page
        this.$router.push('/items/')
      },
      // allow certain fields to be editable
      async editItem() {
        // TODO
      }
    },
    mounted() {
      this.getSingleItem(this.$route.params.id)
    }
  }
</script>

<template>
  <navigation />
  <v-container>
    <h1>
      <div style="display:flex; justify-content:space-between">
        <div>
          {{ item.name }}
        </div>
        <div>
          <v-btn class="ma-6" prepend-icon="mdi-pencil" color="yellow" @click="editItem()">Edit (TODO)</v-btn>
          <v-btn class="ma-6" prepend-icon="mdi-trash-can" color="red" @click="deleteItem()">Delete</v-btn>
        </div>
      </div>  
    </h1>
    <v-row>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Type:</b> {{ this.deviceTypeName }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Description:</b> {{ item.description }}
        </v-sheet>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Serial number:</b> {{ item.serialNumber }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Purchase Date:</b> {{ this.purchaseDate }}
        </v-sheet>
      </v-col>
      <v-col cols="12" sm="4">
        <v-sheet class="ma-5 pa-5 text-h5">
          <b>Warranty Expiration:</b> {{ this.warrantyExpiration }}
        </v-sheet>
      </v-col>
    </v-row>

    <v-divider :thickness="2"></v-divider>
    <h1>Related to:</h1>
  </v-container>
</template>

<style scoped>
  .infotext {
    font-size: 16px;
  }
</style>



<!-- <v-card-text>
      <p class="text-h4 font-weight-black">Name: {{ item.name }}</p>
      <p>Description: {{ item.description }}</p>
      <p>Type: {{ item.deviceType }}</p>
      <p>Serial: {{ item.serialNumber }}</p>
      <p>Notes: {{ item.notes }}</p>
      <p>Purchase Date: {{ item.purchaseDate }}</p>
      <p>Warranty Expiration: {{ item.warrantyExpiration }}</p>
    </v-card-text> -->
