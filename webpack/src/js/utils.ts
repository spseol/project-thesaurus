import Vue from 'vue';
import colors from 'vuetify/lib/util/colors';
import Axios from './axios';
import {User} from './types';
import {hasPerm} from './user';

class PageContext {
    user: User;
    locale: string;
    djangoAdminUrl: string;
    languages: Array<string>;
    groups: Array<string>;
    version: string;

    constructor() {
        return new Proxy(this, {
            get: function(person, field) {
                return window['Thesaurus'].pageContext[field];
            }
        });
    }
}


export function readFileAsync(file) {
    return new Promise((resolve, reject) => {
        let reader = new FileReader();

        reader.onload = () => {
            resolve(reader.result);
        };

        reader.onerror = reject;

        reader.readAsArrayBuffer(file);
    });
}

export function memoize(method) {
    let cache = {};

    return async function(...args) {
        let key = JSON.stringify(args);
        cache[key] = cache[key] || method.apply(this, args);
        return cache[key];
    };
}


export function asyncComputed(url, options = null) {
    const _options = {default: [], watch: ['$i18n.locale'], lazy: false, ...(options || {})};
    return {
        async get() {
            if (_options.perm && !(await hasPerm(_options.perm))) return [];

            return (await Axios.get(url)).data;
        },
        default: _options.default,
        lazy: _options.lazy
    };
}

export const asyncOptions = (url) => asyncComputed(url, {default: []});

export const getAuditMappings = memoize(async () => {
    return (await Axios.get('/api/v1/audit/mappings')).data;
});

const pageContext = new PageContext();

class Flash extends Object {
    text: string;
    color?: string;
}

class EventBus extends Vue {
    public flash(flash: Flash) {
        this.$emit('flash', flash);
    }

    public success(text: string) {
        this.$emit('flash', {text, color: 'success', icon: 'mdi-check-bold'});
    }

    public warning(text: string) {
        this.$emit('flash', {text, color: 'warning', icon: 'mdi-exclamation-thick'});
    }

    public info(text: string) {
        this.$emit('flash', {text, color: 'info', icon: 'mdi-exclamation-thick'});
    }
}

const notificationBus = new EventBus();

export const GRADE_COLOR_SCALE_3 = {
    3: colors.green.lighten2,
    2: colors.blue.lighten3,
    1: colors.red.lighten2,
    0: colors.grey.lighten2
};
export const GRADE_COLOR_SCALE_4 = {
    4: colors.green.lighten2,
    3: colors.blue.lighten3,
    2: colors.orange.lighten1,
    1: colors.red.lighten2,
    0: colors.grey.lighten2
};
export const THEME_COLORS = {
    primary: colors.orange.base,
    secondary: colors.brown.base,
    accent: colors.deepOrange.base,
    error: colors.pink.base,
    warning: colors.orange.darken4,
    info: colors.blue.base,
    success: colors.green.base
};

export {
    pageContext,
    notificationBus
};


