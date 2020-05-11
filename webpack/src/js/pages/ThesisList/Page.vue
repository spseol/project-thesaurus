<template>
    <v-row no-gutters>
        <v-col cols="12">
            <ThesisList></ThesisList>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import ThesisList from './ThesisList';

    export default Vue.extend({
        name: 'Page',
        components: {ThesisList}
    });
</script>

<style scoped>

</style>