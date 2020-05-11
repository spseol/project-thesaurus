<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="filteredItems"
            :search="search"
            show-select
            :items-per-page="1000"
            sort-by="created"
            :footer-props="{
                'disable-items-per-page': true,
            }"
        >

            <template v-slot:item.state="{ item }" class="text-center">
                <div class="text-center">
                    <v-chip outlined :color="stateToColor(item.state)">{{ stateToTitle(item.state) }}</v-chip>
                </div>
            </template>

            <template v-slot:item.actions="{ item }">
                <v-btn v-if="item.state === 'created'" small color="success" v-text="$t('Prepared for pickup')" outlined></v-btn>
                <v-btn v-if="item.state === 'ready'" small color="info" v-text="$t('Picked up')" outlined></v-btn>
                <v-btn v-if="item.state === 'running'" small color="primary" v-text="$t('Returned')" outlined></v-btn>
            </template>

        </v-data-table>

        <portal to="navbar-center">
            <v-toolbar dense color="transparent" elevation="0">
                <v-text-field
                    flat
                    solo-inverted solo
                    hide-details
                    prepend-inner-icon="mdi-magnify"
                    v-model="search"
                    :label="$t('Search')"
                    clearable
                ></v-text-field>

                <v-btn-toggle
                    v-model="stateFilter"
                    group
                    mandatory
                >
                    <v-btn
                        v-for="value in stateOptions"
                        :key="value" :value="value"
                        v-text="stateToTitle(value)"
                    ></v-btn>

                </v-btn-toggle>
            </v-toolbar>
        </portal>
    </div>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';

    export default Vue.extend({
        name: 'ReservationList',
        data() {
            return {
                headers: [
                    {text: this.$t('For user'), value: 'for_user.full_name'},
                    {text: this.$t('Thesis SN'), value: 'thesis_registration_number'},
                    {text: this.$t('Thesis'), value: 'thesis_title'},
                    {text: this.$t('Created'), value: 'created'},
                    {text: this.$t('State'), value: 'state'},
                    {text: this.$t('Actions'), value: 'actions'}
                    // {name: this.$t('State'), value: 'state'},
                ],
                items: [],
                search: '',
                stateFilter: 'all',
                stateOptions: ['all', 'created', 'ready', 'running', 'finished']
            };
        },
        computed: {
            filteredItems() {
                return _.filter(
                    this.items,
                    i => this.stateFilter == 'all' || i.state == this.stateFilter
                );
            }
        },
        methods: {
            stateToColor(state) {
                return {
                    created: 'success',
                    ready: 'info',
                    running: 'primary'
                }[state] || '';
            },
            stateToTitle(state) {
                return {
                    all: this.$t('All'),
                    created: this.$t('Added'),
                    ready: this.$t('Ready'),
                    running: this.$t('Running'),
                    finished: this.$t('Finished')
                }[state] || '';
            }
        },
        async created() {
            this.items = (await Axios.get(`/api/v1/reservation`)).data;
        }
    });
</script>

<style scoped>

</style>