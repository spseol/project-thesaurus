<template>
    <v-row justify="space-between">
        <v-col cols="12" lg="8" xl="6">
            <Dashboard></Dashboard>
        </v-col>
        <v-col cols="12" lg="4" xl="4" v-has-perm:thesis.add_reservation>
            <MyReservations></MyReservations>
        </v-col>
        <v-col cols="12" lg="4" xl="2">
            <RecentTheses></RecentTheses>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Dashboard from './Dashboard';
    import MyReservations from './MyReservations.vue';
    import RecentTheses from './RecentTheses';

    export default Vue.extend({
        name: 'Page',
        components: {MyReservations, RecentTheses, Dashboard}
    });
</script>

<style scoped>

</style>