<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="items"
            :options.sync="options"
            :server-items-length="totalCount"
            :loading="loading"
            sort-by="registration_number"
            single-expand
            show-expand
            :footer-props="{
                'disable-items-per-page': true,
            }"
        >
            <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length">More info about {{ item.title }}</td>
            </template>

            <!-- dynamic slots for all "author" FKs -->
            <template
                v-for="key in 'author supervisor opponent'.split(' ')"
                v-slot:[`item.${key}.full_name`]="{ item }"
            >
                <a @click="addUserFilterFromDataTable(item[key].id)">{{ item[key].full_name }}</a>
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
                {text: 'SN', value: 'registration_number'},
                {text: 'Title', value: 'title'},
                {text: 'Category', value: 'category.title'},
                {text: 'Acad. year', value: 'published_at'},
                {text: 'Author', value: 'author.full_name'},
                {text: 'Supervisor', value: 'supervisor.full_name'},
                {text: 'Opponent', value: 'opponent.full_name'},
                {text: '', value: 'data-table-expand'}
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