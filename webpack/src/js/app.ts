import PortalVue from 'portal-vue';
import {TiptapVuetifyPlugin} from 'tiptap-vuetify';
import Vue from 'vue';
import VueAsyncComputed from 'vue-async-computed';
import VueI18n from 'vue-i18n';
import VueRouter from 'vue-router';
import VuetifyToast from 'vuetify-toast-snackbar';
import csVuetify from 'vuetify/es5/locale/cs';
import enVuetify from 'vuetify/es5/locale/en';
import colors from 'vuetify/es5/util/colors';
import Vuetify from 'vuetify/lib/index';

import '../scss/index.scss';
import App from './App.vue';
import Axios from './axios';
import csLocal from './locale/cs.json';
import enLocal from './locale/en.json';
import {DjangoPermsPlugin, I18nRoutePlugin} from './plugins';
import {createRouter} from './router';
import {pageContext} from './utils';

export default function createVue(opts = {}) {
    Vue.use(VueI18n);
    Vue.use(Vuetify);
    Vue.use(VueRouter);
    Vue.use(VueAsyncComputed);
    Vue.use(PortalVue);
    Vue.use(I18nRoutePlugin);
    Vue.use(DjangoPermsPlugin);
    Vue.use(VuetifyToast, {
        queueable: true
    });

    Vue.config.productionTip = false;

    const {locale} = pageContext;

    const vuetify = new Vuetify({
        lang: {
            locales: {cs: csVuetify, en: enVuetify},
            current: locale
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
                    success: colors.green.base
                }
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
    const router = createRouter((k) => i18n.t(k));

    return new Vue({
        router,
        vuetify,
        i18n,
        render: h => h(App),
        ...opts
    });
}