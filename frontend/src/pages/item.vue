<script>
    export default {
        data() {
            return {
                item: {}
            }
        },
        methods: {
            async getSingleItem(id) {
                const res = await fetch("http://localhost:8000/items/" + id);
                const itemResult = await res.json();

                if( res.status == 404 ) {
                    console.error("item not found")
                    this.$router.push('/404')
                }

                this.item = itemResult;
            },
            async deleteItem(id) {
                fetch('http://localhost:8000/items/' + id, {
                    method: 'DELETE'
                })
                    .then(resposne => response.json())
                    .then(data => console.log(data));
                
                this.$router.push('/items');
            },
            async editItem(id) {
                this.$router.push('/items/' + id + '/edit')
            }
        },
        mounted() {
            this.getSingleItem(this.$route.params.id);
        }
    }
</script>

<!-- <template>
    <navigation />
    <h2>Single item page</h2><br />
    <ul>
        <li>Name: {{ item.name }}</li>
        <li>Description: {{ item.description }}</li>
        <li>Item ID in the DB: {{ item.id }}</li>
    </ul>
    <br />
    <form @submit.prevent="deleteItem(item.id)">
        <button>Delete Item</button>
    </form>
    <form @submit.prevent="editItem(item.id)">
        <button>Edit Item</button>
    </form>
</template> -->


<template>
    <navigation />
    <v-card
      class="mx-auto"
      max-width="344"
    >
      <v-card-text>
        <div>Individual item detail</div>
  
        <p class="text-h4 font-weight-black">Name: {{ item.name }}</p>
  
        <p>Type: server</p>
  
        <div class="text-medium-emphasis">
          Description: {{ item.description }}<br />
          itemType: {{ item.itemType }}<br />
          serialNumber: {{ item.serialNumber }}<br />
          purchaseDate: {{ item.purchaseDate }}<br />
          warrantyExpiration: {{ item.warrantyExpiration }}<br />
          operatingSystem: {{ item.operatingSystem }}<br />
          notes: {{ item.notes }}<br />
        </div>
      </v-card-text>
      <v-card-actions>
        <!-- <v-btn @click="editItem(item.id)">Edit</v-btn>
        <v-btn @click="deleteItem(item.id)">Delete</v-btn> -->
      </v-card-actions>

      <!-- <v-card-actions>
        <v-btn
          color="deep-purple-accent-4"
          text="Learn More"
          variant="text"
        ></v-btn>
      </v-card-actions> -->
    </v-card>
  </template>
