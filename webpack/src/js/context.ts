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

const pageContext = new Context();

export default pageContext;

