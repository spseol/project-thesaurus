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
                                ></v-text-field>

                                <v-text-field
                                    :label="$t('Registration number')" v-model="data.registration_number"
                                    :counter="4"
                                    :rules="[v => !v || /[A-Z]\d{3}/.test(v) || $t('thesis.invalidSNformat')]"
                                ></v-text-field>

                                <v-radio-group
                                    :label="$t('Category')" row
                                    v-model="data.category.id" :rules="[v => !!v]"
                                >
                                    <v-radio
                                        v-for="{text, value} in categoryOptions"
                                        :label="text" :value="value" :key="value"
                                    ></v-radio>
                                </v-radio-group>

                                <v-autocomplete
                                    v-model="data.supervisor.id"
                                    :items="teacherOptions" hide-no-data
                                    :label="$t('Supervisor')"
                                    :rules="[v => !!v]"
                                ></v-autocomplete>

                                <v-autocomplete
                                    v-model="data.opponent.id"
                                    :items="teacherOptions" hide-no-data
                                    :label="$t('Opponent')"
                                    :rules="[v => !!v]"
                                ></v-autocomplete>

                                <v-autocomplete
                                    v-model="authors"
                                    :loading="loading"
                                    :items="studentOptions"
                                    :search-input.sync="search"
                                    cache-items multiple chips clearable deletable-chips small-chips
                                    :label="$t('Author(s)')"
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
                                    :items="thesisStateOptions" v-model="data.state"
                                    :hint="thesisStateOptions.find(({value}) => value === data.state).help_text"
                                    persistent-hint flat solo outlined dense
                                ></v-select>
                            </v-card-text>
                        </v-card>

                        <v-card elevation="0" class="mt-3" outlined>
                            <v-card-subtitle class="font-weight-bold">{{ $t('Attachments') }}</v-card-subtitle>
                            <v-card-text>
                                <v-row v-for="att in thesis.attachments" :key="att.id"
                                    class="pa-3 justify-space-between">
                                    <span>
                                        {{ att.type_attachment.name }}
                                    </span>
                                    <span class="text-right">
                                        <v-btn text outlined small color="info" :href="att.url" target="_blank">
                                            <v-icon small class="mr-1">${{ att.type_attachment.identifier }}</v-icon>
                                            {{ $t('View') }}
                                        </v-btn>
                                        <v-btn outlined color="error" small>
                                            <v-icon small class="mr-1">mdi-trash-can-outline</v-icon>
                                            {{ $t('Delete') }}
                                        </v-btn>
                                    </span>
                                </v-row>
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
                                        <v-btn outlined color="error" small>
                                            <v-icon small class="mr-1">mdi-trash-can-outline</v-icon>
                                            {{ $t('Delete') }}
                                        </v-btn>
                                    </span>
                                </v-row>
                                <v-alert color="info" text v-if="!thesis.reviews.length">
                                    {{ $t('thesis.noReviews') }}
                                </v-alert>
                            </v-card-text>
                        </v-card>

                    </v-col>
                </v-row>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text type="button" large class="ma-2" @click="$emit('close')">{{ $t('Cancel edit') }}</v-btn>
                <v-btn color="success" type="submit" large class="ma-2">{{ $t('Save data') }}</v-btn>
            </v-card-actions>
        </v-form>
    </v-card>
</template>

<script type="text/tsx">

    import _ from 'lodash';
    import qs from 'qs';
    import Axios from '../../axios';

    export default {
        name: 'ThesisEditPanel',
        props: {
            thesis: {type: Object},
            categoryOptions: {type: Array},
            teacherOptions: {type: Array}
        },
        data() {
            return {
                data: {},
                loading: false,
                search: '',
                studentOptions: [],
                thesisStateOptions: [],
                authors: []
            };
        },
        watch: {
            async search(val) {
                val !== this.select && (await this.queryStudentOptions(val));
            }
        },
        methods: {
            async queryStudentOptions(search) {
                this.loading = true;

                this.studentOptions = (await Axios.get(`/api/v1/student-options?${qs.stringify({search})}`)).data;

                this.loading = false;
            },
            async submit() {
                this.loading = true;

                const resp = (await Axios.patch(
                    `/api/v1/thesis/${this.thesis.id}`,
                    {
                        ...this.data,
                        supervisor_id: this.data.supervisor?.id,
                        opponent_id: this.data.opponent?.id
                    }
                )).data;

                this.$emit('reload');
                this.loading = false;
            }
        },
        async created() {
            const t = this.thesis;
            this.data = {
                ...t,
                // load v/o if present
                opponent: {...(t.opponent || {id: null})},
                supervisor: {...(t.supervisor || {id: null})}
            };
            this.authors = _.map(t.authors, 'id');

            // TODO: solve it lazy, lazy Joe
            this.thesisStateOptions = (await Axios.get(`/api/v1/thesis-state-options`)).data;
        }
    };
</script>
