<template>
    <span>
        <template v-if="thesis.state === 'published'">
            <!-- Can add reservation -> show state and possibility to create a reservation -->
            <span v-has-group:student>
                <v-btn v-has-perm:thesis.add_reservation
                    v-if="thesis.reservable && thesis.available_for_reservation && thesis.open_reservations_count === 0"
                    v-text="$t('Borrow')" @click="preReservation = !(createReservationDialog = true)"
                    small color="info" outlined :disabled="loading"
                ></v-btn>
                <v-btn v-has-perm:thesis.add_reservation
                    v-if="thesis.reservable && thesis.available_for_reservation && thesis.open_reservations_count === 1"
                    v-text="$t('Make pre-reservation')" @click="preReservation = createReservationDialog = true"
                    small color="info" outlined :disabled="loading"
                ></v-btn>
                <v-btn v-has-perm:thesis.add_reservation
                    v-if="thesis.reservable && !thesis.available_for_reservation && thesis.open_reservations_count > 1"
                    v-text="$t('Borrowed')"
                    x-small depressed
                ></v-btn>
            </span>

            <!-- Can view reservations -> show state of #reservations, without possibility to create -->

                <span v-has-perm:thesis.change_reservation
                    v-if="thesis.reservable"
                >
                    <v-badge
                        :content="thesis.open_reservations_count" v-if="thesis.open_reservations_count"
                        overlap color="grey"
                    >
                        <v-btn
                            v-text="$t('Borrowed')" :to="$i18nRoute({name: 'reservation-list'})"
                            x-small depressed disabled
                        ></v-btn>
                    </v-badge>

                    <v-btn v-if="thesis.available_for_reservation"
                        v-text="$t('Available')"
                        x-small depressed disabled
                    ></v-btn>
                </span>

            <!-- published but not reservable -->
            <v-btn
                v-if="!thesis.reservable"
                v-text="$t('Not reservable')"
                x-small depressed
            ></v-btn>
        </template>
        <v-btn
            v-has-perm:thesis.change_thesis
            v-if="thesis.state === 'created'"
            v-text="$t('Send to submit')"
            small color="primary" elevation="0"
            @click="sendToSubmit"
            :disabled="loading"
        ></v-btn>

        <v-btn
            v-has-perm:thesis.change_thesis
            v-if="thesis.state === 'submitted'"
            v-text="$t('Send to review')"
            small color="info" elevation="0"
            @click="sendToReviewDialog = true"
            :disabled="loading"
        ></v-btn>

        <v-btn
            v-has-perm:thesis.change_thesis
            v-if="thesis.state === 'reviewed'"
            v-text="$t('Publish')"
            small color="primary" elevation="0"
            @click="publish"
            :disabled="loading"
        ></v-btn>

        <v-btn
            v-has-perm:thesis.change_thesis
            v-if="thesis.state === 'ready_for_submit'"
            v-text="$t('Waiting for submit')"
            x-small depressed disabled
        ></v-btn>

        <span v-has-perm:thesis.change_thesis>
            <template v-if="thesis.state === 'ready_for_review'">
                <v-hover v-slot:default="{ hover }" style="min-width: 15em">
                    <v-badge
                        color="primary" overlap
                        :value="!hover && availableExternalReviewers.length"
                        :content="availableExternalReviewers.length"
                    >
                        <v-btn
                            v-if="!hover || !availableExternalReviewers.length"
                            small depressed disabled block
                        >{{ $t('Waiting for review') }}</v-btn>
                        <v-btn
                            v-if="hover && availableExternalReviewers.length"
                            @click="submitExternalReviewDialog = true"
                            small depressed outlined color="info" block
                        >{{ $t('Submit external review') }}</v-btn>
                    </v-badge>
                </v-hover>
            </template>
        </span>

        <v-dialog v-model="sendToReviewDialog" max-width="60em" :fullscreen="$vuetify.breakpoint.smAndDown">
            <v-card :loading="dialogLoading">
                <v-card-title
                    class="headline grey lighten-2"
                    primary-title
                >{{ $t('Send to review') }}</v-card-title>
                <v-card-text class="pt-3">
                    <v-simple-table>
                        <tbody>
                        <tr>
                            <td colspan="2" class="subtitle-1">{{ thesis.title }}</td>
                        </tr>
                        <tr class="subtitle-1">
                            <td>{{ $tc('Authors', thesis.authors.length) }}</td>
                            <td>{{ thesis.authors.map(a => a.full_name).join(', ') }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.supervisor">
                            <td>{{ $t('Supervisor') }}</td>
                            <td>{{ thesis.supervisor.full_name }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.opponent">
                            <td>{{ $t('Opponent') }}</td>
                            <td>{{ thesis.opponent.full_name }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.category">
                            <td>{{ $t('Category') }}</td>
                            <td>{{ thesis.category.title }}</td>
                        </tr>
                        <tr class="subtitle-1">
                            <td class="col-2">{{ $t('Abstract') }}</td>
                            <td class="text-justify">{{ thesis.abstract }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="getAttachment('thesis_assigment')">
                            <td>{{ $t('Thesis assigment') }}</td>
                            <td><v-btn outlined :href="getAttachment('thesis_assigment').url" small target="_blank">{{ $t('Download thesis assigment') }}</v-btn></td>
                        </tr>
                        <tr class="subtitle-1" v-if="getAttachment('thesis_text')">
                            <td>{{ $t('Thesis text') }}</td>
                            <td><v-btn outlined :href="getAttachment('thesis_text').url" small target="_blank">{{ $t('Download thesis text') }}</v-btn></td>
                        </tr>
                        </tbody>
                    </v-simple-table>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                    <v-subheader class="ma-3">{{ $t('thesis.sendToReviewNote') }}</v-subheader>
                    <v-spacer></v-spacer>
                    <v-btn
                        color="success" class="ma-3" x-large
                        @click="sendToReview"
                        :disabled="!(thesis.opponent && thesis.supervisor)"
                    >{{ $t('Send to review') }}</v-btn>
                </v-card-actions>
              </v-card>
        </v-dialog>

        <v-dialog v-model="submitExternalReviewDialog" max-width="40em" :fullscreen="$vuetify.breakpoint.smAndDown">
            <v-card :loading="dialogLoading">
                <v-form>
                    <v-card-title
                        class="headline grey lighten-2"
                        primary-title
                    >{{ thesis.title }}</v-card-title>
                    <v-card-text class="pt-3 d-flex flex-column">
                        <v-btn-toggle
                            group class="align-self-center"
                            mandatory color="primary"
                            v-model="externalReview.reviewer"
                        >
                            <v-btn
                                v-for="[key, user] in availableExternalReviewers"
                                :key="key" :value="key"
                            >
                                <strong>{{ $t(key) }}</strong>: {{ user.full_name }}
                            </v-btn>
                        </v-btn-toggle>

                        <v-file-input
                            :label="$t('External review')"
                            v-model="externalReview.review" v-if="externalReview.reviewer"
                            :accept="typeAttachmentAcceptTypes(`${externalReview.reviewer}_review`)"
                            :prepend-icon="`$${externalReview.reviewer}_review`"
                        ></v-file-input>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            :disabled="!(externalReview.reviewer && externalReview.review)"
                            color="success" class="ma-3" x-large @click="submitExternalReview"
                        >{{ $t('Submit external review') }}</v-btn>
                    </v-card-actions>
                </v-form>
            </v-card>
        </v-dialog>

        <v-dialog v-model="createReservationDialog" max-width="60em">
            <v-card :loading="dialogLoading">
                <v-form>
                    <v-card-title
                        class="headline grey lighten-2"
                        primary-title
                    >{{ preReservation ? $t('New pre reservation for thesis borrow') : $t('Borrow') }}</v-card-title>
                    <v-card-text class="pt-3">
                        <v-simple-table>
                        <tbody>
                        <tr>
                            <td colspan="2" class="subtitle-1">{{ thesis.title }}</td>
                        </tr>
                        <tr class="subtitle-1">
                            <td>{{ $tc('Authors', thesis.authors.length) }}</td>
                            <td>{{ thesis.authors.map(a => a.full_name).join(', ') }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.supervisor">
                            <td>{{ $t('Supervisor') }}</td>
                            <td>{{ thesis.supervisor.full_name }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.opponent">
                            <td>{{ $t('Opponent') }}</td>
                            <td>{{ thesis.opponent.full_name }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.category">
                            <td>{{ $t('Category') }}</td>
                            <td>{{ thesis.category.title }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.published_at">
                            <td>{{ $t('Published at') }}</td>
                            <td>{{ thesis.published_at }}</td>
                        </tr>
                        <tr class="subtitle-1" v-if="thesis.abstract">
                            <td class="col-2">{{ $t('Abstract') }}</td>
                            <td class="text-justify">{{ thesis.abstract }}</td>
                        </tr>
                        </tbody>
                    </v-simple-table>
                        <v-alert v-if="preReservation" type="info" outlined class="mt-3">
                            {{ $t('reservation.currentlyBorrowed') }}
                        </v-alert>
                        <v-alert v-if="!preReservation" type="success" outlined class="mt-3">
                            {{ $t('reservation.directBorrow') }}
                        </v-alert>
                    </v-card-text>
                    <v-divider></v-divider>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn
                            @click="createReservation"
                            :color="preReservation ? 'info' : 'success'" class="ma-3" x-large
                        >{{ preReservation ? $t('Create reservation') : $t('Borrow thesis') }}</v-btn>
                    </v-card-actions>
                </v-form>
            </v-card>
        </v-dialog>

    </span>
</template>
<script type="text/tsx">
import _ from 'lodash';
import {RESERVATION_ACTIONS} from '../../store/reservation';
import {optionsStore, reservationStore, thesisStore} from '../../store/store';
import {THESIS_ACTIONS} from '../../store/thesis';
import {notificationBus} from '../../utils';

export default {
  name: 'ThesisListActionBtn',
  props: {
    thesis: {type: Object, required: true},
    loading: {type: Boolean}
  },
  data() {
    return {
      dialogLoading: false,
      sendToReviewDialog: false,
      submitExternalReviewDialog: false,
                createReservationDialog: false,
                preReservation: false,

                externalReview: {
                    reviewer: null,
                    review: null
                },
                externalReviewSelectedReviewer: null
            };
        },
        computed: {
            ...thesisStore.mapGetters(['availableExternalReviewersOptions']),
            ...optionsStore.mapGetters(['typeAttachmentAcceptTypes']),
            availableExternalReviewers() {
                return this.availableExternalReviewersOptions(this.thesis);
            }
        },
        methods: {
            ...thesisStore.mapActions([
                THESIS_ACTIONS.SUBMIT_EXTERNAL_REVIEW,
                THESIS_ACTIONS.PUBLISH_THESIS,
                THESIS_ACTIONS.SEND_TO_REVIEW,
                THESIS_ACTIONS.SEND_TO_SUBMIT
            ]),
            ...reservationStore.mapActions([
                RESERVATION_ACTIONS.CREATE_RESERVATION
            ]),
            getAttachment(type) {
                return _.find(this.thesis.attachments, {type_attachment: {identifier: type}});
            },
            async submitExternalReview() {
                this.dialogLoading = true;

                const data = await this[THESIS_ACTIONS.SUBMIT_EXTERNAL_REVIEW]({
                    thesis_id: this.thesis.id,
                    review: this.externalReview
                });

                if (data.id) {
                    notificationBus.success(this.$t('review.external.justSubmitted'));
                    this.submitExternalReviewDialog = false;
                } else {
                    notificationBus.warning(this.$t('review.external.submitFailed'));
                }

                this.dialogLoading = false;
            },
            async sendToReview() {
                this.dialogLoading = true;

                const data = await this[THESIS_ACTIONS.SEND_TO_REVIEW]({thesis_id: this.thesis.id});

                if (data.id) {
                    notificationBus.success(this.$t('thesis.justSentToReview'));
                    this.sendToReviewDialog = false;
                    this.dialogLoading = false;
                }
            },
            async sendToSubmit() {
                this.dialogLoading = true;

                const data = await this[THESIS_ACTIONS.SEND_TO_SUBMIT]({thesis_id: this.thesis.id});

                if (data.id) {
                    notificationBus.success(this.$t('thesis.justSentToSubmit'));
                    this.dialogLoading = false;
                }
            },
            async createReservation() {
                this.dialogLoading = true;

                const data = await this[RESERVATION_ACTIONS.CREATE_RESERVATION]({thesis_id: this.thesis.id});

                if (data.id) {
                    notificationBus.success(this.$t('reservation.justCreated'));
                    this.createReservationDialog = false;
                } else {
                    notificationBus.warning(data.toString());
                }

                this.dialogLoading = false;
            },
            async publish() {
                const response = await this[THESIS_ACTIONS.PUBLISH_THESIS](this.thesis.id);
                if (response.data.id) {
                    notificationBus.success(this.$t('thesis.justPublished'));
                } else {
                    notificationBus.warning(response.data.non_field_errors.join('\n'));
                }
            }
        }
    };
</script>