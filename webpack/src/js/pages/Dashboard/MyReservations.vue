<template>
    <v-card>
        <v-card-title>{{ $t('My reservations') }}</v-card-title>
        <v-card-text>
            <v-alert v-for="res in reservations" v-bind="stateToAttrs(res.state)" :key="res.id">
                {{ res.thesis_label }}
                <div class="mt-3">
                    <strong class="float-left">
                        {{ res.state_label }}

                    </strong>

                    <v-dialog
                        v-model="cancelDialogs[res.id]"
                        v-if="res.state === 'created'"
                        width="500"
                    >
                        <template v-slot:activator="{ on }">
                            <v-btn color="warning" class="float-right" small text v-on="on">
                                {{ $t('Cancel') }}
                                <v-icon right>mdi-cancel</v-icon>
                            </v-btn>
                        </template>

                        <v-card>
                            <v-card-title class="headline warning lighten-5" primary-title>
                                {{ $t('Cancel reservation?') }}
                            </v-card-title>

                            <v-card-text class="mt-5">
                                {{ $t('reservation.cancelQuestion') }} {{ res.thesis_label }}
                            </v-card-text>

                            <v-divider></v-divider>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="warning" text @click="cancelReservation(res)">
                                    {{ $t('Cancel reservation') }}
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </div>
            </v-alert>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Axios from '../../axios';
    import {eventBus} from '../../utils';

    export default {
        name: 'MyReservations',
        data() {
            return {cancelDialogs: {}};
        },
        methods: {
            stateToAttrs(state) {
                return {
                    created: {type: 'info', outlined: true},
                    ready: {type: 'warning', prominent: true},
                    running: {type: 'success', outlined: true}
                }[state] || 'info';
            },
            async cancelReservation(reservation) {
                await Axios.post(`/api/v1/reservation/${reservation.id}/cancel`);
                eventBus.flash({
                    type: 'info',
                    text: this.$t('reservation.justCancelled')
                });
                this.cancelDialogs[reservation.id] = false;
                this.$asyncComputed.reservations.update();
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