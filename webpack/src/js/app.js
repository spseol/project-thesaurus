import PortalVue from 'portal-vue';
import Vue from 'vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify';
import VueI18n from 'vue-i18n';
import {cs as csVuetify, en as enVuetify} from 'vuetify/es5/locale';
import csLocal from './locale/cs.json';
import colors from 'vuetify/es5/util/colors';

import 'vuetify/src/styles/main.sass';
import App from './App';
import Axios from './api-client';

export default function createVue(opts = {}) {
    Vue.use(VueI18n);
    Vue.use(Vuetify);
    Vue.use(VueRouter);
    Vue.use(PortalVue);

    const vuetify = new Vuetify({
        lang: {
            locales: {cs: csVuetify, en: enVuetify},
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
    });

    const i18n = new VueI18n({
        locale: window.Thesaurus.settings.locale, // set locale
        messages: {cs: csLocal},
    });

    Axios.get('/api/i18n/').then(({data}) => {
        i18n.mergeLocaleMessage(window.Thesaurus.settings.locale, data.catalog);
    });

    const router = new VueRouter({
        routes: [
            {path: '/', component: {template: '<div>Home</div>'}, name: 'home'},
            {path: '/theses', component: () => import('./pages/ThesisList/ThesisList'), name: 'thesis-list'},
            {
                path: '/thesis-prepare',
                component: () => import('./pages/ThesisPrepareForm/ThesisPrepareForm'),
                name: 'thesis-prepare',
            },
            {path: '/reservations', component: {template: '<div>Nonono</div>'}, name: 'reservations'},
            {path: '/exports', component: {template: '<div>Nonono</div>'}, name: 'exports'},
            {path: '/settings', component: {template: '<div>Nonono</div>'}, name: 'settings'},
            {path: '*', component: {template: '<div>Not found :-(</div>'}},
        ],
        mode: 'history',
    });

    return new Vue({
        router,
        vuetify,
        i18n,
        render: h => h(App),
        ...opts,
    });

}