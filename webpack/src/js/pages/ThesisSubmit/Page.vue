<template>
    <v-row>
        <v-col xl="4" md="6">
            <SubmitForm :id="$route.params.id"></SubmitForm>
        </v-col>
        <v-col xl="4" md="6">
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import SubmitForm from './SubmitForm';


    export default Vue.extend({
        components: {SubmitForm}
    });
</script>

<style scoped>

</style>