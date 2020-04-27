<template>
    <v-app>
        <v-navigation-drawer
            app
            dark
            :clipped="true"
            v-model="drawer"
        >
            <div class="v-navigation-drawer__content d-flex flex-column justify-space-between">

                <v-list nav shaped>

                    <v-list-item-group color="primary">
                        <v-list-item
                            v-for="item in items"
                            :key="item.text"
                            :to="item.to"
                        >
                            <v-list-item-action>
                                <v-icon>{{ item.icon }}</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>
                                    {{ item.text }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-item-group>
                </v-list>
                <!-- to avoid flex circumstances of v-list-thesis -->
                <div>
                    <LanguageMenu/>

                    <v-list-item v-if="djangoAdminUrl" :href="djangoAdminUrl">
                        <v-list-item-action>
                            <v-icon>mdi-share</v-icon>
                        </v-list-item-action>
                        <v-list-item-content>
                            <v-list-item-title>
                                {{ $t('Django Administration') }}
                            </v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </div>

            </div>

        </v-navigation-drawer>

        <v-app-bar app color="primary accent-3" clipped-left>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <v-btn :to="{name: 'home'}" :text="true" class="primary--text hidden-sm-and-down">
                <v-toolbar-title
                    class="ml-0 pl-1 d-md-flex hidden-sm-and-down black--text"
                >
                    <img height="35" src="../img/thesaurus.svg" class="pr-2" alt="Project Thesaurus">

                    <span class="font-weight-bold mt-1">THESAURUS</span>
                </v-toolbar-title>
            </v-btn>

            <v-col cols="auto">
                <portal-target name="navbar-center" slim/>
            </v-col>

            <v-spacer/>
            <span class="font-weight-medium">
            {{ username }}
            </span>
            <v-btn icon href="/logout" x-large class="mr-2">
                <v-icon large>mdi-logout</v-icon>
            </v-btn>
        </v-app-bar>

        <v-content>
            <v-container fluid>
                <v-fade-transition mode="out-in">
                    <router-view></router-view>

                </v-fade-transition>
            </v-container>
        </v-content>

        <v-footer
            app
        >
            <v-spacer></v-spacer>
            <span class="px-4">&copy; 2020</span>
        </v-footer>
    </v-app>
</template>


<script type="text/tsx">
    import Vue from 'vue';
    import LanguageMenu from './components/LanguageMenu';

    export default Vue.extend({
        components: {LanguageMenu},
        data() {
            return {
                username: window['Thesaurus'].settings.username,
                djangoAdminUrl: window['Thesaurus'].settings.djangoAdminUrl,
                drawer: this.$vuetify.breakpoint.mdAndUp,
                drawerItem: 0,
                items: [
                    {icon: 'mdi-book-multiple', text: this.$t('Theses'), to: {name: 'thesis-list'}},
                    {icon: 'mdi-book-plus', text: this.$t('Prepare admission'), to: {name: 'thesis-prepare'}},
                    {icon: 'mdi-calendar-account', text: this.$t('Reservations'), to: {name: 'reservations'}},
                    {icon: 'mdi-printer', text: this.$t('Exports'), to: {name: 'exports'}},
                    {icon: 'mdi-settings', text: this.$t('Settings'), to: {name: 'settings'}}
                ]
            };
        }
    });
</script>