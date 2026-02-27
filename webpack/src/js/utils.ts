import * as _ from 'lodash-es';
import Vue from 'vue';
import colors from 'vuetify/lib/util/colors';
import Axios from './axios';
import {ThesisTableHeader, User} from './types';
import {hasPerm} from './user';

class FlashMessage {
    type: string;
    text: string;
}

class PageContext {
    user: User;
    locale: string;
    djangoAdminUrl: string;
    logoutUrl: string;
    languages: Array<string>;
    groups: Array<string>;
    version: string;
    messages: Array<FlashMessage>;

    THESIS_SUBMIT_USE_CONFIRM_DIALOG: boolean;

    constructor() {
        return new Proxy(this, {
            get(self, field: string) {
                return window['Thesaurus'].pageContext[field];
            },
            set(self, field: string, value: any, receiver: any): boolean {
                return window['Thesaurus'].pageContext[field] = value;
            }
        });
    }
}

const pageContext = new PageContext();

export function formatDataTableOrdering({sortBy, sortDesc}, headers: ThesisTableHeader[]) {
    let header;
    const remap = (value) => (
        (header = _.find(headers, {value})) && header.mapped)
        ? header.mapped
        : value.replace('.', '__');

    return _.map(
        _.zip(sortBy, sortDesc),
        ([col, desc]) => `${desc ? '-' : ''}${remap(col).split('.')[0]}`
    ).join(',');
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


class Flash extends Object {
    text: string;
    color?: string;
}

class EventBus extends Vue {
    public flash(flash: Flash) {
        this.$emit('flash', flash);
    }

    public debug(text: string) {
        this.$emit('flash', {text, icon: 'mdi-android-debug-bridge'});
    }

    public info(text: string) {
        this.$emit('flash', {text, color: 'info', icon: 'mdi-exclamation-thick'});
    }

    public success(text: string) {
        this.$emit('flash', {text, color: 'success', icon: 'mdi-check-bold'});
    }

    public warning(text: string) {
        this.$emit('flash', {text, color: 'warning', icon: 'mdi-exclamation-thick'});
    }

    public error(text: string) {
        this.$emit('flash', {text, color: 'danger', icon: 'mdi-exclamation-thick'});
    }

}

const notificationBus = new EventBus();

export const GRADE_COLOR_SCALE_3 = {
    3: colors.green.lighten1,
    2: colors.blue.lighten2,
    1: colors.red.lighten1,
    0: colors.grey.lighten1
};
export const GRADE_COLOR_SCALE_4 = {
    4: colors.green.lighten1,
    3: colors.blue.lighten2,
    2: colors.orange.base,
    1: colors.red.lighten1,
    0: colors.grey.lighten1
};
export const THEME_LIGHT_COLORS = {
    primary: colors.orange.base,
    secondary: colors.brown.base,
    accent: colors.deepOrange.base,
    error: colors.pink.base,
    warning: colors.orange.darken4,
    info: colors.blue.base,
    success: colors.green.base
};
export const THEME_DARK_COLORS = {
    primary: colors.orange.darken2,
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


