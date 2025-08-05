<template>
  <v-app-bar style="height: 75px">
    <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>Rack Root</v-app-bar-title>

    <div>
      <v-form @submit.prevent="search">
        <v-text-field
          class="mt-2"
          placeholder="Inventory Search"
          variant="outlined"
          width="300"
          hide-details
          clearable
          v-model="searchQuery"
          @click:append="search"
        ></v-text-field>
      </v-form>
    </div>

    <template v-slot:append>
      <v-btn
        color="medium-emphasis"
        density="comfortable"
        icon="mdi-magnify"
      ></v-btn>
    </template>
    
  </v-app-bar>
  <v-navigation-drawer class="mt-3">
    <v-list-item prepend-icon="mdi-home" title="Home" to="/"></v-list-item>
    <v-list-item prepend-icon="mdi-memory" title="Items" to="/items"></v-list-item>
    <v-list-item prepend-icon="mdi-lan" title="Networks" to="/networks"></v-list-item>
    <v-list-item prepend-icon="mdi-cog" title="Settings" to="/settings"></v-list-item>
  </v-navigation-drawer>
</template>

<script>
  export default {
    data() {
      return {
        searchQuery: '',
      };
    },
    methods: {
      search() {
        if( this.searchQuery ) {
          this.$router.push('/search?q=' + this.searchQuery)
        }
      }
    }
  }
</script>

<!-- icons are from https://pictogrammers.com/library/mdi/ -->
<!-- Spacing: https://vuetifyjs.com/en/styles/spacing/#usage -->
