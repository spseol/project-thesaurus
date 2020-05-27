import Vue from 'vue';
import colors from 'vuetify/lib/util/colors';
import {User} from './types';

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


function readFileAsync(file) {
    return new Promise((resolve, reject) => {
        let reader = new FileReader();

        reader.onload = () => {
            resolve(reader.result);
        };

        reader.onerror = reject;

        reader.readAsArrayBuffer(file);
    });
}

const pageContext = new PageContext();

class Flash extends Object {
    text: string;
    color?: string;
    type?: string;
}

class EventBus extends Vue {
    public flash(flash: Flash) {
        this.$emit('flash', flash);
    }
}

const eventBus = new EventBus();

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
    readFileAsync,
    eventBus
};


