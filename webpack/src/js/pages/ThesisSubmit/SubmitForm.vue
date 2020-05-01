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
            console.log(`/api/v1/thesis/${this.id}/`);
            console.log('http://localhost:8080/api/v1/thesis/d6ba7a00-d57c-457c-84d7-396ec43eb536/');

            this.thesis = (await Axios.get(`/api/v1/thesis/${this.id}/`)).data;
            // this.thesis = (await Axios.get('http://localhost:8080/api/v1/thesis/d6ba7a00-d57c-457c-84d7-396ec43eb536/')).data;
        }
    });
</script>

<style scoped>

</style>