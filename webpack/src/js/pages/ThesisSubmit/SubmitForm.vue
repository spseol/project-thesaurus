<template>
    <v-card>
        <v-card-title>{{ $t('Thesis submit') }}</v-card-title>
        <v-card-text>
            <v-form @submit.prevent="submit" v-model="valid" ref="form" @change="$refs.form.validate()">
                <v-text-field
                    disabled filled v-model="thesis.title"
                    :label="$t('Thesis title')"
                ></v-text-field>

                <v-textarea
                    outlined hide-details
                    rows="15" class="mb-5"
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

                <v-file-input
                    :label="$t('Thesis poster')"
                    v-model="thesis.thesisPoster"
                    accept="image/png"
                ></v-file-input>
                <!-- TODO: validation? -->

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
    import {eventBus, readFileAsync} from '../../utils';

    export default Vue.extend({
        name: 'SubmitForm',
        props: {
            id: {type: String, required: true}
        },
        data() {
            return {
                valid: false,
                thesis: {
                    abstract: '',
                    thesisText: null
                }
            };
        },
        async created() {

            this.thesis = (await Axios.get(`/api/v1/thesis/${this.id}`)).data;
        },
        methods: {
            async submit() {
                let formData = new FormData();

                const data = {
                    ...this.thesis,
                    thesisText: undefined
                };
                if (!this.thesis.thesisText) {
                    this.valid = false;
                    return;
                }
                data.thesisText = await readFileAsync(this.thesis.thesisText);
                if (this.thesis.thesisPoster)
                    data.thesisPoster = await readFileAsync(this.thesis.thesisPoster);

                for (let key in data) {
                    formData.append(key, this.thesis[key]);
                }
                const resp = await Axios.patch(`/api/v1/thesis/${this.id}/submit`, formData, {
                    headers: {'Content-Type': 'multipart/form-data'}
                });

                if (resp.data.id) {
                    eventBus.flash({
                        text: this.$t('thesis.justSubmitted')
                    });
                    this.$router.push({name: 'dashboard'});
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