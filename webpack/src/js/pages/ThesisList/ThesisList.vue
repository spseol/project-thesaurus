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
        >
            <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length">
                    <v-row class="my-2">
                        <v-col cols="1" v-text="$t('Abstract')" class="font-weight-bold text-right"></v-col>
                        <v-col cols="6" md="7" sm="11" class="text-justify">
                            <p class="text-justify">
                                {{ item.abstract }}
                            </p>
                        </v-col>
                    </v-row>
                </td>
            </template>

            <!-- dynamic slots for all "author" FKs -->
            <template
                v-for="key in 'author supervisor opponent'.split(' ')"
                v-slot:[`item.${key}.full_name`]="{ item }"
            >
                <a
                    v-if="item[key]"
                    v-text="item[key].full_name"
                    @click="addUserFilterFromDataTable(item[key].id)"
                ></a>
            </template>

        </v-data-table>


        <portal to="navbar-center">
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
        </portal>
    </div>


</template>

<script type="text/tsx">
    import * as _ from 'lodash';
    import Vue from 'vue';
    import ThesisService from './thesis-service';

    export default Vue.extend({
        data() {
            const headers = [
                {text: this.$t('SN'), value: 'registration_number'},
                {text: this.$t('Title'), value: 'title'},
                {text: '', value: 'data-table-expand'},
                {text: this.$t('Category'), value: 'category.title'},
                {text: this.$t('Year'), value: 'published_at'},
                {text: this.$t('Author'), value: 'author.full_name', mapped: 'author__last_name'},
                {text: this.$t('Supervisor'), value: 'supervisor.full_name', mapped: 'supervisor__last_name'},
                {text: this.$t('Opponent'), value: 'opponent.full_name', mapped: 'opponent__last_name'}
            ];
            return {
                items: [],
                totalCount: 0,
                loading: true,
                options: {},
                headers: headers,
                service: new ThesisService(headers),

                userOptions: [],
                filterItems: []
            };
        },
        methods: {
            addUserFilterFromDataTable(id) {
                this.filterItems.push(
                    _.find(this.userOptions, {id})
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

                const resp = await this.service.loadData(this.options, this.filterItems);

                this.items = resp.data.results;
                this.totalCount = resp.data.count;
                this.loading = false;
            }
        },
        async created() {
            await this.load();

            this.debouncedLoad = _.debounce(this.load, 200);
            this.$watch(
                (self) => ([self.options, self.filterItems]),
                this.debouncedLoad,
                {deep: true}
            );
            this.userOptions = await this.service.loadUserOptions();
        }
    });
</script>

<style scoped>

</style>