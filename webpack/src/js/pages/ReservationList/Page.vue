<template>
    <v-row>
        <v-col cols="12">
            <ReservationList></ReservationList>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import ReservationList from './ReservationList.vue';

    export default Vue.extend({
        name: 'Page',
        components: {ReservationList}
    });
</script>

<style scoped>

</style>