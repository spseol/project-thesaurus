<template>
    <v-container fluid>
        <v-card>
            <v-card-title>{{ $t('Thesis review') }}</v-card-title>
            <v-card-text>
                <v-form>
                    <v-row>
                        <v-col cols="12" md="6">
                            <v-text-field
                                disabled filled
                                :label="$t('Student name')"
                                value="John Doe"
                            ></v-text-field>
                            <v-text-field
                                disabled filled
                                :label="$t('Thesis name')"
                                value="Long thesis name and some words"
                            ></v-text-field>
                            <v-text-field
                                disabled filled
                                :label="$t('Review author')"
                                value="Harry Potter"
                            ></v-text-field>
                            <v-btn-toggle mandatory value="opponent" v-if="false">
                                <v-btn value="supervisor" outlined>{{ $t('Supervisor') }}</v-btn>
                                <v-btn value="opponent" outlined>{{ $t('Opponent') }}</v-btn>
                            </v-btn-toggle>
                            <v-divider></v-divider>
                            <v-textarea
                                outlined
                                rows="14"
                                :label="$t('Review comment')"
                                :rules="[v => !!v]"
                            ></v-textarea>
                            <v-textarea
                                outlined
                                rows="8"
                                :label="$t('Thesis defence questions')"
                                hide-details
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
                                    :max="3"
                                    :min="0"
                                    :step="1"
                                    ticks="always"
                                    :thumb-color="valueToColor(review.difficulty, 3)"
                                    :track-color="valueToColor(review.difficulty, 3)"
                                    :color="valueToColor(review.difficulty, 3)"
                                    class="VSliderCustom__label--gray"
                                ></v-slider>

                                <div v-for="grade in review.grades">
                                    <v-chip
                                        :color="valueToColor(grade.value, 4)"
                                        class="mt-5"
                                    >{{ grade.text }}
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
                                    <v-btn x-large color="success" type="submit">{{ $t('Submit') }}</v-btn>
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
    import Vue from 'vue';
    import colors from 'vuetify/lib/util/colors';


    export default Vue.extend({
        name: 'ImportForm',
        data() {
            return {
                grades4: [
                    this.$t('Excellent'),
                    this.$t('Very well'),
                    this.$t('Great'),
                    this.$t('Not sufficient'),
                    ''
                ].reverse(),
                grades3: [
                    this.$t('Over average'),
                    this.$t('Average'),
                    this.$t('Under average'),
                    ''
                ].reverse(),
                review: {
                    difficulty: 0,
                    grades: [
                        {
                            value: 0,
                            text: this.$t('Students independence during processing (to be filled in only by the supervisor)')
                        },
                        {value: 0, text: this.$t('Theoretical part of the work, comprehensibility of the text')},
                        {value: 0, text: this.$t('Methods and procedures used')},
                        {value: 0, text: this.$t('Formal editing, work with sources, citations in the text')},
                        {value: 0, text: this.$t('Graphic design of the thesis')},
                        {
                            value: 0,
                            text: this.$t('Interpretation of conclusions, their originality and their own contribution to the work')
                        }
                    ]
                }
            };
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
        }
    });
</script>
