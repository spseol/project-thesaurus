<template>
    <v-menu top offset-y>
        <template v-slot:activator="{ on }">
            <v-list-item v-on="on">
                <v-list-item-action>
                    <v-icon>mdi-format-letter-case</v-icon>
                </v-list-item-action>
                <v-list-item-content>
                    <v-list-item-title>
                        {{ localeName }}
                    </v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </template>

        <v-list>
            <v-list-item
                v-for="[code, name] in languages"
                :key="code"
                @click="setLang(code)"
            >
                <v-list-item-title>{{ name }}</v-list-item-title>
            </v-list-item>
        </v-list>
    </v-menu>
</template>
<script type="text/tsx">
    import * as _ from 'lodash';
    import qs from 'qs';
    import Vue from 'vue';
    import Axios from '../axios';
    import {pageContext} from '../utils';

    export default Vue.extend({
        data: () => ({
            languages: pageContext.languages
        }),
        computed: {
            localeName() {
                return (_.find(
                    pageContext.languages,
                    ([code, name]) => code == this.locale
                ) || ['en', 'Unknown'])[1];
            },
            locale: {
                get() {
                    return this.$i18n.locale;
                },
                set(locale) {
                    pageContext.locale = this.$root.$i18n.locale = locale;
                }
            }
        },
        methods: {
            async setLang(language) {
                if (language == this.locale) return;
                let resp = await Axios.post('/api/i18n/setlang/', qs.stringify({language}));

                this.locale = language;
                Axios.defaults.headers['Accept-Language'] = language;
                this.$router.push({
                    params: {...(this.$route.params || {}), locale: language},
                    name: this.$route.name
                });
                return;
            }
        }
    });
</script>