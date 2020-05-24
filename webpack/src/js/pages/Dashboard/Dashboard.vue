<template>
    <v-card>
        <v-card-title>{{ $t('Dashboard') }}</v-card-title>
        <v-card-text>
            <template v-for="thesis in author_theses">

                <v-alert
                    v-if="thesis.state === 'ready_for_submit'"
                    prominent type="warning"
                >
                    <v-row align="center">
                        <v-col class="grow">
                            <h2 class="mb-1">{{ $t('Thesis waiting for submit') }}</h2>
                            {{ thesis.title }} <br>
                            {{ thesis.authors.map(a => a.full_name).join(', ') }}
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
                v-for="thesis in theses_ready_for_review" :key="thesis.id"
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

            <v-alert type="info" outlined prominent v-if="reservations_ready_for_prepare.length">
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Reservations waiting for prepare') }}
                            ({{reservations_ready_for_prepare.length }})
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

            <v-alert type="info" outlined prominent v-if="theses_just_submitted.length">
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Just submitted theses waiting for check') }}
                            ({{ theses_just_submitted.length }})
                        </h2>
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="$i18nRoute({name: 'thesis-list'})">
                            {{ $t('Go to theses') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert v-if="showNoData" type="info" outlined>
                {{ $t('dashboard.nothingNote') }}
            </v-alert>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Axios from '../../axios';

    export default {
        name: 'Dashboard',
        data() {
            return {
                theses_ready_for_review: [],
                reservations_ready_for_prepare: [],
                theses_just_submitted: [],
                author_theses: []
            };
        },
        async created() {
            _.assign(
                this,
                (await Axios.get('/api/v1/dashboard')).data
            );
        },
        computed: {
            reservedThesesRegistrationNumbers() {
                return _.map(
                    this.reservations_ready_for_prepare,
                    _.property('thesis_registration_number')
                ).sort();
            },
            showNoData() {
                return !(
                    this.theses_ready_for_review.length ||
                    this.reservations_ready_for_prepare.length ||
                    this.theses_just_submitted.length ||
                    this.author_theses.length
                );
            }
        }
    };
</script>