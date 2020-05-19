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
            <span v-has-group:teacher>
                <span v-has-perm:thesis.change_reservation
                    v-if="thesis.reservable"
                >
                    <v-badge :content="thesis.open_reservations_count || 0" overlap v-if="thesis.open_reservations_count > 0">
                        <v-btn
                            v-text="$t('Borrowed')" :to="$i18nRoute({name: 'reservation-list'})"
                            x-small depressed
                        ></v-btn>
                    </v-badge>

                    <v-btn v-if="thesis.available_for_reservation"
                        v-text="$t('Available')"
                        x-small depressed
                    ></v-btn>
                </span>
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
            v-if="thesis.state === 'submitted'"
            v-text="$t('Send to review')"
            small color="primary" elevation="0"
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

        <template v-if="thesis.state === 'ready_for_review'" v-has-perm:thesis.change_thesis>
            <v-hover v-slot:default="{ hover }" style="min-width: 15em">
                <v-badge
                    color="primary" overlap :value="!hover"
                    :content="availableExternalReviewersOptions.length"
                >
                    <!-- TODO: detect external/internal s/o -->
                    <v-btn
                        v-if="!hover"
                        small depressed disabled block
                    >{{ $t('Waiting for review') }}</v-btn>
                    <v-btn
                        v-if="hover" @click="submitExternalReviewDialog = true"
                        small depressed outlined color="info" block
                    >{{ $t('Submit external review') }}</v-btn>
                </v-badge>
            </v-hover>
        </template>

        <v-dialog v-model="sendToReviewDialog" :max-width="$vuetify.breakpoint.mdAndDown ? '95vw' : '50vw'">
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

        <v-dialog v-model="submitExternalReviewDialog" :max-width="$vuetify.breakpoint.mdAndDown ? '95vw' : '35vw'">
            <v-card :loading="dialogLoading">
                <v-form>
                    <v-card-title
                        class="headline grey lighten-2"
                        primary-title
                    >{{ thesis.title }}</v-card-title>
                    <v-card-text class="pt-3 d-flex flex-column">
                        <v-file-input
                            accept="application/pdf"
                            :label="$t('External review')"
                            v-model="externalReview.review"
                        ></v-file-input>
                        <v-btn-toggle
                            group class="align-self-center"
                            mandatory color="primary"
                            v-model="externalReview.reviewer"
                        >
                            <v-btn
                                v-for="[key, user] in availableExternalReviewersOptions"
                                :key="key" :value="key"
                            >
                                <strong>{{ $t(key) }}</strong>: {{ user.full_name }}
                            </v-btn>
                        </v-btn-toggle>
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

        <v-dialog v-model="createReservationDialog" :max-width="$vuetify.breakpoint.mdAndDown ? '95vw' : '35vw'">
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
    import Axios from '../../axios';
    import {eventBus, readFileAsync} from '../../utils';

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
            availableExternalReviewersOptions() {
                return _.map(_.filter(
                    ['supervisor', 'opponent'],
                    (key) => (
                        // show option to upload if:
                        !_.find( // does not already have uploaded review
                            this.thesis.attachments,
                            {
                                type_attachment: {identifier: `${key}_review`}
                            }
                        ) && // and
                        this.thesis[key]?.id && // has set user
                        !_.find( // but without internal review
                            this.thesis.reviews,
                            {
                                user: {id: this.thesis[key].id}
                            }
                        )
                    )
                    // format to [key, User]
                ), (k) => [k, this.thesis[k]]);
            }
        },
        methods: {
            getAttachment(type) {
                return _.find(this.thesis.attachments, {type_attachment: {identifier: type}});
            },
            async submitExternalReview() {
                this.dialogLoading = true;

                let formData = new FormData();

                await readFileAsync(this.externalReview.review);
                formData.append('review', this.externalReview.review);
                formData.append('reviewer', this.externalReview.reviewer);

                const resp = await Axios.post(`/api/v1/thesis/${this.thesis.id}/submit_external_review`, formData, {
                    headers: {'Content-Type': 'multipart/form-data'}
                });

                if (resp.data.id) {
                    eventBus.flash({
                        text: this.$t('review.external.justSubmitted')
                    });
                    this.submitExternalReviewDialog = false;
                } else {
                    eventBus.flash({
                        text: this.$t('review.external.submitFailed')
                    });
                }

                this.$emit('reload');
                this.dialogLoading = false;
            },
            async sendToReview() {
                this.dialogLoading = true;

                await Axios.patch(`/api/v1/thesis/${this.thesis.id}/send_to_review`);
                eventBus.flash({color: 'success', text: this.$t('thesis.justSentToReview')});
                this.sendToReviewDialog = false;
                this.dialogLoading = false;

                this.$emit('reload');
            },
            async createReservation() {
                this.dialogLoading = true;

                const {data} = await Axios.post(`/api/v1/reservation`, {
                    thesis: this.thesis.id
                });
                if (data.id) {
                    eventBus.flash({color: 'success', text: this.$t('reservation.justCreated')});
                    this.createReservationDialog = false;
                } else {
                    eventBus.flash({color: 'primary', text: data.toString()});
                }

                this.dialogLoading = false;

                this.$emit('reload');
            },
            async publish() {
                await Axios.patch(`/api/v1/thesis/${this.thesis.id}/publish`);
                eventBus.flash({color: 'success', text: this.$t('thesis.justPublished')});

                this.$emit('reload');
            }
        }
    };
</script>