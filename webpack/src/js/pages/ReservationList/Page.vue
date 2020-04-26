<template>
    <v-row>
        <v-col sm="12" md="12" lg="10">
            <ReservationList></ReservationList>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import ReservationList from './ReservationList';

    export default Vue.extend({
        name: 'Page',
        components: {ReservationList}
    });
</script>

<style scoped>

</style>