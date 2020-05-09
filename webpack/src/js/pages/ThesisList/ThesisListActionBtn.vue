<template>
    <span>
        <template v-if="thesis.state === 'published'">
            <v-btn
                v-if="thesis.reservable && thesis.available_for_reservation"
                v-text="$t('Borrow')"
                small color="info" outlined
            ></v-btn>
            <v-btn
                v-if="thesis.reservable && !thesis.available_for_reservation && thesis.open_reservations_count === 1"
                v-text="$t('Make pre-reservation')"
                small color="info" outlined
            ></v-btn>
            <v-btn
                v-if="thesis.reservable && !thesis.available_for_reservation && thesis.open_reservations_count > 1"
                v-text="$t('Borrowed')"
                x-small depressed
            ></v-btn>
            <v-btn
                v-if="!thesis.reservable"
                v-text="$t('Not reservable')"
                x-small depressed
            ></v-btn>
        </template>
        <v-btn
            v-if="thesis.state === 'submitted'"
            v-text="$t('Send to review')"
            small color="primary" elevation="0"
            @click="sendToReviewDialog = true"
            v-has-perm:thesis.change_thesis
        ></v-btn>

        <v-btn
            v-if="thesis.state === 'reviewed'"
            v-text="$t('Publish')"
            small color="primary" elevation="0"
            @click="publishDialog = true"
            v-has-perm:thesis.change_thesis
        ></v-btn>

        <v-btn
            v-if="thesis.state === 'ready_for_submit'"
            v-text="$t('Waiting for submit')"
            x-small depressed disabled
            v-has-perm:thesis.change_thesis
        ></v-btn>

        <v-btn
            v-if="thesis.state === 'ready_for_review'"
            x-small depressed disabled
            v-has-perm:thesis.change_thesis
        >{{ $t('Waiting for review') }} ({{ 2 - thesis.reviews.length }})</v-btn>

        <v-dialog v-model="sendToReviewDialog" :max-width="$vuetify.breakpoint.mdAndDown ? '95vw' : '50vw'">
            <v-card :loading="loading">
                <v-card-title
                    class="headline grey lighten-2"
                    primary-title
                >{{ thesis.title }}</v-card-title>
                <v-card-text class="pt-3">
                    <v-simple-table>
                        <tbody>
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
                    <v-subheader class="ma-3">{{ $t('After sending thesis to review, opponent and supervisor will be able to download the thesis and fill their reviews.') }}</v-subheader>
                    <v-spacer></v-spacer>
                    <!-- TODO: AJAX call, you know it man-->
                    <v-btn
                        color="success" class="ma-3" x-large
                        @click="sendToReview"
                        :disabled="!(thesis.opponent && thesis.supervisor)"
                    >{{ $t('Send to review') }}</v-btn>
                </v-card-actions>
              </v-card>
        </v-dialog>
    </span>
</template>
<script type="text/tsx">
    import _ from 'lodash';
    import Axios from '../../axios';
    import {eventBus} from '../../utils';

    export default {
        name: 'ThesisListActionBtn',
        props: {
            thesis: {}
        },
        data() {
            return {
                loading: false,
                sendToReviewDialog: false,
                publishDialog: false
            };
        },
        methods: {
            getAttachment(type) {
                return _.find(this.thesis.attachments, {type_attachment: {identifier: type}});
            },
            async sendToReview() {
                this.loading = true;

                await Axios.patch(`/api/v1/thesis/${this.thesis.id}/send_to_review`);
                eventBus.flash({color: 'success', text: this.$t('Thesis has been sent to supervisor and opponent.')});
                this.sendToReviewDialog = false;
                this.loading = false;

                this.$emit('reload');
            }
        },
    };
</script>