import Vue from 'vue';
import Vuetify from 'vuetify';

import AsyncComputed from 'vue-async-computed';

import 'vuetify/src/styles/main.sass';
import cs from 'vuetify/es5/locale/cs';
import en from 'vuetify/es5/locale/en';


export default function createVueFactory(opts) {
    Vue.use(AsyncComputed);
    Vue.use(Vuetify);
    const vuetify = new Vuetify({
        lang: {
            locales: {cs, en},
            current: window.Thesaurus.settings.locale,
        },
        // preset,
    });

    return new Vue({
        vuetify,
        ...opts,
    });

}