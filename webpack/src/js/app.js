import Vue from 'vue';
import PortalVue from 'portal-vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify/lib/index';
import VueI18n from 'vue-i18n';
import csVuetify from 'vuetify/es5/locale/cs';
import enVuetify from 'vuetify/es5/locale/en';
import colors from 'vuetify/es5/util/colors';
import VueAsyncComputed from 'vue-async-computed';

import '../scss/index.scss';
import csLocal from './locale/cs.json';
import enLocal from './locale/en.json';
import App from './App';
import hasPerm from './user';
import Axios from './axios';
import {eventBus, pageContext} from './utils';
import {DjangoPermsPlugin, I18nRoutePlugin} from './plugins';


export default function createVue(opts = {}) {
    Vue.use(VueI18n);
    Vue.use(Vuetify);
    Vue.use(VueRouter);
    Vue.use(VueAsyncComputed);
    Vue.use(PortalVue);
    Vue.use(I18nRoutePlugin);
    Vue.use(DjangoPermsPlugin);
    Vue.config.productionTip = false;

    const {locale} = pageContext;

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
                    warning: colors.orange.darken4,
                    info: colors.blue.base,
                    success: colors.green.base,
                },
            },
        },
        icons: {
            values: {
                thesis_assigment: 'mdi-file-pdf',
                thesis_text: 'mdi-file-pdf',
                thesis_poster: 'mdi-image',
                supervisor_review: 'mdi-file-pdf',
                opponent_review: 'mdi-file-pdf',
                thesis_attachment: 'mdi-folder-zip',
            },
        },
    });

    const i18n = new VueI18n({
        locale,
        messages: {cs: csLocal, en: enLocal},
    });

    Axios.defaults.headers['Accept-Language'] = locale;

    const router = new VueRouter({
        routes: [
            {
                path: '/:locale/', // unknown locales handles Django itself by locale middleware
                component: {template: '<router-view></router-view>'},
                children: [
                    {path: '', component: () => import('./pages/Dashboard/Page'), name: 'dashboard'},
                    {
                        path: 'thesis/list',
                        component: () => import('./pages/ThesisList/Page'),
                        name: 'thesis-list',
                    },
                    {
                        path: 'thesis/prepare',
                        component: () => import('./pages/ThesisPrepare/Page'),
                        name: 'thesis-prepare',
                        meta: {perm: 'thesis.add_thesis'},
                    },
                    {
                        path: 'thesis/submit/:id',
                        component: () => import('./pages/ThesisSubmit/Page'),
                        name: 'thesis-submit',
                    },
                    {
                        path: 'reservations',
                        component: () => import('./pages/ReservationList/Page'),
                        name: 'reservations',
                        meta: {perm: 'thesis.view_reservation'},
                    },
                    {
                        path: 'exports',
                        component: () => import('./pages/Exports/Page'),
                        name: 'exports',
                        meta: {perm: 'accounts.view_user'},
                    },
                    {
                        path: 'settings',
                        component: {template: '<div>Nonono</div>'},
                        name: 'settings',
                    },
                    {
                        path: 'review/:thesisId/:reviewId?',
                        component: () => import('./pages/ReviewSubmit/Page'),
                        name: 'review-detail',
                    },
                    {path: '404', component: () => import('./components/404'), name: '404'},
                    {path: '403', component: () => import('./components/403'), name: '403'},
                    {path: '*', redirect: {name: '404'}},
                ],
            },
            {path: '*', redirect: {name: '404'}},
        ],
        mode: 'history',
    });

    router.beforeEach((to, from, next) => {
        if (to.meta?.perm) {
            hasPerm(to.meta.perm).then(allow => {
                if (allow) {
                    next();
                } else {
                    eventBus.flash({color: 'warning', text: i18n.t('Permission denied')});
                    next({name: '403'});
                }
            }).catch(() => {
                eventBus.flash({color: 'warning', text: i18n.t('Unknown problem')});
                next({name: '403'});
            });
        } else {
            next();
        }
    });

    return new Vue({
        router,
        vuetify,
        i18n,
        render: h => h(App),
        ...opts,
    });
}