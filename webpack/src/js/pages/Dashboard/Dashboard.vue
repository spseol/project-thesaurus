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
                        {{ thesis.authors.map(a => a.full_name).join(',') }}
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
                        {{ thesis.authors.map(a => a.full_name).join(',') }}
                    </v-col>
                    <v-col class="shrink">
                        <v-btn large :to="{name: 'review-submit', params: {id: thesis.id}}">
                            {{ $t('Submit review') }}
                        </v-btn>
                    </v-col>
                </v-row>
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
                theses_ready_for_review: []
            };
        },
        async created() {
            const {theses_ready_for_submit, theses_ready_for_review} = (await Axios.get('/api/v1/dashboard')).data;
            _.assign(
                this,
                {
                    theses_ready_for_submit, theses_ready_for_review
                }
            );
        }
    };
</script>