<template>
    <v-card>
        <v-card-title>{{ $t('Dashboard') }}</v-card-title>
        <v-card-text>
            <v-alert
                v-for="thesis in theses_ready_for_submit" :key="thesis.id"
                prominent type="warning"
            >
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">{{ $t('Thesis waiting for submit') }}</h2>
                        {{ thesis.title }} <br>
                        {{ thesis.authors.map(a => a.full_name).join(', ') }}
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="{name: 'thesis-submit', params: {id: thesis.id}}">
                            {{ $t('Submit thesis') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

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
                        <v-btn large :to="{name: 'review-detail', params: {thesisId: thesis.id}}">
                            {{ $t('Submit review') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert type="info" outlined prominent>
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Reservations waiting for prepare') }}
                            ({{reservations_ready_for_prepare.length }})
                        </h2>
                        {{ reservedThesesRegistrationNumbers.join(', ') }}
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="{name: 'reservations'}">
                            {{ $t('Go to reservations') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert v-if="!(theses_ready_for_review.length + theses_ready_for_submit.length + reservations_ready_for_prepare.length)" type="info" outlined>
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
                theses_ready_for_submit: [],
                theses_ready_for_review: [],
                reservations_ready_for_prepare: []
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
            }
        }
    };
</script>