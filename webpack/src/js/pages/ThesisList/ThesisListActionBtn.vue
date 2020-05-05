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
            v-text="$t('Waiting for review')"
            x-small depressed disabled
            v-has-perm:thesis.change_thesis
        ></v-btn>

        <v-dialog v-model="sendToReviewDialog" max-width="40vw">
            <v-card>
                <v-card-title
                    class="headline grey lighten-2"
                    primary-title
                >{{ $t('Send to review') }}</v-card-title>
                <v-card-text class="pt-3">
                    <div class="title">
                        {{ thesis.title }}
                    </div>
                    <div class="subtitle-1">
                        {{ $tc('Authors', thesis.authors.length) }}: {{ thesis.authors.map(a => a.full_name).join(', ') }}
                    </div>
                    <div class="subtitle-1">
                        {{ $tc('Supervisor') }}: {{ thesis.supervisor.full_name }}
                    </div>
                    <div class="subtitle-1">
                        {{ $tc('Opponent') }}: {{ thesis.opponent.full_name }}
                    </div>
                    <div class="subtitle-1" v-if="thesisTextAttachment">
                        {{ $tc('Thesis text') }}: <v-btn text :to="thesisTextAttachment.url">{{ $t('Download') }}</v-btn>
                    </div>
                </v-card-text>
                <v-divider></v-divider>
                <v-card-actions>
                  <v-spacer></v-spacer>
                  <v-btn
                      color="success"
                      @click="sendToReviewDialog = false"
                  >{{ $t('Send to review') }}</v-btn>
                </v-card-actions>
              </v-card>
        </v-dialog>
    </span>
</template>
<script>
    import _ from 'lodash';

    export default {
        name: 'ThesisListActionBtn',
        props: {
            thesis: {},
        },
        data() {
            return {
                sendToReviewDialog: false,
                publishDialog: false,
            };
        },
        computed: {
            thesisTextAttachment() {
                return _.find(this.thesis.attachments, {type_attachment: {identifier: 'thesis_text'}});
            },
        },
    };
</script>