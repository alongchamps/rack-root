<template>
    <v-app-bar :elevation="2">
        <template v-slot:prepend>
            <v-app-bar-nav-icon></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title>Rack Root</v-app-bar-title>
    </v-app-bar>
    <v-navigation-drawer>
        <v-list-item title="Home" to="/"></v-list-item>
        <v-divider></v-divider>
        <v-list-item title="Items" to="/items"></v-list-item>
        <!-- <v-list-item title="Books" to="/books"></v-list-item> -->
    </v-navigation-drawer>
</template>
