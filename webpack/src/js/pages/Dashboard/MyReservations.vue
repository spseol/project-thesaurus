<template>
    <v-card>
        <v-card-title>{{ $t('My reservations') }}</v-card-title>
        <v-card-text>
            <v-alert v-for="res in reservations" v-bind="stateToAttrs(res.state)">
                {{ res.thesis_label }}
                <div>
                    <strong class="float-right">
                        {{ res.state_label }}
                    </strong>
                </div>
            </v-alert>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Axios from '../../axios';

    export default {
        name: 'MyReservations',
        data() {
            return {};
        },
        methods: {
            stateToAttrs(state) {
                return {
                    created: {type: 'info', outlined: true},
                    ready: {type: 'warning', prominent: true},
                    running: {type: 'success', outlined: true}
                }[state] || 'info';
            }
        },
        asyncComputed: {
            async reservations() {
                return _.sortBy(
                    (await Axios.get('/api/v1/reservation')).data,
                    s => ['ready', 'running', 'created'].indexOf(s.state)
                );
            }
        }
    };
</script>