<template>
    <v-card>
        <v-card-title>Import file</v-card-title>
        <v-card-text>
            <v-form>
                <v-file-input
                    label="File to import"
                ></v-file-input>
                <v-row no-gutters>
                    <v-spacer></v-spacer>
                    <v-btn type="submit" color="success">Import</v-btn>
                </v-row>
            </v-form>
        </v-card-text>
    </v-card>
</template>

<script type="text/tsx">
    import Vue from 'vue';

    export default Vue.extend({
        name: 'ImportForm'
    });
</script>

<style scoped>

</style>