<template>
    <div>
        <v-data-table
            :loading="loading"
            :headers="headers"
            :items="filteredItems"
            :search="search"
            :options.sync="options"
            :items-per-page="20"
            sort-by="created"
            :footer-props="{
                'disable-items-per-page': true,
            }"
        >

            <template v-slot:item.state="{ item }" class="text-center">
                <div class="text-center">
                    <v-chip outlined :color="stateToColor(item.state)">{{ stateToLabel(item.state) }}</v-chip>
                </div>
            </template>

            <template v-slot:item.created="{ item }">
                {{ (new Date(item.created)).toLocaleString() }}
            </template>

            <template v-slot:item.actions="{ item }">
                <div class="text-center">
                    <v-btn
                        v-if="item.state === 'created'" @click="changeState(item, 'ready')" :disabled="loading"
                        small color="success" v-text="$t('Prepared for pickup')" outlined
                    ></v-btn>
                    <v-btn
                        v-if="item.state === 'ready'" @click="changeState(item, 'running')" :disabled="loading"
                        small color="info" v-text="$t('Picked up')" outlined
                    ></v-btn>
                    <v-btn
                        v-if="item.state === 'running'" @click="changeState(item, 'finished')" :disabled="loading"
                        small color="primary" v-text="$t('Returned')" outlined
                    ></v-btn>
                </div>
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
                        v-for="{text, value} in stateOptions"
                        :key="value" :value="value"
                        v-text="text"
                    ></v-btn>

                </v-btn-toggle>
            </v-toolbar>
        </portal>
    </div>
</template>

<script>
    import _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';
    import {eventBus} from '../../utils';

    export default Vue.extend({
        name: 'ReservationList',
        data() {
            return {
                loading: false,
                items: [],
                search: '',
                stateFilter: 'all',
                options: {},
            };
        },
        computed: {
            filteredItems() {
                return _.filter(
                    this.items,
                    i => this.stateFilter === 'all' || i.state === this.stateFilter,
                );
            },
            headers() {
                const customStateSort = ['created', 'ready', 'running', 'finished'];
                return [
                    {text: this.$t('For user'), value: 'for_user.full_name'},
                    {text: this.$t('Thesis SN'), value: 'thesis_registration_number'},
                    {text: this.$t('Thesis'), value: 'thesis_title'},
                    {text: this.$t('Created'), value: 'created'},
                    {text: this.$t('State'), value: 'state', sort: (t) => customStateSort.indexOf(t)},
                    {text: this.$t('Actions'), value: 'actions', sortable: false},
                    // {name: this.$t('State'), value: 'state'},
                ];
            },
        },
        asyncComputed: {
            async stateOptions() {
                return [
                    {text: this.$t('All'), value: 'all'},
                    ...(await Axios.get('/api/v1/reservation-state-options')).data,
                ];
            },
        },
        methods: {
            stateToColor(state) {
                return {
                    created: 'success',
                    ready: 'info',
                    running: 'primary',
                }[state] || '';
            },
            stateToLabel(state) {
                return (_.find(this.stateOptions, {value: state}) || {text: '---'}).text;
            },
            async changeState(reservation, state) {
                this.loading = true;

                const {data} = await Axios.patch(`/api/v1/reservation/${reservation.id}`, {
                    state,
                });
                if (data.id) {
                    eventBus.flash({color: 'success', text: this.$t('reservation.stateChanged')});
                } else {
                    eventBus.flash({color: 'primary', text: data.toString()});
                }
                await this.load();
                this.loading = false;
            },
            async load() {
                const {page = 1} = this.options;
                // TODO: async API search
                this.items = (await Axios.get(`/api/v1/reservation?page=${page}`)).data;//.results;
            },
        },
        async created() {
            await this.load();
            this.$watch('options', async () => this.load());
        },
    });
</script>

<style scoped>

</style>