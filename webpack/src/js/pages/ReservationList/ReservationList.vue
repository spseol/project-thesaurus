<template>
    <div>
        <v-data-table
            :loading="loading"
            :headers="headers"
            :items="reservations.results"
            :search="search"
            :options.sync="options"
            :items-per-page="20"
            sort-by="created"
            :server-items-length="reservations.count"
            :footer-props="{
                'disable-items-per-page': true,
            }"
        >

            <template v-slot:item.state="props">
                <div class="text-center">
                    <v-edit-dialog
                        large
                        @save="changeState(props.item, stateEdit)"
                        @open="stateEdit = props.item.state"
                        :save-text="$t('Save')"
                        :cancel-text="$t('Cancel edit')"
                    >
                        <span class="caption d-flex align-center">
                            {{ stateToLabel(props.item.state) }}
                            <v-icon class="ml-1" small>mdi-lead-pencil</v-icon>
                        </span>
                        <template v-slot:input>
                            <v-select
                                :items="availableStatesToEdit" v-model="stateEdit" flat
                            ></v-select>
                        </template>
                    </v-edit-dialog>
                </div>
            </template>


            <template v-slot:item.created="{ item }">
                {{ (new Date(item.created)).toLocaleDateString($i18n.locale) }}
            </template>

            <template v-slot:item.actions="{ item }">
                <div class="text-center">
                    <v-btn
                        v-if="item.state === 'created'" @click="changeState(item, 'ready')" :disabled="loading"
                        small color="success" outlined
                    >
                        <v-icon class="pr-2">mdi-check-bold</v-icon>
                        {{ $t('Prepared for pickup') }}
                    </v-btn>
                    <v-btn
                        v-if="item.state === 'ready'" @click="changeState(item, 'running')" :disabled="loading"
                        small color="info" outlined
                    >
                        <v-icon class="pr-2">mdi-account-arrow-right-outline</v-icon>
                        {{ $t('Picked up') }}
                    </v-btn>
                    <v-btn
                        v-if="item.state === 'running'" @click="changeState(item, 'finished')" :disabled="loading"
                        small color="primary" outlined
                    >
                        <v-icon class="pr-2">mdi-account-arrow-left-outline</v-icon>
                        {{ $t('Returned') }}
                    </v-btn>
                </div>

            </template>
            <template v-slot:item.audit="{ item }">
                <audit-for-instance
                    small :model-pk="item.id" model-name="thesis.reservation"
                ></audit-for-instance>
            </template>
        </v-data-table>

        <!-- didnt find any better way to stop portal in case of another page view with disabled keep-alive -->
        <portal to="navbar-center" v-if="$route.name === 'reservation-list'">
            <v-toolbar dense color="transparent" elevation="0">
                <v-text-field
                    flat solo-inverted solo clearable
                    hide-details prepend-inner-icon="mdi-magnify"
                    v-model="search"
                    :label="$t('Search')"
                ></v-text-field>
                <v-divider vertical class="mx-2"></v-divider>
                <v-select
                    v-model="stateFilter" :items="stateOptions" :label="$t('State')"
                    solo solo-inverted flat hide-details prepend-inner-icon="mdi-filter-outline" style="max-width: 18em"
                >
                </v-select>
            </v-toolbar>
        </portal>
    </div>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Vue from 'vue';
    import AuditForInstance from '../../components/AuditForInstance.vue';
    import {RESERVATION_ACTIONS} from '../../store/reservation';
    import {reservationStore} from '../../store/store';
    import {hasPerm} from '../../user';
    import {asyncComputed, notificationBus} from '../../utils';

    export default Vue.extend({
        name: 'ReservationList',
        components: {AuditForInstance},
        data() {
            return {
                loading: false,
                items: [],
                headers: [],
                search: '',
                stateFilter: 'open',
                options: {},
                stateEdit: null,
            };
        },
        computed: {
            ...reservationStore.mapState(['reservations']),
            availableStatesToEdit() {
                return _.slice(this.stateOptions, 1);
            },
        },
        asyncComputed: {
            // TODO: link to vuex
            stateOptions: asyncComputed('/api/v1/reservation-state-options'),
        },
        methods: {
            ...reservationStore.mapActions([
                RESERVATION_ACTIONS.EDIT_RESERVATION,
                RESERVATION_ACTIONS.LOAD_RESERVATIONS,
            ]),
            stateToLabel(state) {
                return (_.find(this.stateOptions, {value: state}) || {text: '---'}).text;
            },
            async changeState(reservation, state) {
                this.loading = true;

                const data = await this[RESERVATION_ACTIONS.EDIT_RESERVATION]({
                    reservation_id: reservation.id,
                    data: {state},
                });
                if (data.id) {
                    notificationBus.success(this.$t('reservation.stateChanged'));
                } else {
                    notificationBus.warning(data.toString());
                }
                this.loading = false;
            },
            async load() {
                await this[RESERVATION_ACTIONS.LOAD_RESERVATIONS]({
                    options: this.options,
                    state: this.stateFilter,
                    search: this.search,
                    headers: this.headers,
                });
            },
        },
        async created() {
            this.debouncedLoad = _.debounce(this.load, 200);

            this.$watch(
                (vm) => ([vm.options, vm.$i18n.locale]),
                this.debouncedLoad,
                {deep: true, immediate: true},
            );

            this.$watch(
                (vm) => ([vm.search, vm.stateFilter]),
                () => {
                    this.options.page = 1;
                    this.debouncedLoad();
                },
            );

            const customStateSort = ['created', 'ready', 'running', 'finished'];
            this.headers = [
                {text: this.$t('For user'), value: 'user.full_name', mapped: 'user__last_name'},
                {
                    text: this.$t('Thesis SN'),
                    value: 'thesis_registration_number',
                    mapped: 'thesis__registration_number',
                },
                {text: this.$t('Thesis'), value: 'thesis_label', mapped: 'thesis__title'},
                {text: this.$t('Created'), value: 'created'},
                {text: this.$t('State'), value: 'state', sort: (t) => customStateSort.indexOf(t)},
                {text: this.$t('Actions'), value: 'actions', sortable: false},
            ];
            if (await hasPerm('audit.view_auditlog'))
                this.headers.push(
                    {text: this.$t('Audit'), value: 'audit', sortable: false},
                );

        },
    });
</script>

<style scoped>

</style>