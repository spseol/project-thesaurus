<template>
        <v-card :loading="loading">
            <v-card-title>
                {{ $t('Thesis review') }}

                <v-btn
                    @click="$router.back()" v-if="canBack"
                    outlined text small rounded class="ml-3"
                >
                    <v-icon small class="mr-1">mdi-arrow-left-bold-circle-outline</v-icon>
                    {{ $t('Back to theses') }}
                </v-btn>
            </v-card-title>
            <v-card-text>
                <!-- TODO: disable all? https://stackoverflow.com/a/55915597 -->
                <v-form @submit.prevent="submit" v-model="valid">
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-text-field
                                :label="$t('Student name')" :value="thesis.authors.map(a => a.full_name).join(', ')"
                                readonly filled disabled
                            ></v-text-field>

                            <v-text-field
                                :label="$t('Thesis name')" :value="thesis.title"
                                readonly filled disabled
                            ></v-text-field>

                            <v-text-field
                                :label="$t('Review author')" :suffix="$t(reviewerRole)"
                                :value="(thesis[reviewerRole] || {full_name: $t('Unknown')}).full_name"
                                readonly filled disabled
                            ></v-text-field>
                            <v-row no-gutters justify="center" class="mb-5">
                                <v-btn
                                    v-for="attachment in thesis.attachments" :key="attachment.id"
                                    :href="attachment.url"
                                    color="primary" target="_blank" outlined class="ma-2"
                                >
                                    <v-icon color="grey" class="mr-2">
                                        ${{ attachment.type_attachment.identifier }}
                                    </v-icon>
                                    {{ attachment.type_attachment.name }}
                                </v-btn>
                            </v-row>
                            <div v-if="showComments">
                              <v-divider></v-divider>
                              <h3
                                  class="my-5"
                                  :class="{'error--text': error_messages.comment}"
                              >{{ $t('Review comment') }}</h3>
                              <tiptap-vuetify
                                  v-model="review.comment"
                                  :placeholder="$t('review.commentPlaceholder')"
                                  :extensions="tipTapExtensions" :disabled="disabled"
                                  :card-props="{flat: true, outlined: true, solo: true}"
                                  minHeight="200px"
                                  :editor-properties="{autoFocus: true}"
                                  :toolbar-properties="{dark: !$vuetify.theme.dark}"
                                  class="mb-5"
                              ></tiptap-vuetify>
                              <v-alert
                                  v-for="m of error_messages.comment"
                                  dense outlined text type="error"
                                  v-text="m" class="mt-4"
                              ></v-alert>

                              <h3
                                  class="mb-5"
                                  :class="{'error--text': error_messages.questions}"
                              >{{ $t('Thesis defence questions') }}</h3>
                              <tiptap-vuetify
                                  v-model="review.questions" :disabled="disabled"
                                  :placeholder="$t('review.questionsPlaceholder')"
                                  :extensions="tipTapExtensions"
                                  :card-props="{flat: true, outlined: true, solo: true}"
                                  minHeight="150px"
                                  :toolbar-properties="{dark: !$vuetify.theme.dark}"
                              ></tiptap-vuetify>
                              <v-alert
                                  v-for="m of error_messages.questions"
                                  dense outlined text type="error"
                                  v-text="m" class="mt-4"
                              ></v-alert>
                            </div>
                        </v-col>
                        <v-col class="d-flex flex-column justify-space-between" cols="12" md="6">
                            <div>
                                <v-chip
                                    :color="valueToColor(review.difficulty, 3)"
                                    v-text="$t('Difficulty of selected topic')"
                                    text-color="grey darken-4"
                                ></v-chip>
                              <v-slider
                                  :color="valueToColor(review.difficulty, 3)"
                                  :max="3" :min="0" :step="1" :rules="[v => v > 0]"
                                  :thumb-color="valueToColor(review.difficulty, 3)"
                                  :tick-labels="grades3"
                                  class="VSliderCustom__label--grey"
                                  ticks="always" track-color="grey" :thumb-size="48" :tick-size="4"
                                  v-model="review.difficulty" :disabled="disabled"
                              ></v-slider>

                              <div v-for="(grade, i) in review.grades">
                                <v-chip
                                    :color="valueToColor(grade, 4)" class="mt-7"
                                    v-text="gradings[i]" text-color="grey darken-4"
                                ></v-chip>
                                <v-slider
                                    :min="0" :max="4" :step="1"
                                    :rules="[v => v > 0]"
                                    :thumb-color="valueToColor(grade, 4)"
                                    :color="valueToColor(grade, 4)"
                                    :tick-labels="grades4" ticks="always" track-color="grey"
                                    class="VSliderCustom__label--grey" :thumb-size="48" :tick-size="4"
                                    v-model="review.grades[i]" :disabled="disabled"
                                ></v-slider>
                              </div>
                            </div>
                            <div>
                                <v-divider></v-divider>
                                <v-radio-group
                                    :label="$t('Classification proposal')" row
                                    :rules="[v => !!v]"
                                    v-model="review.grade_proposal" :disabled="disabled"
                                >
                                  <v-spacer></v-spacer>
                                  <v-radio
                                      :color="valueToColor(4 - review.grade_proposal, 4)"
                                      :key="value"
                                      :label="text"
                                      :value="value"
                                      v-for="[value, text] in gradeProposalOptions"

                                  >
                                    <template v-slot:label>
                                        <span
                                            v-text="text"
                                            :style="{
                                              color: review.grade_proposal === value ?
                                                valueToColor(4 - review.grade_proposal, 4) : undefined
                                            }"
                                        />
                                    </template>
                                  </v-radio>
                                </v-radio-group>
                                <v-row no-gutters v-if="!this.review.id">
                                    <v-checkbox
                                        :label="$t('review.submitHint')"
                                        :rules="[v => !!v]"
                                        class="font-weight-bold"
                                        :hide-details="!non_field_error_messages"
                                        :error-messages="non_field_error_messages"
                                    ></v-checkbox>
                                    <v-spacer></v-spacer>
                                    <v-btn :disabled="!valid" color="success" type="submit" x-large>
                                        {{ $t('Submit') }}
                                    </v-btn>
                                </v-row>
                                <v-row no-gutters v-if="this.review.id">
                                    <v-alert type="info" outlined width="100%">
                                        {{$t('review.submittedAt')}}
                                        {{ (new Date(this.review.created)).toLocaleString($i18n.locale) }}.
                                    </v-alert>
                                </v-row>
                            </div>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-card-text>
                <p>{{ $t('review.gradingNote') }}</p>
            </v-card-text>
        </v-card>

</template>

<script type="text/tsx">
import _ from 'lodash';
import {Bold, BulletList, History, Italic, Link, ListItem, TiptapVuetify} from 'tiptap-vuetify';
import Axios from '../../axios';
import {DASHBOARD_ACTIONS} from '../../store/dashboard';
import {dashboardStore} from '../../store/store';
import {hasPerm} from '../../user';
import {GRADE_COLOR_SCALE_3, GRADE_COLOR_SCALE_4, notificationBus, pageContext} from '../../utils';


export default {
  name: 'ReviewForm',
  components: {TiptapVuetify},
  props: {
    thesisLoaded: {
      type: Object,
      required: true
    },
    reviewLoaded: {
      type: Object,
      required: false
            }
        },
        data() {
            // @ts-ignore
            const $t = (key) => this.$t(key);
            return {
              thesis: {authors: [], opponent: {}, supervisor: {}},
              tipTapExtensions: [History, Link, Bold, Italic, BulletList, ListItem],
              loading: false,
              valid: true,
              non_field_error_messages: [],
              error_messages: {},
              review: {
                difficulty: 0,
                grade_proposal: 0,
                grades: _.times(this.reviewerRole == 'supervisor' ? 6 : 5, () => 0),
                comment: null,
                questions: null
              }
            };
        },
        computed: {
            grades4() {
              return [
                '',
                this.$t('Not sufficient'),
                this.$t('Great'),
                this.$t('grades.veryWell'),
                this.$t('Excellent')
              ];
            },
            grades3() {
              return [
                '',
                this.$t('Under average'),
                this.$t('Average'),
                this.$t('Over average')
              ];
            },
            reviewerRole() {
                return {
                    [this.thesis.supervisor?.username]: 'supervisor',
                    [this.thesis.opponent?.username]: 'opponent'
                }[this.review?.user?.username || pageContext.user.username];
            },
            gradings() {
                return _.compact([
                    this.reviewerRole == 'supervisor' ? this.$t('Students independence during processing') : null,
                    this.$t('Theoretical part of the work, comprehensibility of the text'),
                    this.$t('Methods and procedures used'),
                    this.$t('Formal editing, work with sources, citations in the text'),
                    this.$t('Graphic design of the thesis'),
                    this.$t('Interpretation of conclusions, their originality and their own contribution to the work')
                ]);
            },
            gradeProposalOptions() {
              // plus one because select does have empty option as first one
              return _.map(_.compact(this.grades4), (grade, i) => ([1 + i, grade]));
            },
            disabled() {
                return !!this.review.id;
            },
            canBack() {
                return window.history.length > 1;
            }
        },
        asyncComputed: {
            showComments: {
                async get() {
                    return (await hasPerm('review.add_review')) ||
                        !!_.find(this.thesis.authors, {id: pageContext.user.id});
                },
                default: false
            }
        },
        methods: {
            ...dashboardStore.mapActions([
                DASHBOARD_ACTIONS.LOAD_DASHBOARD
            ]),
            valueToColor(v, scale = 3) {
                return (scale === 3 ? GRADE_COLOR_SCALE_3 : GRADE_COLOR_SCALE_4)[v];
            },
            async submit() {
                this.loading = true;
                const resp = (await Axios.post('/api/v1/review',
                    {
                        ...this.review,
                        thesis: this.thesis.id
                    }
                )).data;
                this.loading = false;

                if (resp.id) {
                    notificationBus.success(this.$t('review.justSubmitted'));
                    await this.$router.push(this.$i18nRoute({name: 'dashboard'}));
                } else {
                  this.error_messages = resp;
                  this.non_field_error_messages = resp.non_field_errors;
                }
            }
        },
        watch: {
            thesisLoaded(to) {
                this.thesis = Object.assign({}, this.thesis, _.cloneDeep(to));
            },
            reviewLoaded(to) {
                this.review = Object.assign({}, this.review, _.cloneDeep(to));
            }
        }
    };
</script>

