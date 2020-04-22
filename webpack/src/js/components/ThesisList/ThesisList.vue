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
    import Axios from '../api-client.ts';
    import _ from 'lodash';

    import qs from 'qs';


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
                    {text: 'Author', value: 'author.full_name', mapped: 'author__last_name'},
                    {text: 'Opponent', value: 'opponent.full_name', mapped: 'opponent__last_name'},
                    {text: 'Supervisor', value: 'supervisor.full_name', mapped: 'supervisor__last_name'},
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
            search() {
                this.debouncedLoad();
            },
        },
        methods: {
            async load() {
                const {sortBy, sortDesc, page = 1, itemsPerPage, ...rest} = this.options;

                this.loading = true;
                // TODO: generalize? VueJS Composition API?
                const remap = (value) => _.find(this.headers, {value}).mapped || value;

                const resp = await Axios.get(`/api/v1/thesis/?${qs.stringify({
                    page,
                    search: this.search,
                    ordering: _.map(_.zip(sortBy, sortDesc), ([col, desc]) => `${desc ? '-' : ''}${remap(col).split('.')[0]}`).join(','),
                })}`);

                this.items = resp.data.results;
                this.totalCount = resp.data.count;
                this.loading = false;
            },
        },
        async created() {
            await this.load();
            this.debouncedLoad = _.debounce(this.load, 200);
        },
    };
</script>

<style scoped>

</style>