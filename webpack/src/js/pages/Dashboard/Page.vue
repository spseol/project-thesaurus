<template>
    <v-row>
        <v-col cols="8">
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