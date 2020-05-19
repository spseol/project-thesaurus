const Axios = require('axios');
const fs = require('fs');
const path = require('path');

const LANGUAGES = ['cs', 'en'];
const LANGUAGES_DEFAULTS = {
    en: (key) => key,
    cs: (key) => '',
};
const sortedReplacer = (key, value) =>
    value instanceof Object && !(value instanceof Array) ?
        Object.keys(value)
            .sort()
            .reduce((sorted, key) => {
                sorted[key] = value[key];
                return sorted;
            }, {}) :
        value;


for (let i in LANGUAGES) {
    const lang = LANGUAGES[i];

    const localePath = path.resolve(__dirname, `../src/js/locale/${lang}.json`);

    let savedLocale = JSON.parse(fs.readFileSync(localePath).toString());

    Axios.get('http://localhost:8080/api/i18n/catalog', {
        headers: {
            'Accept-language': lang,
        },
    }).then(({data}) => {
        const djangoLocale = data.catalog;

        let resultLocale = {};
        for (let key in savedLocale) {

            resultLocale[key] = savedLocale[key] || djangoLocale[key] || LANGUAGES_DEFAULTS[lang](key);
        }

        fs.writeFileSync(localePath, JSON.stringify(resultLocale, sortedReplacer, 2));
        return true;
    }).catch((e) => {
        console.log('Something went wrong:', e);
    });


}
