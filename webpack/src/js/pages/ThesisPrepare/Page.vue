<template>
    <v-row>
        <v-col xl="4" md="6">
            <ThesisPrepareForm></ThesisPrepareForm>
        </v-col>
        <v-col xl="4" md="6">
            <ImportForm></ImportForm>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import ImportForm from './ImportForm';

    import PrepareForm from './PrepareForm';

    export default Vue.extend({
        components: {ThesisPrepareForm: PrepareForm, ImportForm}
    });
</script>

<style scoped>

</style>