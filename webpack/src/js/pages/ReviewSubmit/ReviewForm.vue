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
                                rows="12"
                                :label="$t('Review comment')"
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
                                <div class="subtitle-1 black--text">{{ $t('Difficulty of selected topic') }}</div>
                                <v-slider
                                    :tick-labels="grades3"
                                    v-model="review.difficulty"
                                    :max="2"
                                    :step="1"
                                    ticks="always"
                                    :thumb-color="valueToColor(review.difficulty, 3)"
                                    :track-color="valueToColor(review.difficulty, 3)"
                                    :color="valueToColor(review.difficulty, 3)"
                                    class="VSliderCustom__label--gray"
                                ></v-slider>

                                <div v-for="grade in review.grades">
                                    <div class="subtitle-1 mt-6 black--text">{{ grade.text }}</div>
                                    <v-slider
                                        v-model="grade.value"
                                        :tick-labels="grades4"
                                        :max="3"
                                        :step="1"
                                        ticks="always"
                                        color="info"
                                        :thumb-color="valueToColor(grade.value, 4)"
                                        :track-color="valueToColor(grade.value, 4)"
                                        :color="valueToColor(grade.value, 4)"
                                        class="VSliderCustom__label--gray"
                                    >
                                        <template v-slot:tick-labels="value">

                                        </template>
                                        <template slot="default">test</template>

                                    </v-slider>
                                </div>
                            </div>
                            <div class="d-flex">

                                <v-text-field
                                    outlined
                                    :label="$t('Classification proposal')"
                                    value="???"
                                    class="mr-3"
                                    hide-details
                                ></v-text-field>
                                <v-btn x-large color="success">{{ $t('Submit') }}</v-btn>
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
                    this.$t('Not sufficient')
                ].reverse(),
                grades3: [
                    this.$t('Over average'),
                    this.$t('Average'),
                    this.$t('Under average')
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
                        2: colors.green.lighten2,
                        1: colors.blue.lighten2,
                        0: colors.red.accent3
                    }[v];
                } else {
                    return {
                        3: colors.deepPurple.lighten2,
                        2: colors.blue.lighten2,
                        1: colors.brown.base,
                        0: colors.red.accent3
                    }[v];
                }
            }
        }
    });
</script>
