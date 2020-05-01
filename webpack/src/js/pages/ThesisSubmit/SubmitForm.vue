<template>
    <v-card>
        <v-card-title>{{ $t('Thesis submit') }}</v-card-title>
        <v-card-text>
            <v-form>
                <v-text-field
                    disabled filled
                    :label="$t('Thesis title')"
                    value="Long thesis name and some words"
                ></v-text-field>

                <v-textarea
                    outlined
                    rows="15"
                    :label="$t('Abstract')"
                    hide-details
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

    export default Vue.extend({
        name: 'SubmitForm'
    });
</script>

<style scoped>

</style>