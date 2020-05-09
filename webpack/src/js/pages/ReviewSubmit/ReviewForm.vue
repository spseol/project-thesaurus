<template>
    <v-container fluid>
        <v-card :loading="loading">
            <v-card-title>{{ $t('Thesis review') }}</v-card-title>
            <v-card-text>
                <!-- TODO: https://stackoverflow.com/a/55915597-->
                <v-form @submit.prevent="submit" v-model="valid">
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-text-field
                                :label="$t('Student name')" :value="thesis.authors.map(a => a.full_name).join(', ')"
                                disabled
                                filled
                            ></v-text-field>

                            <v-text-field
                                :label="$t('Thesis name')" :value="thesis.title"
                                disabled
                                filled
                            ></v-text-field>

                            <v-text-field
                                :label="$t('Review author')" :suffix="$t(reviewerRole)"
                                :value="(thesis[reviewerRole] || {full_name: $t('Unknown')}).full_name"
                                disabled
                                filled
                            ></v-text-field>
                            <v-row class="mb-4" no-gutters v-if="thesisTextAttachment">
                                <v-spacer></v-spacer>
                                <v-btn :href="thesisTextAttachment.url" color="info" large target="_blank">
                                    {{ $t('Download thesis text') }}
                                </v-btn>
                                <v-spacer></v-spacer>
                            </v-row>
                            <v-textarea
                                :label="$t('Review comment')"
                                :rules="[v => !!v]"
                                outlined
                                rows="14"
                                v-model="review.comment"
                            ></v-textarea>
                            <v-textarea
                                :label="$t('Thesis defence questions')"
                                hide-details
                                outlined
                                rows="8"
                                v-model="review.questions"
                            ></v-textarea>
                        </v-col>
                        <v-col class="d-flex flex-column justify-space-between" cols="12" md="6">
                            <div>
                                <v-chip
                                    :color="valueToColor(review.difficulty, 3)"
                                    v-text="$t('Difficulty of selected topic')"
                                ></v-chip>
                                <v-slider
                                    :color="valueToColor(review.difficulty, 3)"
                                    :max="3"
                                    :min="0"
                                    :rules="[v => v > 0]"
                                    :step="1"
                                    :thumb-color="valueToColor(review.difficulty, 3)"
                                    :tick-labels="grades3"
                                    class="VSliderCustom__label--gray"
                                    ticks="always"
                                    track-color="grey"
                                    v-model="review.difficulty"
                                ></v-slider>

                                <div v-for="(grade, i) in review.grades">
                                    <v-chip
                                        :color="valueToColor(grade, 4)"
                                        class="mt-7" v-text="gradings[i]"
                                    ></v-chip>
                                    <v-slider
                                        :color="valueToColor(grade, 4)"
                                        :max="4"
                                        :min="0"
                                        :rules="[v => v > 0]"
                                        :step="1"
                                        :thumb-color="valueToColor(grade, 4)"
                                        :tick-labels="grades4"
                                        class="VSliderCustom__label--gray"
                                        ticks="always"
                                        track-color="grey"
                                        v-model="review.grades[i]"
                                    ></v-slider>
                                </div>
                            </div>
                            <div>
                                <v-divider></v-divider>
                                <v-radio-group
                                    :label="$t('Classification proposal')"
                                    :rules="[v => !!v]"
                                    row
                                    v-model="review.grade_proposal"
                                >
                                    <v-spacer></v-spacer>
                                    <v-radio
                                        :color="valueToColor(review.grade_proposal, 4)"
                                        :key="value" :label="text" :value="value"
                                        v-for="[value, text] in gradeProposalOptions"
                                    ></v-radio>
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
                            </div>
                        </v-col>
                    </v-row>
                </v-form>
            </v-card-text>
            <v-card-text>
                <p>{{ $t('review.gradingNote') }}</p>
            </v-card-text>
        </v-card>
    </v-container>

</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';
    import {eventBus, GRADE_COLOR_SCALE_3, GRADE_COLOR_SCALE_4, pageContext} from '../../utils';


    export default Vue.extend({
        name: 'ReviewForm',
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
                loading: false,
                valid: true,
                non_field_error_messages: [],
                grades4: [$t('Excellent'), $t('Very well'), $t('Great'), $t('Not sufficient'), ''].reverse(),
                grades3: [$t('Over average'), $t('Average'), $t('Under average'), ''].reverse(),
                review: {
                    difficulty: 0,
                    grade_proposal: 0,
                    grades: _.times(this.reviewingUserRole == 'supervisor' ? 6 : 5, () => 0),
                    comment: null,
                    questions: null
                }
            };
        },
        computed: {
            reviewerRole() {
                return {
                    [this.thesis.supervisor?.username]: 'supervisor',
                    [this.thesis.opponent?.username]: 'opponent'
                }[this.review?.user?.username || pageContext.username];
            },
            gradings() {
                return _.compact([
                    this.reviewingUserRole == 'supervisor' ? this.$t('Students independence during processing') : null,
                    this.$t('Theoretical part of the work, comprehensibility of the text'),
                    this.$t('Methods and procedures used'),
                    this.$t('Formal editing, work with sources, citations in the text'),
                    this.$t('Graphic design of the thesis'),
                    this.$t('Interpretation of conclusions, their originality and their own contribution to the work')
                ]);
            },
            thesisTextAttachment() {
                return _.find(this.thesis.attachments, {type_attachment: {identifier: 'thesis_text'}});
            },
            gradeProposalOptions() {
                return _.map(_.reverse(_.compact(this.grades4)), (grade, i) => ([4 - i, grade]));
            }
        },
        methods: {
            valueToColor(v, scale = 3) {
                return (scale === 3 ? GRADE_COLOR_SCALE_3 : GRADE_COLOR_SCALE_4)[v];
            },
            async submit() {
                this.loading = true;
                // TODO: editation?
                const resp = (await Axios.post('/api/v1/review',
                    {
                        ...this.review,
                        thesis: this.thesis.id
                    }
                )).data;
                this.loading = false;

                if (resp.id) {
                    eventBus.flash({text: this.$t('Review has been submitted.')});
                    this.$router.push({name: 'dashboard'});
                } else {
                    this.messages = resp;
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
    });
</script>
