import Vue from 'vue';
import Vuetify from 'vuetify';

import AsyncComputed from 'vue-async-computed';

import 'vuetify/src/styles/main.sass';
import cs from 'vuetify/es5/locale/cs';
import en from 'vuetify/es5/locale/en';
import colors from 'vuetify/es5/util/colors';

export default function createVueFactory(opts) {
    Vue.use(AsyncComputed);
    Vue.use(Vuetify);
    const vuetify = new Vuetify({
        lang: {
            locales: {cs, en},
            current: window.Thesaurus.settings.locale,
        },
        theme: {
            themes: {
                light: {
                    primary: colors.orange.base,
                    secondary: colors.brown.base,
                    accent: colors.deepOrange.base,
                    error: colors.pink.base,
                    warning: colors.yellow.base,
                    info: colors.blue.base,
                    success: colors.green.base,
                },
            },
        },
        // preset,
    });

    return new Vue({
        vuetify,
        ...opts,
    });

}