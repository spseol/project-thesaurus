<template>
    <v-row>
        <v-col cols="12" lg="8" xl="6">
            <Dashboard></Dashboard>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Dashboard from './Dashboard';

    export default Vue.extend({
        name: 'Page',
        components: {Dashboard}
    });
</script>

<style scoped>

</style>