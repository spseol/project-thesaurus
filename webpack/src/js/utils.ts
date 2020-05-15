import Vue from 'vue';
import colors from 'vuetify/lib/util/colors';

class Context {
    username: string;
    locale: string;
    djangoAdminUrl: string;
    languages: Array<string>;
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

const pageContext = new Context();

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
export {
    pageContext,
    readFileAsync,
    eventBus
};


