<template>
    <v-card>
        <v-card-title>{{ $t('My reservations') }}</v-card-title>
        <v-card-text>
            <v-progress-linear indeterminate v-if="false"></v-progress-linear>

            <v-alert v-for="res in orderedByImportance" v-bind="stateToAttrs(res.state)" :key="res.id">
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
                                {{ $t('reservation.cancel.dialogTitle') }}
                            </v-card-title>

                            <v-card-text class="mt-5">
                                {{ $t('reservation.cancel.question') }} {{ res.thesis_label }}?
                            </v-card-text>

                            <v-divider></v-divider>

                            <v-card-actions>
                                <v-spacer></v-spacer>
                                <v-btn color="warning" text @click="cancelReservation(res)">
                                    {{ $t('reservation.cancel.confirmationButton') }}
                                </v-btn>
                            </v-card-actions>
                        </v-card>
                    </v-dialog>
                </div>
            </v-alert>

            <v-alert type="info" text v-if="!orderedByImportance.length">
                {{ $t('reservation.noActiveReservations') }}
                <v-row justify="end" class="mt-2">
                    <v-btn :to="$i18nRoute({name: 'thesis-list'})" type="info" light text>
                        {{ $t('reservation.goAndMakeAReservation') }}
                    </v-btn>
                </v-row>
            </v-alert>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import {RESERVATION_ACTIONS} from '../../store/reservation';
    import {reservationStore} from '../../store/store';
    import {notificationBus} from '../../utils';

    export default {
        name: 'MyReservations',
        data() {
            return {cancelDialogs: {}};
        },
        computed: {
            ...reservationStore.mapGetters(['orderedByImportance'])
        },
        methods: {
            ...reservationStore.mapActions([
                RESERVATION_ACTIONS.LOAD_RESERVATIONS,
                RESERVATION_ACTIONS.CANCEL_RESERVATION
            ]),
            stateToAttrs(state) {
                return {
                    created: {type: 'info', outlined: true},
                    ready: {type: 'success', prominent: true, text: true},
                    running: {type: 'success', outlined: true, icon: 'mdi-clock'}
                }[state] || {type: 'info'};
            },
            async cancelReservation(reservation) {
                const data = await this[RESERVATION_ACTIONS.CANCEL_RESERVATION]({
                    reservation_id: reservation.id
                });

                if (data.id) {
                    notificationBus.info(this.$t('reservation.justCancelled'));
                    this.cancelDialogs[reservation.id] = false;
                } else {
                    notificationBus.warning(data.toString());
                }
            }
        },
        created() {
            this[RESERVATION_ACTIONS.LOAD_RESERVATIONS]();
        }
    };
</script>