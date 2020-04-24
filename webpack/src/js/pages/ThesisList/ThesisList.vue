<template>

    <div>
        <v-data-table
            :headers="headers"
            :items="items"
            :search="search"
            :options.sync="options"
            :server-items-length="totalCount"
            :loading="loading"
            sort-by="registration_number"
            single-expand
            show-expand
            :footer-props="{
                'disable-items-per-page': true,
            }"
        >
            <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length">More info about {{ item.title }}</td>
            </template>

            <!-- dynamic slots for all "author" FKs -->
            <template
                v-for="key in 'author supervisor opponent'.split(' ')"
                v-slot:[`item.${key}.full_name`]="{ item }"
            >
                <!-- TODO: add chips for each filter? -->
                <a @click="search += ` ${item[key].full_name}`">{{ item[key].full_name }}</a>
            </template>

        </v-data-table>


        <portal to="navbar-center">
            <v-text-field
                flat
                solo-inverted
                hide-details
                clearable
                prepend-inner-icon="mdi-magnify"
                label="Search"
                v-model="search"
            />
        </portal>
    </div>


</template>

<script type="text/tsx">
    import * as _ from 'lodash';

    import * as qs from 'qs';
    import Vue from 'vue';
    import Axios from '../../api-client';


    export default Vue.extend({
        data() {
            return {
                items: [],
                totalCount: 0,
                loading: true,
                options: {},
                search: '',
                headers: [
                    {text: 'SN', value: 'registration_number'},
                    {text: 'Title', value: 'title'},
                    {text: 'Category', value: 'category.title'},
                    {text: 'Acad. year', value: 'published_at'},
                    {text: 'Author', value: 'author.full_name', mapped: 'author__last_name'},
                    {text: 'Opponent', value: 'opponent.full_name', mapped: 'opponent__last_name'},
                    {text: 'Supervisor', value: 'supervisor.full_name', mapped: 'supervisor__last_name'},
                    {text: '', value: 'data-table-expand'}
                ]
            };
        },
        watch: {
            options: {
                async handler() {
                    await this.load();
                },
                deep: true
            },
            search() {
                this.options.page = 1;
                this.debouncedLoad();
            }
        },
        methods: {
            async load() {
                const {sortBy, sortDesc, page = 1, itemsPerPage, ...rest} = this.options;

                this.loading = true;
                // TODO: generalize? VueJS Composition API?
                const remap = (value) => (_.find(this.headers, {value}) || {}).mapped || value.replace('.', '__');

                const resp = await Axios.get(`/api/v1/thesis/?${qs.stringify({
                    page,
                    search: this.search,
                    ordering: _.map(
                        _.zip(sortBy, sortDesc),
                        ([col, desc]) => `${desc ? '-' : ''}${remap(col).split('.')[0]}`
                    ).join(',')
                })}`);

                this.items = resp.data.results;
                this.totalCount = resp.data.count;
                this.loading = false;
            }
        },
        async created() {
            await this.load();
            this.debouncedLoad = _.debounce(this.load, 200);
        }
    });
</script>

<style scoped>

</style>