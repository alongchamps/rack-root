<template>
  <v-app-bar :elevation="2">
    <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </template>

    <v-app-bar-title>Rack Root</v-app-bar-title>
  </v-app-bar>
  <v-navigation-drawer>
    <v-list-item prepend-icon="mdi-home" title="Home" to="/"></v-list-item>
    <v-list-item prepend-icon="mdi-memory" title="Items" to="/items"></v-list-item>
    <v-list-item prepend-icon="mdi-cog" title="Settings" to="/settings"></v-list-item>
  </v-navigation-drawer>
</template>
