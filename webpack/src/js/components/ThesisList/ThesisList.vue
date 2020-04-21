<template>
    <v-app>
        <v-card elevation="1">
            <v-card-title>
                Theses

                <v-spacer></v-spacer>

                <v-text-field
                    v-model="search"
                    append-icon="mdi-magnify"
                    label="Search"
                    single-line
                    hide-details
                ></v-text-field>

            </v-card-title>
            <v-data-table
                :headers="headers"
                :items="items"
                :search="search"
                :options.sync="options"
                :server-items-length="totalCount"
                :loading="loading"
                :items-per-page="40"
            ></v-data-table>
        </v-card>
    </v-app>
</template>

<script>
    import {VDataTable} from 'vuetify/lib';

    export default {
        components: {VDataTable},
        data() {
            return {
                url: this.$parent.url,
                search: '',
                items: [],
                totalCount: 0,
                loading: true,
                options: {},
                headers: [
                    {text: 'SN', value: 'registration_number'},
                    {text: 'Title', value: 'title'},
                    {text: 'Author', value: 'author.full_name'},
                    {text: 'Opponent', value: 'opponent.full_name'},
                    {text: 'Supervisor', value: 'supervisor.full_name'},
                ],
            };
        },
        watch: {
            options: {
                async handler() {
                    await this.load();
                },
                deep: true,
            },
        },
        methods: {
            async load() {
                const {sortBy, sortDesc, page = 1, itemsPerPage, ...rest} = this.options;
                console.log(this.options);

                const coreapi = window.coreapi;  // Loaded by `coreapi.js`
                const schema = window.schema;    // Loaded by `schema.js`

                console.log(schema);
                const client = new coreapi.Client();

                this.loading = true;
                let {count, results} = await client.action(schema, ['thesis', 'list'], {page});
                this.items = results;
                this.totalCount = count;
                this.loading = false;
            },
        },
        async created() {
            await this.load();
        },
    };
</script>

<style scoped>

</style>