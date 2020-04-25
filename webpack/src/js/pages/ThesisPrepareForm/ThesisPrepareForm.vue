<template>
    <v-row>
        <v-col xl="4" md="6">
            <v-card :loading="loading">
                <v-card-title>Prepare new thesis</v-card-title>
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
                            label="Title"
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
                            label="Author(s)"
                            :rules="[v => v.length > 0]"
                        ></v-autocomplete>

                        <v-radio-group

                            label="Category"
                            v-model="thesis.category"
                            row
                            :rules="[v => !!v]"
                        >
                            <v-radio
                                v-for="{text, value} in categoryOptions"
                                :label="text" :value="value"
                            ></v-radio>
                        </v-radio-group>

                        <v-file-input
                            accept="application/pdf"
                            label="Thesis admission"
                            v-model="thesis.admissionAttachment"
                        ></v-file-input>

                        <v-row>
                            <v-spacer></v-spacer>
                            <v-btn large right type="submit" color="primary">Submit</v-btn>
                        </v-row>
                    </v-form>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import qs from 'qs';
    import Vue from 'vue';
    import Axios from '../../api-client';

    export default Vue.extend({
        data: () => ({
            valid: true,
            loading: false,

            search: '',
            select: null,
            teacherOptions: [],
            categoryOptions: [],
            studentOptions: [],
            checkbox: false,
            thesis: {
                title: '',
                authors: [],
                category: null,
                admissionAttachment: null

            }
        }),
        watch: {
            async search(val) {
                val !== this.select && (await this.queryStudentOptions(val));
            }
        },

        methods: {
            validate() {
                this.$refs.form.validate();
            },
            reset() {
                this.$refs.form.reset();
            },
            resetValidation() {
                this.$refs.form.resetValidation();
            },
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
                let formData = new FormData();

                const admissionAttachment = await this.readFileAsync(this.thesis.admissionAttachment);

                const data = {
                    ...this.thesis,
                    admissionAttachment
                };

                for (let key in data) {
                    formData.append(key, this.thesis[key]);
                }
                console.log(data, formData);
            }
        },
        async created() {
            this.categoryOptions = (await Axios.get('/api/v1/category-options/')).data;
            this.teacherOptions = (await Axios.get('/api/v1/teacher-options/')).data;
        }
    });
</script>