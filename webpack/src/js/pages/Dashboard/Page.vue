<template>
    <v-row justify="space-between">
        <v-col cols="12" lg="8" xl="6">
            <Dashboard></Dashboard>
        </v-col>
        <v-col cols="12" lg="4" xl="3">
            <RecentTheses></RecentTheses>
        </v-col>
        <v-col cols="12" lg="4" xl="3">
            <RecentTheses></RecentTheses>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Dashboard from './Dashboard';
    import RecentTheses from './RecentTheses';

    export default Vue.extend({
        name: 'Page',
        components: {RecentTheses, Dashboard}
    });
</script>

<style scoped>

</style>