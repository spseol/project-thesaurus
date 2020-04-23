import Vue from 'vue';
import Vuetify from 'vuetify';
import cs from 'vuetify/es5/locale/cs';
import en from 'vuetify/es5/locale/en';
import colors from 'vuetify/es5/util/colors';
import VueRouter from 'vue-router';


import 'vuetify/src/styles/main.sass';
import App from './App';

export default function createVue(opts) {
    Vue.use(Vuetify);
    Vue.use(VueRouter);

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
    });

    const router = new VueRouter({
        routes: [
            {path: '/theses', component: () => import('./pages/ThesisList/ThesisList'), name: 'thesis-list'},
            {path: '/thesis-create', component: () => import('./pages/ThesisForm/ThesisForm'), name: 'thesis-create'},
            {path: '/reservations', component: () => import('./pages/ThesisForm/ThesisForm'), name: 'reservations'},
            {path: '/exports', component: () => import('./pages/ThesisForm/ThesisForm'), name: 'exports'},
            {path: '/settings', component: () => import('./pages/ThesisForm/ThesisForm'), name: 'settings'},
            {path: '*', component: {template: '<div>Not found :-(</div>'}},
        ],
        mode: 'history',
    });

    return new Vue({
        router,
        vuetify,
        render: h => h(App),
        ...opts,
    });

}