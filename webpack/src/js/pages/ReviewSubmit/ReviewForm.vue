<template>
    <v-container fluid>
        <v-card>
            <v-card-title>{{ $t('Thesis review') }}</v-card-title>
            <v-card-text>
                <v-form v-model="valid">
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-text-field
                                disabled filled
                                :label="$t('Student name')"
                                :value="thesis.authors.map(a => a.full_name).join(', ')"
                            ></v-text-field>
                            <v-text-field
                                disabled filled
                                :label="$t('Thesis name')"
                                :value="thesis.title"
                            ></v-text-field>
                            <v-text-field
                                disabled filled
                                :label="$t('Review author')"
                                :value="(thesis[reviewingUserRole] || {full_name: $t('Unknown')}).full_name"
                                :suffix="$t(reviewingUserRole)"
                            ></v-text-field>
                            <v-divider></v-divider>
                            <v-textarea
                                outlined
                                rows="14"
                                :label="$t('Review comment')"
                                :rules="[v => !!v]"
                                v-model="review.comment"
                            ></v-textarea>
                            <v-textarea
                                outlined
                                rows="8"
                                :label="$t('Thesis defence questions')"
                                hide-details
                                v-model="review.questions"
                            ></v-textarea>
                        </v-col>
                        <v-col cols="12" md="6" class="d-flex flex-column justify-space-between">
                            <div>
                                <v-chip
                                    :color="valueToColor(review.difficulty, 3)"
                                >{{ $t('Difficulty of selected topic') }}
                                </v-chip>
                                <v-slider
                                    :tick-labels="grades3"
                                    v-model="review.difficulty"
                                    :rules="[v => v > 0]"
                                    :max="3"
                                    :min="0"
                                    :step="1"
                                    ticks="always"
                                    :thumb-color="valueToColor(review.difficulty, 3)"
                                    :track-color="valueToColor(review.difficulty, 3)"
                                    :color="valueToColor(review.difficulty, 3)"
                                    class="VSliderCustom__label--gray"
                                ></v-slider>

                                <div v-for="(grade, i) in review.grades">
                                    <v-chip
                                        :color="valueToColor(grade.value, 4)"
                                        class="mt-5"
                                    >{{ gradings[i] }}
                                    </v-chip>
                                    <v-slider
                                        v-model="grade.value"
                                        :rules="[v => v > 0]"
                                        :tick-labels="grades4"
                                        :max="4"
                                        :min="0"
                                        :step="1"
                                        ticks="always"
                                        color="info"
                                        :thumb-color="valueToColor(grade.value, 4)"
                                        track-color="grey"
                                        :color="valueToColor(grade.value, 4)"
                                        class="VSliderCustom__label--gray"
                                    ></v-slider>
                                </div>
                            </div>
                            <div>
                                <v-divider></v-divider>
                                <v-checkbox
                                    :label="$t('review.submitHint')"
                                    class="font-weight-bold"
                                    :rules="[v => !!v]"
                                ></v-checkbox>
                                <div class="d-flex">
                                    <v-text-field
                                        outlined
                                        :label="$t('Classification proposal')"
                                        value="???"
                                        class="mr-3"
                                        hide-details
                                    ></v-text-field>
                                    <v-btn x-large color="success" type="submit" :disabled="!valid">{{ $t('Submit') }}
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
    import pageContext from '../../context';


    export default Vue.extend({
        name: 'ReviewForm',
        props: {
            id: {
                type: String,
                required: true
            }
        },
        data() {
            // @ts-ignore
            const $t = (key) => this.$t(key);
            return {
                thesis: {authors: [], opponent: {}, supervisor: {}},
                valid: true,
                grades4: [$t('Excellent'), $t('Very well'), $t('Great'), $t('Not sufficient'), ''].reverse(),
                grades3: [$t('Over average'), $t('Average'), $t('Under average'), ''].reverse(),

                review: {
                    difficulty: 0,
                    grades: _.times(6, () => ({value: 0})),
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
            }
        },
        async created() {
            this.thesis = (await Axios.get(`/api/v1/thesis/${this.id}`)).data;
        }
    });
</script>
