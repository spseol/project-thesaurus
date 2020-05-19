<template>
    <v-row no-gutters>
        <v-col col="12" xl="10">
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