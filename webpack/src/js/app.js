import Vue from 'vue';
import PortalVue from 'portal-vue';
import VueRouter from 'vue-router';
import Vuetify from 'vuetify/lib/index';
import VueI18n from 'vue-i18n';
import csVuetify from 'vuetify/es5/locale/cs';
import enVuetify from 'vuetify/es5/locale/en';
import colors from 'vuetify/es5/util/colors';

import '../scss/index.scss';
import csLocal from './locale/cs.json';
import enLocal from './locale/en.json';
import App from './App';
import Axios from './axios';
import hasPerm from './user';
import {eventBus, pageContext} from './utils';

export default function createVue(opts = {}) {
    Vue.use(VueI18n);
    Vue.use(Vuetify);
    Vue.use(VueRouter);
    Vue.use(PortalVue);
    Vue.config.productionTip = false;

    // TODO: think about https://github.com/mblarsen/vue-browser-acl
    Vue.directive('has-perm', {
        inserted(el, bindings, vnode) {
            if (!bindings.arg) return;

            // dot is modifier sign for vue directives and app splitter for Django perms, needed manual parse
            const perm = bindings.arg.indexOf('.') >= 0 ? bindings.arg : bindings.rawName.replace(/v-has-perm:/g, '');

            el.style.display = 'none';
            hasPerm(perm).then((allowed) => {
                if (allowed)
                    el.style.display = null;
                else
                    el.style.display = 'none';

            }).catch(() => {
                el.style.display = 'none';
            });
        },
    });

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
    });

    const i18n = new VueI18n({
        locale,
        messages: {cs: csLocal, en: enLocal},
    });

    Axios.get('/api/i18n/catalog', {headers: {'Accept-language': locale}}).then(({data}) => {
        i18n.mergeLocaleMessage(locale, data.catalog);
    });

    const router = new VueRouter({
        routes: [
            {path: '/', component: () => import('./pages/Dashboard/Page'), name: 'dashboard'},
            {
                path: '/thesis/list',
                component: () => import('./pages/ThesisList/Page'),
                name: 'thesis-list',
            },
            {
                path: '/thesis/prepare',
                component: () => import('./pages/ThesisPrepare/Page'),
                name: 'thesis-prepare',
                meta: {perm: 'thesis.add_thesis'},
            },
            {
                path: '/thesis/submit/:id',
                component: () => import('./pages/ThesisSubmit/Page'),
                name: 'thesis-submit',
            },
            {
                path: '/reservations',
                component: () => import('./pages/ReservationList/Page'),
                name: 'reservations',
                meta: {perm: 'thesis.view_reservation'},
            },
            {
                path: '/exports',
                component: () => import('./pages/Exports/Page'),
                name: 'exports',
                meta: {perm: 'accounts.view_user'},
            },
            {
                path: '/settings',
                component: {template: '<div>Nonono</div>'},
                name: 'settings',
            },
            {
                path: '/review/:thesisId/:reviewId?',
                component: () => import('./pages/ReviewSubmit/Page'),
                name: 'review-detail',
            },
            {path: '/not-found', component: () => import('./components/404'), name: '404'},
            {path: '*', redirect: {name: '404'}},
        ],
        mode: 'history',
        base: `${locale}/`,
    });

    router.beforeEach((to, from, next) => {
        if (to.meta?.perm) {
            hasPerm(to.meta.perm).then(allow => {
                if (allow) {
                    next();
                } else {
                    eventBus.flash({color: 'warning', text: i18n.t('Permission denied')});
                    next({name: 'dashboard'});
                }
            }).catch(() => {
                eventBus.flash({color: 'warning', text: i18n.t('Unknown problem')});
                next({name: 'dashboard'});
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