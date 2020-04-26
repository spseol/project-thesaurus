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
    import Vue from 'vue';
    import Axios from '../axios';

    export default Vue.extend({
        data: () => ({
            languages: window.Thesaurus.settings.languages,
            locale: window.Thesaurus.settings.locale,
            localeName: (_.find(
                window.Thesaurus.settings.languages,
                ([code, name]) => code == window.Thesaurus.settings.locale
            ) || ['en', 'Unknown'])[1]
        }),
        methods: {
            async setLang(code) {
                if (code == this.locale) return;
                let resp = await Axios.post('/api/i18n/setlang/', {
                    language: code
                });
                // TODO: router call?
                window.location.href = `/${code}`;
            }
        }
    });
</script>