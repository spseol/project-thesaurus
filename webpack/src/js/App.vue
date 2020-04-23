<template>
    <v-app
    >
        <v-navigation-drawer app :clipped="true" v-model="drawer">
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
        </v-navigation-drawer>

        <v-app-bar app color="orange accent-3" clipped-left>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <v-toolbar-title
                class="ml-0 pl-2 d-md-flex hidden-sm-and-down"
            >
                <img height="35" src="../img/thesaurus.svg" class="pr-2" alt="Project Thesaurus">

                <span class="font-weight-bold mt-1">THESAURUS</span>
            </v-toolbar-title>
            <v-spacer></v-spacer>

            <v-text-field
                flat
                solo-inverted
                hide-details
                prepend-inner-icon="mdi-magnify"
                label="Search"
                v-model.sync="search"
            />

            <v-spacer/>
            <v-btn icon>
                <v-icon>mdi-apps</v-icon>
            </v-btn>
            <v-btn icon href="/logout">
                <v-icon>mdi-logout</v-icon>
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
            <span class="px-4">Josef Kolář &copy; 2020</span>
        </v-footer>
    </v-app>
</template>


<script>
    import ThesisList from './pages/ThesisList/ThesisList';

    export default {
        components: {ThesisList},
        data() {
            return {
                drawer: this.$vuetify.breakpoint.mdAndUp,
                search: '',
                drawerItem: 0,
                items: [
                    {icon: 'mdi-book-multiple', text: 'Theses', to: {name: 'thesis-list'}},
                    {icon: 'mdi-book-plus', text: 'Prepare thesis', to: {name: 'thesis-create'}},
                    {icon: 'mdi-calendar-account', text: 'Reservations', to: {name: 'reservations'}},
                    {icon: 'mdi-printer', text: 'Exports', to: {name: 'exports'}},
                    {icon: 'mdi-settings', text: 'Settings', to: {name: 'settings'}},
                ],
            };
        },
    };
</script>