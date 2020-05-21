<template>
    <v-card :loading="loading">
        <v-card-title>{{ $t('Thesis edit') }}</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
            <v-row no-gutters>
                <v-col class="mt-3">

                    <v-text-field
                        :label="$t('Title')" v-model="data.title" :rules="[v => !!v]"
                    ></v-text-field>

                    <v-text-field
                        :label="$t('Registration number')" v-model="data.registration_number"
                        :counter="4"
                        :rules="[v => !v || /[A-Z]\d{3}/.test(v) || $t('Not in format AXXX.')]"
                    ></v-text-field>

                    <v-radio-group
                        :label="$t('Category')" row
                        v-model="data.category" :rules="[v => !!v]"
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

                </v-col>
                <v-col class="mt-3 ml-3">
                    <v-subheader>{{ $t('Reviews') }}</v-subheader>
                    <v-simple-table class="px-0">
                        <table>
                            <tbody>
                            <tr v-for="rew in thesis.reviews" class="py-2">
                                <td class="col-6">
                                    {{ rew.user.full_name }}
                                </td>
                                <td class="text-right">
                                    <v-btn text outlined small color="info">
                                        <v-icon small class="mr-1">mdi-eye</v-icon>
                                        {{ $t('View') }}
                                    </v-btn>
                                    <v-btn outlined color="error" small>
                                        <v-icon small class="mr-1">mdi-trash-can-outline</v-icon>
                                        {{ $t('Delete') }}
                                    </v-btn>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </v-simple-table>
                    <v-spacer></v-spacer>
                    <v-subheader>{{ $t('Attachments') }}</v-subheader>
                    <v-simple-table>
                        <table>
                            <tbody>
                            <tr v-for="att in thesis.attachments" class="py-2">
                                <td class="col-6">
                                    {{ att.type_attachment.name }}
                                </td>
                                <td class="text-right">
                                    <v-btn text outlined small color="info">
                                        <v-icon small class="mr-1">mdi-eye</v-icon>
                                        {{ $t('View') }}
                                    </v-btn>
                                    <v-btn outlined color="error" small>
                                        <v-icon small class="mr-1">mdi-trash-can-outline</v-icon>
                                        {{ $t('Delete') }}
                                    </v-btn>
                                </td>
                            </tr>
                            </tbody>
                        </table>
                    </v-simple-table>
                </v-col>
            </v-row>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="success" type="submit" large class="ma-2">{{ $t('Save data') }}</v-btn>
        </v-card-actions>
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
            return {data: {}, loading: false, search: '', studentOptions: [], authors: []};
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
            async save() {

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
        }
    };
</script>
