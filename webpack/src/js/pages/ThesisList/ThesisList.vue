<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="items"
            :options.sync="options"
            :server-items-length="totalCount"
            :loading="loading"
            sort-by="registration_number"
            show-expand
            :footer-props="{
                'disable-items-per-page': true,
            }"
            class="body-2"
        >
            <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length" class="orange lighten-5">
                    <ThesisDetailPanel :thesis="item"/>
                </td>
            </template>

            <template v-slot:item.available_for_reservation="{ item }">
                <div class="text-center">
                    <v-btn
                        v-if="item.reservable && item.available_for_reservation"
                        v-text="$t('Borrow')"
                        small color="info" outlined
                    ></v-btn>
                    <v-btn
                        v-if="item.reservable && !item.available_for_reservation"
                        v-text="$t('Borrowed')"
                        x-small depressed
                    ></v-btn>
                    <v-btn
                        v-if="!item.reservable"
                        v-text="$t('Not reservable')"
                        x-small depressed
                    ></v-btn>
                </div>
            </template>

            <!-- dynamic slots for all "author" FKs -->
            <template
                v-for="key in 'author supervisor opponent'.split(' ')"
                v-slot:[`item.${key}.full_name`]="{ item }"
            >
                <a
                    v-if="item[key]"
                    v-text="item[key].full_name"
                    @click="addUserFilterFromDataTable(item[key].username)"
                ></a>
            </template>

        </v-data-table>


        <portal to="navbar-center">
            <v-toolbar dense color="transparent" elevation="0">
                <v-combobox
                    :items="userOptions"
                    flat
                    solo-inverted solo
                    hide-details
                    clearable
                    hide-selected
                    prepend-inner-icon="mdi-magnify"
                    label="Search"
                    v-model="filterItems"
                    multiple
                    chips
                    :filter="userOptionsFilter"
                    menu-props="closeOnContentClick"
                >
                    <template v-slot:selection="{ attrs, item, select, selected }">
                        <v-chip
                            v-bind="attrs"
                            :input-value="selected"
                            close
                            @click="select"
                            @click:close="removeFromFilter(item)"
                        >
                            <v-avatar left>
                                <v-icon v-if="item.id">mdi-account</v-icon>
                                <v-icon v-else>mdi-format-letter-case</v-icon>
                            </v-avatar>
                            <strong>{{ item.text || item }}</strong>
                        </v-chip>
                    </template>

                    <template v-slot:item="{ item }">
                        {{ item.text || item }}
                    </template>
                </v-combobox>
                <v-btn-toggle
                    v-model="categoryFilter"
                    group
                >
                    <v-btn
                        v-for="{text, value} in categoryOptions"
                        :value="value" v-text="text" :key="value"
                    ></v-btn>
                </v-btn-toggle>

                <v-btn icon v-if="categoryFilter" @click="categoryFilter = null">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-toolbar>
        </portal>
    </div>


</template>

<script type="text/tsx">
    import * as _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';
    import ThesisService from './thesis-service';
    import ThesisDetailPanel from './ThesisDetailPanel.vue';

    export default Vue.extend({
        components: {ThesisDetailPanel},
        data() {
            return {
                items: [],
                totalCount: 0,
                loading: true,
                options: {},
                service: new ThesisService(),

                userOptions: [],
                categoryOptions: [],
                filterItems: [],
                categoryFilter: null
            };
        },
        methods: {
            addUserFilterFromDataTable(username) {
                this.filterItems.push(
                    _.find(this.userOptions, {username})
                );
            },
            removeFromFilter(item) {
                this.filterItems.splice(this.filterItems.indexOf(item), 1);
                this.filterItems = [...this.filterItems];
            },

            userOptionsFilter(item, queryText, itemText) {
                return itemText.toLowerCase().includes(queryText.toLowerCase());
            },

            async load() {
                this.loading = true;

                const resp = await this.service.loadData(
                    this.options,
                    _.filter(_.concat(this.filterItems, this.categoryFilter)),
                    this.headers
                );

                this.items = resp.data.results;
                this.totalCount = resp.data.count;
                this.loading = false;
            }
        },
        computed: {
            headers() {
                const lgAndUp = this.$vuetify.breakpoint.lgAndUp;
                const mdAndUp = this.$vuetify.breakpoint.mdAndUp;
                const headers = [
                    lgAndUp && {text: this.$t('SN'), value: 'registration_number'},

                    {text: this.$t('Title'), value: 'title'},
                    {text: '', value: 'data-table-expand'},
                    {text: this.$t('Category'), value: 'category.title'},

                    mdAndUp && {text: this.$t('Year'), value: 'published_at'},

                    {text: this.$t('Author'), value: 'author.full_name'},

                    lgAndUp && {text: this.$t('Supervisor'), value: 'supervisor.full_name'},
                    lgAndUp && {text: this.$t('Opponent'), value: 'opponent.full_name'}
                ];


                headers.push({text: this.$t('State'), value: 'available_for_reservation'});
                return _.filter(headers, _.isPlainObject);
            }
        },
        async created() {
            await this.load();

            this.debouncedLoad = _.debounce(this.load, 200);
            this.$watch(
                (self) => ([self.options, self.filterItems, self.categoryFilter]),
                this.debouncedLoad,
                {deep: true}
            );
            this.userOptions = await this.service.loadUserOptions();
            this.categoryOptions = (await Axios.get('/api/v1/category-options')).data;
        }
    });
</script>
