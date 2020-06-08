<template>
    <v-row no-gutters v-page-title="$t('page.title.thesisList')">
        <v-col cols="12">
            <ThesisList></ThesisList>
        </v-col>
    </v-row>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import ThesisList from './ThesisList.vue';

    export default Vue.extend({
        components: {ThesisList}
    });
</script>

<style scoped>

</style>