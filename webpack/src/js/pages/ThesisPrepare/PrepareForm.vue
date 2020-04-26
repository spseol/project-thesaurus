<template>

    <v-card :loading="loading">
        <v-card-title>{{ $t('Prepare new thesis') }}</v-card-title>
        <v-card-text>
            <v-form
                ref="form"
                v-model="valid"
                @submit.prevent="submit"
                lazy-validation
            >
                <v-text-field
                    v-model="thesis.title"
                    :counter="128"
                    :rules="[v => !!v]"
                    :label="$t('Title')"
                    required
                ></v-text-field>

                <v-text-field
                    v-model="thesis.registration_number"
                    :counter="4"
                    :rules="[v => !!v, v => /[A-Z]\d{3}/.test(v) || 'Not in format AXXX.']"
                    :label="$t('Registration number')"
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
                ></v-autocomplete>

                <v-autocomplete
                    v-model="thesis.supervisor"
                    :items="teacherOptions"
                    hide-no-data
                    :label="$t('Supervisor')"
                    :rules="[v => !!v]"
                ></v-autocomplete>

                <v-radio-group
                    :label="$t('Category')"
                    v-model="thesis.category"
                    row
                    :rules="[v => !!v]"
                >
                    <v-radio
                        v-for="{text, value} in categoryOptions"
                        :label="text" :value="value" :key="value"
                    ></v-radio>
                </v-radio-group>

                <v-text-field
                    v-model="thesis.published_at"
                    :counter="7"
                    :rules="[v => !!v, v => /\d{4}\/\d{2}/.test(v) || 'Not in format YYYY/MM.']"
                    :label="$t('Published')"
                    required
                ></v-text-field>

                <v-file-input
                    accept="application/pdf"
                    :label="$t('Thesis admission')"
                    v-model="thesis.admission"
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
    import qs from 'qs';
    import Vue from 'vue';
    import Axios from '../../axios';

    export default Vue.extend({
        name: 'ThesisPrepareForm',
        data: () => ({
            valid: false,
            loading: false,

            search: '',
            select: null,
            teacherOptions: [],
            categoryOptions: [],
            studentOptions: [],
            checkbox: false,
            thesis: {
                title: '',
                registration_number: '',
                authors: [],
                published_at: new Date().toISOString().substr(0, 7).replace('-', '/'),
                category: null,
                supervisor: null,
                admission: null
            }
        }),
        watch: {
            async search(val) {
                val !== this.select && (await this.queryStudentOptions(val));
            }
        },

        methods: {
            async queryStudentOptions(search) {
                this.loading = true;

                this.studentOptions = (await Axios.get(`/api/v1/student-options/?${qs.stringify({search})}`)).data;

                this.loading = false;
            },
            readFileAsync(file) {
                return new Promise((resolve, reject) => {
                    let reader = new FileReader();

                    reader.onload = () => {
                        resolve(reader.result);
                    };

                    reader.onerror = reject;

                    reader.readAsArrayBuffer(file);
                });
            },
            async submit() {
                this.$refs.form.validate();
                let formData = new FormData();

                const data = {
                    ...this.thesis,
                    admission: undefined
                };
                if (this.thesis.admission) {
                    data.admission = await this.readFileAsync(this.thesis.admission);
                }

                for (let key in data) {
                    formData.append(key, this.thesis[key]);
                }

                await Axios.post('/api/v1/thesis/', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
            }
        },
        async created() {
            this.categoryOptions = (await Axios.get('/api/v1/category-options/')).data;
            this.teacherOptions = (await Axios.get('/api/v1/teacher-options/')).data;
        }
    });
</script>