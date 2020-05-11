<template>
    <v-row>
        <v-col col="12" lg="8" xl="6">
            <SubmitForm :id="$route.params.id"></SubmitForm>
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