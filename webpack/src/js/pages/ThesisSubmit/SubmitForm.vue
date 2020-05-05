<template>
    <v-card>
        <v-card-title>{{ $t('Thesis submit') }}</v-card-title>
        <v-card-text>
            <v-form @submit.prevent="submit" :valid="valid">
                <v-text-field
                    disabled filled v-model="thesis.title"
                    :label="$t('Thesis title')"
                ></v-text-field>

                <v-textarea
                    outlined hide-details
                    rows="15"
                    :label="$t('Abstract')"
                    v-model="thesis.abstract"
                    :rules="[v => !!v]"
                ></v-textarea>

                <v-file-input
                    :label="$t('Thesis text')"
                    v-model="thesis.thesisText"
                    :rules="[v => !!v]"
                    accept="application/pdf"

                ></v-file-input>

                <v-row no-gutters>
                    <v-spacer></v-spacer>
                    <v-btn type="submit" color="success" :disabled="!valid">
                        {{ $t('Submit thesis') }}
                    </v-btn>
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
                valid: true,
                thesis: {
                    abstract: null,
                    thesisText: null
                }
            };
        },
        async created() {

            this.thesis = (await Axios.get(`/api/v1/thesis/${this.id}`)).data;
        },
        methods: {
            async submit() {
                // TODO: make it alive
                let formData = new FormData();

                const data = {
                    ...this.thesis,
                    thesisText: undefined
                };
                if (this.thesis.thesisText) {
                    data.thesisText = await readFileAsync(this.thesis.thesisText);
                }

                for (let key in data) {
                    formData.append(key, this.thesis[key]);
                }
                const resp = await Axios.patch(`/api/v1/thesis/${this.id}/submit`, formData, {
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