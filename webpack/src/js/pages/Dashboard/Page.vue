<template>
    <v-row justify="space-between">
        <v-col cols="12" lg="8" xl="6">
            <Dashboard></Dashboard>
        </v-col>
        <v-col cols="12" lg="4" xl="4" v-if="showMyReservations">
            <MyReservations></MyReservations>
        </v-col>
        <!--        <v-col cols="12" lg="4" xl="2">-->
        <!--            <RecentTheses></RecentTheses>-->
        <!--        </v-col>-->
    </v-row>
</template>

<script>
    import Vue from 'vue';
    import {hasGroup, hasPerm} from '../../user';
    import Dashboard from './Dashboard';
    import MyReservations from './MyReservations.vue';
    import RecentTheses from './RecentTheses';

    export default Vue.extend({
        name: 'Page',
        components: {MyReservations, RecentTheses, Dashboard},
        asyncComputed: {
            async showMyReservations() {
                return await hasPerm('thesis.add_reservation') && await hasGroup('student');
            },
        },
    });
</script>

<style scoped>

</style>