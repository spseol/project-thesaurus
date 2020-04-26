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
import Axios from './axios';

export default function createVue(opts = {}) {
    Vue.use(VueI18n);
    Vue.use(Vuetify);
    Vue.use(VueRouter);
    Vue.use(PortalVue);

    const {locale} = window.Thesaurus.settings;

    const vuetify = new Vuetify({
        lang: {
            locales: {cs: csVuetify, en: enVuetify},
            current: locale,
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
        locale,
        messages: {cs: csLocal, en: {}},
    });


    Axios.get('/api/i18n/catalog', {headers: {'Accept-language': locale}}).then(({data}) => {
        i18n.mergeLocaleMessage(locale, data.catalog);
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
        base: `${locale}/`,
    });

    return new Vue({
        router,
        vuetify,
        i18n,
        render: h => h(App),
        ...opts,
    });

}