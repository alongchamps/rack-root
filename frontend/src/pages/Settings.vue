<script>
    export default {
        data() {
            return {
                tab: null,
                deviceTypes: [],
                headers: [
                    { title: 'ID', value: 'id' },
                    { title: 'Name', value: 'name' }
                ]
            }
        },
        methods: {
            async getItems() {
                const res = await fetch("http://localhost:8000/deviceTypes/");
                const finalDeviceTypes = await res.json();
                this.deviceTypes = finalDeviceTypes
            }
        },
        mounted() {
            this.getItems();
        }
    }
</script>

<template>
    <navigation />
    <div class="d-flex justify-center py-10 h-auto">
        <v-card width="75em">
            <v-tabs v-model="tab">
                <v-tab value="1-devices">Device Types</v-tab>
            </v-tabs>

            <v-card-text>
                <v-tabs-window v-model="tab">
                    <v-tabs-window-item value="1-devices">
                        <v-data-table :items="deviceTypes" :headers="headers" item-key="id"></v-data-table>
                    </v-tabs-window-item>
                </v-tabs-window>
            </v-card-text>
        </v-card>
    </div>
</template>
