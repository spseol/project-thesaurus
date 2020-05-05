<template>
    <v-container fluid>
        <v-card :loading="loading">
            <v-card-title>{{ $t('Thesis review') }}</v-card-title>
            <v-card-text>
                <v-form v-model="valid" @submit.prevent="submit" disabled="disabled">
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
                                :label="$t('Review author')" :suffix="$t(reviewingUserRole)"
                                :value="(thesis[reviewingUserRole] || {full_name: $t('Unknown')}).full_name"
                                disabled
                                filled
                            ></v-text-field>
                            <v-divider></v-divider>
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
                                >{{ $t('Difficulty of selected topic') }}
                                </v-chip>
                                <v-slider
                                    :color="valueToColor(review.difficulty, 3)"
                                    :max="3"
                                    :min="0"
                                    :rules="[v => v > 0]"
                                    :step="1"
                                    :thumb-color="valueToColor(review.difficulty, 3)"
                                    :tick-labels="grades3"
                                    :track-color="valueToColor(review.difficulty, 3)"
                                    class="VSliderCustom__label--gray"
                                    ticks="always"
                                    v-model="review.difficulty"
                                ></v-slider>

                                <div v-for="(grade, i) in review.grades">
                                    <v-chip
                                        :color="valueToColor(grade, 4)"
                                        class="mt-5"
                                    >{{ gradings[i] }}
                                    </v-chip>
                                    <v-slider
                                        :color="valueToColor(grade, 4)"
                                        :max="4"
                                        :min="0"
                                        :rules="[v => v > 0]"
                                        :step="1"
                                        :thumb-color="valueToColor(grade, 4)"
                                        :tick-labels="grades4"
                                        class="VSliderCustom__label--gray"
                                        color="info"
                                        ticks="always"
                                        track-color="grey"
                                        v-model="review.grades[i]"
                                    ></v-slider>
                                </div>
                            </div>
                            <div>
                                <v-divider></v-divider>
                                <v-checkbox
                                    :label="$t('review.submitHint')"
                                    :rules="[v => !!v]"
                                    class="font-weight-bold"
                                ></v-checkbox>
                                <div class="d-flex">
                                    <v-text-field
                                        :label="$t('Classification proposal')"
                                        class="mr-3"
                                        hide-details
                                        outlined
                                        v-model="review.grade_proposal"
                                    ></v-text-field>
                                    <v-btn :disabled="!valid" color="success" type="submit" x-large>{{ $t('Submit') }}
                                    </v-btn>
                                </div>
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
    import colors from 'vuetify/lib/util/colors';
    import Axios from '../../axios';
    import {pageContext} from '../../utils';


    export default Vue.extend({
        name: 'ReviewForm',
        props: {
            thesisId: {
                type: String,
                required: true
            }
        },
        data() {
            // @ts-ignore
            const $t = (key) => this.$t(key);
            return {
                thesis: {authors: [], opponent: {}, supervisor: {}},
                loading: false,
                valid: true,
                grades4: [$t('Excellent'), $t('Very well'), $t('Great'), $t('Not sufficient'), ''].reverse(),
                grades3: [$t('Over average'), $t('Average'), $t('Under average'), ''].reverse(),

                review: {
                    difficulty: 0,
                    grades: _.times(6, () => 0),
                    comment: null,
                    questions: null
                }
            };
        },
        computed: {
            reviewingUserRole() {
                return {
                    [this.thesis.supervisor.username]: 'supervisor',
                    [this.thesis.opponent.username]: 'opponent'
                }[pageContext.username]; // TODO: in case of filled review.user.username use that
            },
            gradings() {
                return _.filter([
                    this.reviewingUserRole == 'supervisor' ? this.$t('Students independence during processing') : null,
                    this.$t('Theoretical part of the work, comprehensibility of the text'),
                    this.$t('Methods and procedures used'),
                    this.$t('Formal editing, work with sources, citations in the text'),
                    this.$t('Graphic design of the thesis'),
                    this.$t('Interpretation of conclusions, their originality and their own contribution to the work')
                ]);
            }
        },
        methods: {
            valueToColor(v, scale = 3) {
                if (scale === 3) {
                    return {
                        3: colors.deepPurple.lighten2,
                        2: colors.blue.lighten2,
                        1: colors.red.lighten3,
                        0: colors.grey.lighten1
                    }[v];
                } else {
                    return {
                        4: colors.deepPurple.lighten2,
                        3: colors.blue.lighten2,
                        2: colors.orange.base,
                        1: colors.red.lighten3,
                        0: colors.grey.lighten1
                    }[v];
                }
            },
            async submit() {
                this.loading = true;

                const resp = (await Axios.post('/api/v1/review/',
                    {
                        ...this.review,
                        thesis: {id: this.thesis.id}
                    }
                )).data;

                if (resp.id) {
                    // TODO: show success
                } else {
                    // TODO show messages
                    this.valid = false;
                    this.messages = resp;
                }

                this.loading = false;
            }
        },
        async created() {
            this.thesis = (await Axios.get(`/api/v1/thesis/${this.thesisId}`)).data;
        }
    });
</script>
