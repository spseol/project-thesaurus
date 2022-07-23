import * as Sentry from '@sentry/browser';
import {Vue as VueIntegration} from '@sentry/integrations';
import PortalVue from 'portal-vue';
import {TiptapVuetifyPlugin} from 'tiptap-vuetify';
import Vue from 'vue';
import VueAsyncComputed from 'vue-async-computed';
import VueCallStore from 'vue-call-store';
import VueI18n from 'vue-i18n';
import VueRouter from 'vue-router';
import VuetifyToast from 'vuetify-toast-snackbar';
import 'vuetify-toast-snackbar/src/index';
import csVuetify from 'vuetify/es5/locale/cs';
import enVuetify from 'vuetify/es5/locale/en';
import Vuetify, {VBtn, VIcon, VSnackbar} from 'vuetify/lib/index';
import '../scss/index.scss';
import App from './App.vue';
import Axios from './axios';
import csLocal from './locale/cs.json';
import enLocal from './locale/en.json';
import {DjangoPermsPlugin, I18nRoutePlugin} from './plugins';
import {createRouter} from './router';
import {OPTIONS_ACTIONS} from './store/options';
import {PERMS_ACTIONS} from './store/perms';
import {createStore} from './store/store';
import {notificationBus, pageContext, THEME_DARK_COLORS, THEME_LIGHT_COLORS} from './utils';

Vue.use(DjangoPermsPlugin);
Vue.use(I18nRoutePlugin);
Vue.use(PortalVue);
Vue.use(VueAsyncComputed);
Vue.use(VueI18n);
Vue.use(VueRouter);
Vue.use(Vuetify, {
    components: {
        VSnackbar,
        VBtn,
        VIcon
    }
});
Vue.use(VuetifyToast, {
    x: 'right',
    y: 'top',
    timeout: 6000
});

declare var __SENTRY_DSN__: string;

if (__SENTRY_DSN__) {
    Sentry.init({
        dsn: __SENTRY_DSN__,
        integrations: [new VueIntegration({Vue, attachProps: true})]
    });
}

export default function createVue(opts: any = {}) {
    Vue.config.productionTip = false;

    const originTitle = document.title;

    Vue.directive('page-title', (el, binding) => document.title = `${binding.value} | ${originTitle}`);

    const {locale} = pageContext;

    const vuetify = new Vuetify({
        lang: {
            locales: {cs: csVuetify, en: enVuetify},
            current: locale
        },
        theme: {
            themes: {
                light: THEME_LIGHT_COLORS,
                dark: THEME_DARK_COLORS
            }
        },
        icons: {
            values: {
                thesis_assigment: 'mdi-file-pdf',
                thesis_text: 'mdi-file-pdf',
                thesis_poster: 'mdi-image',
                supervisor_review: 'mdi-file-pdf',
                opponent_review: 'mdi-file-pdf',
                thesis_attachment: 'mdi-folder-zip'
            }
        }
    });

    const i18n = new VueI18n({locale, messages: {cs: csLocal, en: enLocal}});

    Vue.use(TiptapVuetifyPlugin, {
        vuetify,
        iconsGroup: 'mdi'
    });

    Axios.defaults.headers['Accept-Language'] = locale;

    let store;
    if ('store' in opts)
        store = opts.store;
    else
        store = createStore();

    let router;
    if ('router' in opts)
        router = opts.router;
    else
        router = createRouter((k) => i18n.t(k), store);


    if (store) {
        store.dispatch(`perms/${PERMS_ACTIONS.LOAD_PERMS}`);
        store.dispatch(`options/${OPTIONS_ACTIONS.LOAD_OPTIONS}`);
    }

    Vue.use(VueCallStore, {store});

    const app = new Vue({
        router,
        vuetify,
        store,
        i18n,
        render: h => h(App),
        ...opts
    });

    notificationBus.$on('flash', (flash) => {
        app.$toast(flash.text, {...flash, color: flash.color});
    });

    pageContext.messages.forEach((m) => {
        notificationBus[m.type](m.text);
    });

    return app;
}