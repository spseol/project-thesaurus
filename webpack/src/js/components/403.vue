<template>
    <v-container class="fill-height mt-md-12" fluid>
        <v-row align="center" justify="center" no-gutters class="mt-md-12">
            <v-col cols="12" md="2" class="md-md-12 mr-10 text-right Emoji hidden-sm-and-down">
                !
            </v-col>
            <v-col cols="12" md="3" class="md-md-12 ml-md-10">
                <h1 class="display-3 font-weight-medium">{{ $t('page.403title') }}</h1>
                <p class="subtitle-1">{{ $t('page.403note') }}</p>
            </v-col>
        </v-row>
    </v-container>
</template>

<script type="text/tsx">
    import Vue from 'vue';

    export default Vue.extend({
        name: 'Page403'

    });
</script>

<style scoped lang="scss">
    @import "~vuetify/src/styles/settings/index";

    .Emoji {
        font-family: $heading-font-family;
        font-weight: 600;
        font-size: 15em;
        color: map_get($orange, 'base');
        text-shadow: 0 0 1px black;
    }
</style>