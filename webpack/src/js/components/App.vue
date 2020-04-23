<template>
    <v-app
    >
        <v-navigation-drawer app :clipped="true" v-model="drawer">
            <v-list dense>
                <template v-for="item in items">
                    <v-row
                        v-if="item.heading"
                        :key="item.heading"
                        align="center"
                    >
                        <v-col cols="6">
                            <v-subheader v-if="item.heading">
                                {{ item.heading }}
                            </v-subheader>
                        </v-col>
                        <v-col
                            cols="6"
                            class="text-center"
                        >
                            <a
                                href="#!"
                                class="body-2 black--text"
                            >EDIT</a>
                        </v-col>
                    </v-row>
                    <v-list-group
                        v-else-if="item.children"
                        :key="item.text"
                        v-model="item.model"
                        :prepend-icon="item.model ? item.icon : item['icon-alt']"
                        append-icon=""
                    >
                        <template v-slot:activator>
                            <v-list-item-content>
                                <v-list-item-title>
                                    {{ item.text }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </template>
                        <v-list-item
                            v-for="(child, i) in item.children"
                            :key="i"
                            link
                        >
                            <v-list-item-action v-if="child.icon">
                                <v-icon>{{ child.icon }}</v-icon>
                            </v-list-item-action>
                            <v-list-item-content>
                                <v-list-item-title>
                                    {{ child.text }}
                                </v-list-item-title>
                            </v-list-item-content>
                        </v-list-item>
                    </v-list-group>
                    <v-list-item
                        v-else
                        :key="item.text"
                        link
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
                </template>
            </v-list>
        </v-navigation-drawer>

        <v-app-bar app color="orange accent-3" clipped-left>
            <v-app-bar-nav-icon @click.stop="drawer = !drawer"/>
            <v-toolbar-title
                class="ml-0 pl-4 d-flex hidden-sm-and-down"
            >
                <img height="35" src="../../img/thesaurus.svg" class="pr-4" alt="Project Thesaurus">

                <span class="font-weight-bold mt-1">THESAURUS</span>
            </v-toolbar-title>

            <!--            <v-text-field-->
            <!--                flat-->
            <!--                solo-inverted-->
            <!--                hide-details-->
            <!--                prepend-inner-icon="mdi-magnify"-->
            <!--                label="Search"-->
            <!--                class="hidden-sm-and-down"-->
            <!--            />-->
            <v-spacer/>
            <v-btn icon>
                <v-icon>mdi-apps</v-icon>
            </v-btn>
            <v-btn icon>
                <v-icon>mdi-bell</v-icon>
            </v-btn>
        </v-app-bar>

        <v-content>
            <v-container fluid>

                <ThesisList></ThesisList>
                <!--                <router-view></router-view>-->
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
    import ThesisList from './ThesisList/ThesisList';

    export default {
        components: {ThesisList},
        data: () => ({
            drawer: true,
            items: [
                {icon: 'mdi-book-multiple', text: 'Theses'},
                {icon: 'mdi-book-plus', text: 'Prepare thesis'},
                {icon: 'mdi-calendar-account', text: 'Reservations'},
                {icon: 'mdi-printer', text: 'Exports'},
                {icon: 'mdi-settings', text: 'Settings'},
                /*
                {
                    icon: 'mdi-chevron-up',
                    'icon-alt': 'mdi-chevron-down',
                    text: 'Labels',
                    model: true,
                    children: [
                        {icon: 'mdi-plus', text: 'Create label'},
                    ],
                },
                {
                    icon: 'mdi-chevron-up',
                    'icon-alt': 'mdi-chevron-down',
                    text: 'More',
                    model: false,
                    children: [
                        {text: 'Import'},
                        {text: 'Export'},
                        {text: 'Print'},
                        {text: 'Undo changes'},
                        {text: 'Other contacts'},
                    ],
                },
                {icon: 'mdi-message', text: 'Send feedback'},
                {icon: 'mdi-help-circle', text: 'Help'},
                {icon: 'mdi-cellphone-link', text: 'App downloads'},
                {icon: 'mdi-keyboard', text: 'Go to the old version'},
                 */
            ],
        }),
        mounted() {
        },
    };
</script>