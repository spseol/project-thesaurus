<template>
    <v-card :loading="loading">
        <v-card-title>{{ $t('Prepare admission') }}</v-card-title>
        <v-card-text>
            <v-form
                ref="form"
                v-model="valid"
                @submit.prevent="submit"
            >
                <v-text-field
                    v-model="thesis.title"
                    :counter="128"
                    :rules="[v => !!v]"
                    :label="$t('Title')"
                    :error-messages="messages.title"
                    required
                ></v-text-field>

                <v-autocomplete
                    v-model="thesis.authors"
                    :loading="loading"
                    :items="studentOptions"
                    :search-input.sync="search"
                    cache-items
                    multiple
                    hide-no-data
                    :label="$t('Author(s)')"
                    :rules="[v => v.length > 0]"
                    :error-messages="messages.authors"
                ></v-autocomplete>

                <v-autocomplete
                    v-model="thesis.supervisor_id"
                    :items="teacherOptions"
                    hide-no-data
                    :label="$t('Supervisor')"
                    :rules="[v => !!v]"
                    :error-messages="messages.supervisor_id"
                ></v-autocomplete>

                <v-radio-group
                    :label="$t('Category')"
                    v-model="thesis.category"
                    row
                    :error-messages="messages.category"
                    :rules="[v => !!v]"
                >
                    <v-radio
                        v-for="{text, value} in categoryOptions"
                        :label="text" :value="value" :key="value"
                    ></v-radio>
                </v-radio-group>

                <v-menu
                    :close-on-content-click="false"
                    transition="scale-transition"
                    offset-y max-width="290px"
                >
                    <template v-slot:activator="{ on }">
                        <v-text-field
                            v-model="thesis.published_at" v-on="on"
                            :label="$t('Published')" readonly
                            append-icon="mdi-calendar"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="thesis.published_at"
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
                            v-model="thesis.submit_deadline" v-on="on"
                            :label="$t('Submit deadline')" readonly
                            append-icon="mdi-calendar"
                        ></v-text-field>
                    </template>
                    <v-date-picker
                        v-model="thesis.submit_deadline"
                        type="date" no-title scrollable
                    ></v-date-picker>
                </v-menu>

                <v-file-input
                    :label="$t('Thesis admission')"
                    v-model="thesis.admission"
                    :error-messages="messages.admission"
                    :accept="typeAttachmentAcceptTypes('thesis_assigment')"
                ></v-file-input>

                <v-row no-gutters>
                    <v-spacer></v-spacer>
                    <v-btn
                        large
                        type="submit"
                        color="success"
                        :disabled="!valid"
                        v-text="$t('Prepare')"
                    ></v-btn>
                </v-row>
            </v-form>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import _ from 'lodash-es';
    import qs from 'qs';
    import Axios from '../../axios';
    import {optionsStore} from '../../store/store';
    import {asyncComputed, notificationBus, readFileAsync} from '../../utils';

    export default {
        name: 'ThesisPrepareForm',
        data() {
            return {
                valid: false,
                loading: false,
                messages: {},

                search: '',
                studentOptions: [],
                checkbox: false,
                thesis: this.emptyThesis()
            };
        },
        watch: {
            async search(val) {
                await this.queryStudentOptions(val);
            }
        },
        computed: {
            ...optionsStore.mapGetters(['typeAttachmentAcceptTypes'])
        },
        methods: {
            async queryStudentOptions(search) {
                this.loading = true;

                this.studentOptions = (
                    await Axios.get(`/api/v1/student-options?only_active=true&${qs.stringify({search})}`)
                ).data;

                this.loading = false;
            },
            emptyThesis() {
                return {
                    title: '',
                    registration_number: '',
                    authors: [],
                    published_at: new Date().toISOString().substr(0, 7).replace('-', '/'),
                    submit_deadline: '',
                    category: null,
                    supervisor_id: null,
                    admission: null
                };
            },
            async submit() {
                this.$refs.form.validate();
                let formData = new FormData();

                const data = {
                    ...this.thesis,
                    admission: undefined
                };
                if (this.thesis.admission) {
                    data.admission = await readFileAsync(this.thesis.admission);
                }

                for (let key in data) {
                    formData.append(key, this.thesis[key]);
                }
                const resp = await Axios.post('/api/v1/thesis', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });

                if (resp.data.id) {
                    notificationBus.success(this.$t('thesis.justPrepared'));
                    Object.assign(this.$data, this.$options.data.apply(this));
                    await this.$router.push({name: 'thesis-list'});
                } else {
                    this.messages = resp.data;
                    _.forEach(
                        this.messages,
                        (msg) => {
                            notificationBus.warning(msg);
                        }
                    );
                }
            }
        },
        asyncComputed: {
            categoryOptions: asyncComputed('/api/v1/category-options'),
            teacherOptions: asyncComputed('/api/v1/teacher-options')
        }
    };
</script>