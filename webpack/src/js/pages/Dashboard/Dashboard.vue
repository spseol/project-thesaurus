<template>
    <v-card v-page-title="$t('page.title.dashboard')">
        <v-card-title>{{ $t('Dashboard') }}</v-card-title>
        <v-card-text>
            <CallLoader :identifier="DASHBOARD_ACTIONS.LOAD_DASHBOARD"></CallLoader>

            <template v-for="thesis in dashboardStore.author_theses">
                <v-alert
                    v-if="thesis.state === 'ready_for_submit'"
                    prominent type="warning" color="red accent-2"
                >
                    <v-row align="center">
                        <v-col class="grow">
                            <h2 class="mb-1">{{ $t('Thesis waiting for submit') }}</h2>
                            <v-icon small>mdi-format-title</v-icon>
                            {{ thesis.title }}
                            <br>
                            <v-icon small>mdi-account</v-icon>
                            {{ thesis.authors.map(a => a.full_name).join(', ') }}
                            <template v-if="thesis.submit_deadline">
                                <br>
                                <v-icon small>mdi-calendar</v-icon>
                                {{ $t('Submit deadline') }}
                                {{ relativeDeadline(thesis.submit_deadline) }}
                                <span class="caption">
                                    ({{ deadline(thesis.submit_deadline).calendar() }})
                                </span>
                            </template>
                        </v-col>
                        <v-col class="shrink">
                            <v-btn large :to="$i18nRoute({name: 'thesis-submit', params: {id: thesis.id}})">
                                {{ $t('Submit thesis') }}
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-alert>

                <v-alert v-else type="info" outlined prominent color="gray">
                    <v-row align="center">
                        <v-col class="grow">
                            <h3 class="mb-1">{{ thesis.title }}</h3>
                            {{ thesis.authors.map(a => a.full_name).join(', ') }}
                        </v-col>
                        <v-col class="shrink">
                            <v-btn large text>
                                {{ thesis.state_label }}
                            </v-btn>
                        </v-col>
                    </v-row>
                </v-alert>
            </template>

            <v-alert
                v-for="thesis in dashboardStore.theses_ready_for_review" :key="thesis.id"
                prominent type="info" light
            >
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">{{ $t('Thesis waiting for review') }}</h2>
                        {{ thesis.title }} <br>
                        {{ thesis.authors.map(a => a.full_name).join(', ') }}
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="$i18nRoute({name: 'review-detail', params: {thesisId: thesis.id}})">
                            {{ $t('Submit review') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert type="info" outlined prominent v-if="dashboardStore.reservations_ready_for_prepare.length">
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Reservations waiting for prepare') }}
                            ({{ dashboardStore.reservations_ready_for_prepare.length }})
                        </h2>
                        {{ reservedThesesRegistrationNumbers.join(', ') }}
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="$i18nRoute({name: 'reservation-list'})">
                            {{ $t('Go to reservations') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert type="info" outlined prominent v-if="dashboardStore.theses_just_submitted.length">
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Just submitted theses waiting for check') }}
                            ({{ dashboardStore.theses_just_submitted.length }})
                        </h2>
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="$i18nRoute({name: 'thesis-list'})">
                            {{ $t('Go to theses') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert v-if="!hasData && !$calls.isPending(DASHBOARD_ACTIONS.LOAD_DASHBOARD)" type="info" outlined>
                {{ $t('dashboard.nothingNote') }}
            </v-alert>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import moment from 'moment';
    import Vue from 'vue';
    import {mapState} from 'vuex';
    import CallLoader from '../../components/CallLoader.vue';
    import {DASHBOARD_ACTIONS} from '../../store/dashboard';
    import {dashboardStore} from '../../store/store';

    export default Vue.extend({
        name: 'Dashboard',
        components: {CallLoader},
        data() {
            return {DASHBOARD_ACTIONS};
        },
        computed: {
            ...mapState({'dashboardStore': 'dashboard'}),
            ...dashboardStore.mapGetters([
                'reservedThesesRegistrationNumbers',
                'hasData'
            ])
        },
        methods: {
            ...dashboardStore.mapActions([DASHBOARD_ACTIONS.LOAD_DASHBOARD]),
            relativeDeadline(date) {
                return this.deadline(date).fromNow();
            },
            deadline(date) {
                return moment(date, null, this.$i18n.locale).endOf('day');
            }
        },
        watch: {
            '$i18n.locale'() {
                this[DASHBOARD_ACTIONS.LOAD_DASHBOARD]();
            }
        }
    });
</script>