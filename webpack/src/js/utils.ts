import Vue from 'vue';

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

const eventBus = new Vue();

export {
    pageContext,
    readFileAsync,
    eventBus
};


