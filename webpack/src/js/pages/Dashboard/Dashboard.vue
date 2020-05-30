<template>
    <v-card>
        <v-card-title>{{ $t('Dashboard') }}</v-card-title>
        <v-card-text>
            <v-progress-linear indeterminate v-if="$asyncComputed.data.updating"></v-progress-linear>

            <template v-for="thesis in data.author_theses">
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
                                {{ $t('Submit deadline') }} {{ relativeDeadline(thesis.submit_deadline) }}
                                <span class="caption">({{ (new Date(thesis.submit_deadline)).toLocaleDateString($i18n.locale) }})</span>
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
                v-for="thesis in data.theses_ready_for_review" :key="thesis.id"
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

            <v-alert type="info" outlined prominent v-if="data.reservations_ready_for_prepare.length">
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Reservations waiting for prepare') }}
                            ({{ data.reservations_ready_for_prepare.length }})
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

            <v-alert type="info" outlined prominent v-if="data.theses_just_submitted.length">
                <v-row align="center">
                    <v-col class="grow">
                        <h2 class="mb-1">
                            {{ $t('Just submitted theses waiting for check') }}
                            ({{ data.theses_just_submitted.length }})
                        </h2>
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="$i18nRoute({name: 'thesis-list'})">
                            {{ $t('Go to theses') }}
                        </v-btn>
                    </v-col>
                </v-row>
            </v-alert>

            <v-alert v-if="hasNoData && !$asyncComputed.data.updating" type="info" outlined>
                {{ $t('dashboard.nothingNote') }}
            </v-alert>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import moment from 'moment';
    import {asyncComputed} from '../../utils';

    export default {
        name: 'Dashboard',
        asyncComputed: {
            data: asyncComputed(
                '/api/v1/dashboard',
                {
                    'default': {
                        theses_ready_for_review: {},
                        reservations_ready_for_prepare: {},
                        theses_just_submitted: {},
                        author_theses: {}
                    }
                }
            ),
            async hasNoData() {
                return !(
                    this.data.theses_ready_for_review.length ||
                    this.data.reservations_ready_for_prepare.length ||
                    this.data.theses_just_submitted.length ||
                    this.data.author_theses.length
                );
            }
        },
        computed: {
            reservedThesesRegistrationNumbers() {
                return _.map(
                    this.data.reservations_ready_for_prepare,
                    _.property('thesis_registration_number')
                ).sort();
            }
        },
        methods: {
            relativeDeadline(date) {
                return moment(date, null, this.$i18n.locale).fromNow();
            }
        }
    };
</script>