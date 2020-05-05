<template>
    <v-card>
        <v-card-title>{{ $t('Thesis submit') }}</v-card-title>
        <v-card-text>
            <v-form>
                <v-text-field
                    disabled filled v-model="thesis.title"
                    :label="$t('Thesis title')"
                ></v-text-field>

                <v-textarea
                    outlined hide-details
                    rows="15"
                    :label="$t('Abstract')"
                    v-model="thesis.abstract"
                ></v-textarea>

                <v-file-input
                    label="Thesis text"
                ></v-file-input>
                <v-row no-gutters>
                    <v-spacer></v-spacer>
                    <v-btn type="submit" color="success">Submit</v-btn>
                </v-row>
            </v-form>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Axios from '../../axios';
    import {readFileAsync} from '../../utils';

    export default Vue.extend({
        name: 'SubmitForm',
        props: {
            id: {type: String, required: true}
        },
        data() {
            return {
                thesis: {
                    abstract: null
                }
            };
        },
        async created() {

            this.thesis = (await Axios.get(`/api/v1/thesis/${this.id}/`)).data;
        },
        methods: {
            async submit() {
                // TODO: make it alive
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
                const resp = await Axios.put('/api/v1/thesis/', formData, {
                    headers: {'Content-Type': 'multipart/form-data'}
                });

                if (resp.data.id) {

                } else {
                    this.messages = resp.data;
                    this.valid = false;
                }
            }
        }
    });
</script>

<style scoped>

</style>