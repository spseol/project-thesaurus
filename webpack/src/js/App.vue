<template>
    <v-app>
        <v-navigation-drawer app dark clipped v-model="drawer">
            <div class="v-navigation-drawer__content d-flex flex-column justify-space-between">
                <v-list nav>
                    <v-list-item-group color="primary">
                        <v-list-item
                            v-for="item in menuItems" :key="item.text"
                            :to="$i18nRoute(item.to)" exact
                            v-has-perm:[item.perm]
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
                <!-- to avoid flex circumstances of v-list -->
                <div>
                    <v-menu top offset-y>
                        <template v-slot:activator="{ on }">
                            <v-list-item v-on="on">
                                <v-list-item-action>
                                    <v-icon>mdi-white-balance-sunny</v-icon>
                                </v-list-item-action>
                                <v-list-item-content>
                                    <v-list-item-title>
                                        {{ $vuetify.theme.dark ? $t('Dark') : $t('Light') }}
                                    </v-list-item-title>
                                </v-list-item-content>
                            </v-list-item>
                        </template>

                        <v-list>
                            <v-list-item @click="setDark(false)">
                                <v-list-item-title>{{ $t('Light') }}</v-list-item-title>
                            </v-list-item>
                            <v-list-item @click="setDark(true)">
                                <v-list-item-title>{{ $t('Dark') }}</v-list-item-title>
                            </v-list-item>
                        </v-list>
                    </v-menu>

                    <LanguageMenu></LanguageMenu>

                    <v-list-item v-if="pageContext.djangoAdminUrl" :href="pageContext.djangoAdminUrl">
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
            <v-btn :to="$i18nRoute({name: 'dashboard'})" :text="true" class="primary--text hidden-sm-and-down px-0 px-xl-2">
                <v-toolbar-title
                    class="ml-0 pl-1 d-md-flex hidden-sm-and-down black--text"
                >
                    <img height="35" src="../img/thesaurus.svg" class="pr-0 pr-xl-2" alt="Project Thesaurus">

                    <span class="font-weight-bold mt-1 hidden-lg-and-down">THESAURUS</span>
                </v-toolbar-title>
            </v-btn>

            <v-row no-gutters>
                <v-col cols="auto">
                    <portal-target name="navbar-center" slim/>
                </v-col>
            </v-row>

            <v-spacer/>
            <span class="font-weight-medium">
            {{ $vuetify.breakpoint.lgAndUp ? pageContext.user.full_name : pageContext.user.username }}
            </span>
            <v-btn icon :href="pageContext.logoutUrl" x-large class="mr-2">
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

        <v-footer app>
            <v-spacer></v-spacer>
            <span class="px-4">
                <a href="https://github.com/spseol/project-thesaurus">
                <v-icon>mdi-github</v-icon>
                    v{{ pageContext.version }}
                </a> &copy; 2020</span>
        </v-footer>
    </v-app>
</template>


<script type="text/tsx">
import Vue from 'vue';
import {appCache} from './cache';
import LanguageMenu from './components/LanguageMenu.vue';
import {pageContext} from './utils';

export default Vue.extend({
  components: {LanguageMenu},
  data() {
    return {
      pageContext,
      drawer: this.$vuetify.breakpoint.xl && this.$route.name != '404'
    };
  },
  methods: {
    async setDark(v) {
      await appCache.setItem('dark', v);
                this.$vuetify.theme.dark = v;
            }
        },
        computed: {
            menuItems() {
                return [
                    {icon: 'mdi-home', text: this.$t('Dashboard'), to: {name: 'dashboard'}},
                    {
                        icon: 'mdi-book-multiple',
                        text: this.$t('Theses'),
                        to: {name: 'thesis-list'},
                        perm: 'thesis.view_thesis'
                    },
                    {
                        icon: 'mdi-book-plus',
                        text: this.$t('Prepare admission'),
                        to: {name: 'thesis-prepare'},
                        perm: 'thesis.add_thesis'
                    },
                    // {icon: 'mdi-pencil', text: this.this.$t('Submit review'), to: {name: 'reviews'}, perm: 'thesis.add_review'},
                    {
                        icon: 'mdi-calendar-account',
                        text: this.$t('Reservations'),
                        to: {name: 'reservation-list'},
                        perm: 'thesis.change_reservation'
                    },
                    {
                        icon: 'mdi-printer',
                        text: this.$t('Exports'),
                        to: {name: 'exports'},
                        perm: 'accounts.view_user'
                    },
                  // {icon: 'mdi-cog', text: this.$t('Settings'), to: {name: 'settings'}}
                ];
            }
        },
        watch: {
            $route(to, from) {
                if (to.name == '404')
                    this.drawer = false;
            }
        },
        async created() {
            this.$vuetify.theme.dark = await appCache.getItem('dark') || false;
        }
    });
</script>