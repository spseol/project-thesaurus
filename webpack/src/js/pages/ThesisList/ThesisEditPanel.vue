<template>
    <v-card :loading="loading">
        <v-form @submit.prevent="submit">
            <v-card-title>{{ $t('Thesis edit') }}</v-card-title>
            <v-divider></v-divider>
            <v-card-text>
                <v-row no-gutters>
                    <v-col class="mr-3">
                        <v-card elevation="0" outlined>
                            <v-card-subtitle class="font-weight-bold">{{ $t('Base info') }}</v-card-subtitle>
                            <v-card-text>
                                <v-text-field
                                    :label="$t('Title')" v-model="data.title" :rules="[v => !!v]"
                                    :error-messages="messages.title"
                                ></v-text-field>

                                <v-text-field
                                    :label="$t('Registration number')" v-model="data.registration_number"
                                    :counter="4" :error-messages="messages.registration_number"
                                    :rules="[v => !v || /[A-Z]\d{3}/.test(v) || $t('thesis.invalidSNformat')]"
                                ></v-text-field>

                                <v-menu
                                    :close-on-content-click="false"
                                    transition="scale-transition"
                                    offset-y max-width="290px"
                                >
                                    <template v-slot:activator="{ on }">
                                        <v-text-field
                                            v-model="data.published_at" v-on="on"
                                            :label="$t('Published')" readonly
                                            append-icon="mdi-calendar"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="data.published_at"
                                        type="month" no-title scrollable
                                    ></v-date-picker>
                                </v-menu>

                                <v-menu
                                    :close-on-content-click="false"
                                    transition="scale-transition"
                                    offset-y max-width="290px"
                                >
                                    <template v-slot:activator="{ on }">
                                        <v-text-field
                                            v-on="on"
                                            :value="toHumanDeadline(data.submit_deadline)"
                                            :label="$t('Submit deadline')" readonly
                                            append-icon="mdi-calendar"
                                        ></v-text-field>
                                    </template>
                                    <v-date-picker
                                        v-model="data.submit_deadline"
                                        type="date" no-title scrollable
                                    ></v-date-picker>
                                </v-menu>

                                <v-radio-group
                                    :label="$t('Category')" row :error-messages="messages.category"
                                    v-model="data.category.id" :rules="[v => !!v]"
                                >
                                    <v-radio
                                        v-for="{text, value} in optionsStore.category"
                                        :label="text" :value="value" :key="value"
                                    ></v-radio>
                                </v-radio-group>

                                <v-autocomplete
                                    v-model="data.supervisor.id"
                                    :items="optionsStore.teacher" hide-no-data
                                    :label="$t('Supervisor')"
                                    :rules="[v => !!v]" :error-messages="messages.supervisor_id"
                                ></v-autocomplete>

                                <v-autocomplete
                                    v-model="data.opponent.id"
                                    :items="optionsStore.teacher" hide-no-data
                                    :label="$t('Opponent')"
                                    :rules="[v => !!v]" :error-messages="messages.opponent_id"
                                ></v-autocomplete>

                                <v-autocomplete
                                    v-model="data.authors"
                                    :loading="loading"
                                    :items="studentOptions"
                                    :search-input.sync="search"
                                    cache-items multiple chips clearable deletable-chips small-chips
                                    :label="$t('Author(s)')" :error-messages="messages.authors"
                                    :rules="[v => v.length > 0]"
                                ></v-autocomplete>
                            </v-card-text>
                        </v-card>
                    </v-col>
                    <v-col class="ml-3">
                        <v-card elevation="0" outlined>
                            <v-card-subtitle class="font-weight-bold">{{ $t('State') }}</v-card-subtitle>
                            <v-card-text>
                                <v-select
                                    :items="optionsStore.thesisState" v-model="data.state"
                                    :hint="stateHint"
                                    persistent-hint flat solo outlined dense
                                    :error-messages="messages.state"
                                ></v-select>
                            </v-card-text>
                        </v-card>

                        <v-card elevation="0" class="mt-3" outlined>
                            <v-card-subtitle class="font-weight-bold">{{ $t('Reviews') }}</v-card-subtitle>
                            <v-card-text>
                                <v-row v-for="rew in thesis.reviews" :key="rew.id"
                                    class="pa-3 justify-space-between">
                                    <span>
                                        {{ rew.user.full_name }}
                                    </span>
                                    <span class="text-right">
                                        <v-btn text outlined small color="info" :href="rew.url" target="_blank">
                                            <v-icon small class="mr-1">mdi-eye</v-icon>
                                            {{ $t('View') }}
                                        </v-btn>
                                        <v-dialog v-model="rew._deleteDialog" max-width="30em">
                                            <template v-slot:activator="{on}">
                                                <v-btn outlined color="error" small v-on="on">
                                                    <v-icon small>mdi-trash-can-outline</v-icon>
                                                </v-btn>
                                            </template>
                                            <v-card :loading="rew._loading">
                                                <v-card-title>
                                                    {{ $t('Delete review from') }}
                                                    {{ rew.user.full_name }}
                                                </v-card-title>
                                                <v-card-text>
                                                    {{ $t('thesis.deleteReviewQuestion') }}
                                                    <strong>{{ thesis.title }}</strong>?
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn
                                                        color="error" large
                                                        @click="deleteReview(rew)" :loading="rew._loading"
                                                    >
                                                        {{ $t('Yes, delete') }}
                                                    </v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>
                                    </span>
                                </v-row>
                                <v-alert color="info" text v-if="!thesis.reviews.length">
                                    {{ $t('thesis.noReviews') }}
                                </v-alert>
                            </v-card-text>
                        </v-card>

                        <v-card elevation="0" class="mt-3" outlined>
                            <v-card-subtitle class="font-weight-bold">{{ $t('Attachments') }}</v-card-subtitle>
                            <v-card-text>
                                <v-row
                                    v-for="att in thesis.attachments" :key="att.id"
                                    class="pa-3 justify-space-between"
                                >
                                    <span class="d-flex align-center">
                                        <v-icon class="mr-1">${{ att.type_attachment.identifier }}</v-icon>
                                        {{ att.type_attachment.name }}
                                        <span class="caption ml-1">({{ att.size_label }})</span>
                                    </span>
                                    <span class="text-right">
                                        <v-btn text outlined small color="info" :href="att.url" target="_blank">
                                            <v-icon small class="mr-1">mdi-eye</v-icon>
                                            {{ $t('View') }}
                                        </v-btn>
                                        <v-dialog v-model="att._deleteDialog" max-width="30em">
                                            <template v-slot:activator="{on}">
                                                <v-btn outlined color="error" small v-on="on">
                                                    <v-icon small>mdi-trash-can-outline</v-icon>
                                                </v-btn>
                                            </template>
                                            <v-card>
                                                <v-card-title>
                                                    {{ $t('Delete attachment') }}
                                                    {{ att.type_attachment.name }}
                                                </v-card-title>
                                                <v-card-text>
                                                    {{ $t('thesis.deleteAttachmentQuestion') }}
                                                    <strong>{{ thesis.title }}</strong>?
                                                </v-card-text>
                                                <v-card-actions>
                                                    <v-spacer></v-spacer>
                                                    <v-btn
                                                        color="error" large
                                                        @click="deleteAttachment(att)" :loading="att._loading"
                                                    >
                                                        {{ $t('Yes, delete') }}
                                                    </v-btn>
                                                </v-card-actions>
                                            </v-card>
                                        </v-dialog>
                                    </span>
                                </v-row>

                                <v-alert color="info" text v-if="!thesis.attachments.length">
                                    {{ $t('thesis.noAttachments') }}
                                </v-alert>
                            </v-card-text>
                        </v-card>

                        <v-card elevation="0" class="mt-3" outlined v-has-perm:attachment.add_attachment>
                            <v-card-subtitle class="font-weight-bold">{{ $t('New attachment') }}</v-card-subtitle>
                            <v-card-text>
                                <v-row class="align-end" no-gutters>
                                    <v-col cols="10">
                                        <v-select
                                            :label="$t('Type attachment')" hide-details prepend-icon="mdi-book-search-outline"
                                            :items="optionsStore.typeAttachment" item-text="name" item-value="id"
                                            v-model="newAttachment.type_attachment" return-object clearable
                                        ></v-select>
                                        <v-file-input
                                            :label="$t('New file')" hide-details show-size
                                            v-model="newAttachment.file" v-if="newAttachment.type_attachment"
                                            :accept="newAttachment.type_attachment.allowed_content_types.join(',')"
                                            :prepend-icon="`$${newAttachment.type_attachment.identifier}`"
                                        ></v-file-input>
                                    </v-col>
                                    <v-col cols="2" class="text-right">
                                        <v-btn
                                            :disabled="!newAttachment.type_attachment || !newAttachment.file"
                                            color="success" small class="ml-3"
                                            @click="uploadNewAttachment"
                                            :loading="newAttachment._loading"
                                        >
                                            <v-icon>mdi-upload</v-icon>
                                        </v-btn>
                                    </v-col>
                                </v-row>
                            </v-card-text>
                        </v-card>

                        <v-alert
                            v-for="msg in non_field_error_messages" :key="msg"
                            type="warning" text outlined class="mt-3"
                        >{{ msg }}
                        </v-alert>
                    </v-col>
                </v-row>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
                <audit-for-instance
                    model-name="thesis.Thesis" :model-pk="data.id"
                ></audit-for-instance>
                <v-spacer></v-spacer>
                <v-btn text type="button" large class="ma-2" @click="$emit('close')">{{ $t('Cancel edit') }}</v-btn>
                <v-btn color="success" type="submit" large class="ma-2">{{ $t('Save data') }}</v-btn>
            </v-card-actions>
        </v-form>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import moment from 'moment';
    import qs from 'qs';
    import Vue from 'vue';
    import {mapState} from 'vuex';
    import Axios from '../../axios';
    import AuditForInstance from '../../components/AuditForInstance.vue';
    import {ATTACHMENT_ACTIONS} from '../../store/attachment';
    import {attachmentStore, thesisStore} from '../../store/store';
    import {THESIS_ACTIONS} from '../../store/thesis';
    import {notificationBus} from '../../utils';

    export default Vue.extend({
        name: 'ThesisEditPanel',
        components: {AuditForInstance},
        props: {
            thesis: {type: Object}
        },
        data() {
            return {
                data: {},
                loading: false,
                search: '',
                studentOptions: [],
                messages: {},
                non_field_error_messages: [],
                newAttachment: {
                    type_attachment: null,
                    file: null,
                    _loading: false
                }
            };
        },
        watch: {
            async search(val) {
                val !== this.select && (await this.queryStudentOptions(val));
            }
        },
        methods: {
            ...thesisStore.mapActions([
                THESIS_ACTIONS.SAVE_THESIS,
                THESIS_ACTIONS.DELETE_REVIEW
            ]),
            ...attachmentStore.mapActions([
                ATTACHMENT_ACTIONS.DELETE_ATTACHMENT,
                ATTACHMENT_ACTIONS.UPLOAD_ATTACHMENT
            ]),
            async queryStudentOptions(search) {
                this.loading = true;

                this.studentOptions = (await Axios.get(`/api/v1/student-options?${qs.stringify({search})}`)).data;

                this.loading = false;
            },
            async submit() {
                this.loading = true;

                const resp = await this[THESIS_ACTIONS.SAVE_THESIS](this.data);

                if (resp.id) {
                    notificationBus.success(this.$t('thesis.justSaved'));
                    this.$emit('reload');
                } else {
                    this.messages = resp;
                    this.non_field_error_messages = resp.non_field_errors;
                }

                this.loading = false;
            },
            async deleteReview(review) {
                review._loading = true;
                await this[THESIS_ACTIONS.DELETE_REVIEW]({review_id: review.id, thesis_id: this.thesis.id});
                notificationBus.success(this.$t('review.justDeleted'));
                review._deleteDialog = false;
                review._loading = false;
            },
            async deleteAttachment(attachment) {
                attachment._loading = true;
                await this[ATTACHMENT_ACTIONS.DELETE_ATTACHMENT]({
                    attachment_id: attachment.id,
                    thesis_id: this.thesis.id
                });
                notificationBus.success(this.$t('attachment.justDeleted'));
                attachment._deleteDialog = false;
                attachment._loading = false;
            },
            async uploadNewAttachment() {
                this.newAttachment._loading = true;
                const data = await this[ATTACHMENT_ACTIONS.UPLOAD_ATTACHMENT]({
                    thesis_id: this.thesis.id,
                    attachment: this.newAttachment
                });

                if (data.id) {
                    notificationBus.success(this.$t('attachment.justAdded'));
                    this.newAttachment = {
                        type_attachment: null,
                        file: null
                    };
                    this.non_field_error_messages = [];
                } else {
                    this.non_field_error_messages = data;
                }
                this.newAttachment._loading = false;
            },
            toHumanDeadline(date) {
                return moment(date, null, this.$i18n.locale).endOf('day').format('L LT');
            }
        },
        computed: {
            ...mapState({optionsStore: 'options'}),
            stateHint() {
                return _.find(this.optionsStore.thesisState, {value: this.data.state})?.help_text;
            }
        },
        async created() {
            this.$watch('thesis', () => {
                const t = this.thesis;
                this.data = {
                    ...t,
                    // load v/o if present
                    opponent: {...(t.opponent || {id: null})},
                    supervisor: {...(t.supervisor || {id: null})},
                    authors: _.map(t.authors, 'id')
                };
            }, {immediate: true});
        }
    });
</script>
