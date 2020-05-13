<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="items"
            :options.sync="options"
            :server-items-length="totalCount"
            :loading="loading"
            sort-by="published_at"
            sort-desc
            show-expand
            :footer-props="{
                'disable-items-per-page': true,
            }"
            class="body-2"
        >
            <template v-slot:expanded-item="{ headers, item }">
                <td :colspan="headers.length" class="white lighten-5">
                    <ThesisDetailPanel :thesis="item"/>
                </td>
            </template>

            <template v-slot:item.title="{ item }">
                {{ item.title }}
            </template>

            <template v-slot:item.state="{ item }">
                <div class="text-center">
                    <ThesisListActionBtn
                        :thesis="item"
                        :title="item.state"
                        :loading="loading"
                        @reload="load"
                    ></ThesisListActionBtn>
                </div>
            </template>

            <template
                v-slot:item.authors="{ item }"
            >
                <template
                    v-if="item.authors"
                    v-for="(author, i) in item.authors"
                >
                    <span v-if="i !== 0">, </span>
                    <!-- TODO: think about idea of clickable filters -->
                    <template v-if="false && isPossibleUserFilter(author)">
                        <a
                            v-text="author.full_name"
                            @click="addUserFilterFromDataTable(author.username)"
                        ></a>
                    </template>
                    <template v-else>
                        {{ author.full_name }}
                    </template>
                </template>
            </template>

            <template
                v-for="key in 'supervisor opponent'.split(' ')"
                v-slot:[`item.${key}.full_name`]="props"
                v-has-perm:thesis.change_thesis
            >
                <!-- edit dialog for users with permission to edit -->
                <v-edit-dialog
                    v-if="isThesisEditAllowed(props.item)"
                    :return-value="userEditDialogModel"
                    @save="persistThesisEdit(props.item.id, {[key + '_id']: userEditDialogModel.value})"
                    @open="userEditDialogModel = props.item[key] ? {text: props.item[key].full_name, value: props.item[key].id} : null"
                >
                    {{ (props.item[key] || {full_name: '---'}).full_name }}
                    <template v-slot:input>
                        <v-combobox
                            :items="teacherOptions"
                            v-model="userEditDialogModel"
                            return-object autofocus
                            :label="$t(key)"
                        ></v-combobox>
                    </template>
                </v-edit-dialog>

                <!-- filter link for users without permission -->
                <a v-else-if="props.item[key]"
                    v-text="props.item[key].full_name"
                    @click="addUserFilterFromDataTable(props.item[key].username)"
                ></a>
            </template>
        </v-data-table>

        <portal to="navbar-center">
            <v-toolbar dense color="transparent" elevation="0">
                <v-combobox
                    v-model="filterItems" multiple :items="userOptions"
                    flat solo-inverted solo prepend-inner-icon="mdi-magnify"
                    hide-details clearable hide-selected chips
                    :label="$t('Search')"
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
                        :value="value" v-text="text" :key="value" class="text-transform-none"
                    ></v-btn>
                </v-btn-toggle>

                <v-btn icon v-if="categoryFilter" @click="categoryFilter = null">
                    <v-icon>mdi-close</v-icon>
                </v-btn>

                <v-select
                    :items="thesisYearOptions" v-model="thesisYearFilter" clearable
                    flat solo-inverted hide-details prepend-inner-icon="mdi-calendar"
                ></v-select>
            </v-toolbar>
        </portal>
    </div>
</template>

<script type="text/tsx">
    import * as _ from 'lodash';
    import Vue from 'vue';
    import Axios from '../../axios';
    import hasPerm from '../../user';
    import {eventBus} from '../../utils';
    import ThesisService from './thesis-service';
    import ThesisDetailPanel from './ThesisDetailPanel';
    import ThesisListActionBtn from './ThesisListActionBtn';

    export default Vue.extend({
        components: {ThesisListActionBtn, ThesisDetailPanel},
        data() {
            return {
                items: [],
                totalCount: 0,
                loading: true,
                options: {},
                thesisService: new ThesisService(),

                userOptions: [],
                categoryOptions: [],
                teacherOptions: [],
                thesisYearOptions: [],
                filterItems: [],
                categoryFilter: null,
                thesisYearFilter: null,

                userEditDialogModel: {},
                hasThesisEditPerm: false
            };
        },
        methods: {
            addUserFilterFromDataTable(username) {
                this.filterItems.push(
                    _.find(this.userOptions, {username})
                );
            },
            removeFromFilter(item) {
                // TODO: eeeh
                this.filterItems.splice(this.filterItems.indexOf(item), 1);
                this.filterItems = [...this.filterItems];
            },
            userOptionsFilter(item, queryText, itemText) {
                itemText = itemText.toLowerCase();
                return _.some(
                    queryText.toLowerCase().split(/\s+/g),
                    token => itemText.includes(token)
                );
            },
            isPossibleUserFilter({username}) {
                return !!_.find(this.userOptions, {username});
            },
            isThesisEditAllowed({state}) {
                // TODO: list all states
                return this.hasThesisEditPerm && state != 'published';
            },

            async persistThesisEdit(thesisId, data) {
                this.loading = true;
                await Axios.patch(`/api/v1/thesis/${thesisId}`, data);
                eventBus.flash({color: 'success', text: this.$t('Successfully saved!')});
                await this.load();
            },
            async load() {
                this.loading = true;

                const resp = await this.thesisService.loadData(
                    this.options,
                    _.filter(_.concat(this.filterItems, this.categoryFilter, this.thesisYearFilter)),
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
                    {text: '', value: 'data-table-expand'},

                    {text: this.$t('Title'), value: 'title', width: '30%'},
                    lgAndUp && {text: this.$t('SN'), value: 'registration_number'},
                    {text: this.$t('Category'), value: 'category.title'},

                    mdAndUp && {text: this.$t('Year'), value: 'published_at'},

                    {text: this.$t('Authors'), value: 'authors'},

                    lgAndUp && {
                        text: this.$t('Supervisor'),
                        value: 'supervisor.full_name',
                        mapped: 'supervisor__last_name'
                    },
                    lgAndUp && {text: this.$t('Opponent'), value: 'opponent.full_name', mapped: 'opponent__last_name'}
                ];

                headers.push({text: '', value: 'state', width: '18em'});
                return _.compact(headers);
            }
        },
        async created() {
            this.debouncedLoad = _.debounce(this.load, 200);
            this.$watch(
                (s) => ([s.options]),
                this.debouncedLoad,
                {deep: true, immediate: true}
            );
            this.$watch(
                (s) => ([s.filterItems, s.categoryFilter, s.thesisYearFilter]),
                () => {
                    this.options.page = 1;
                    this.debouncedLoad();
                }
            );

            [
                this.userOptions,
                this.categoryOptions,
                this.thesisYearOptions
            ] = _.map(await Promise.all([
                Axios.get('/api/v1/user-filter-options'),
                Axios.get('/api/v1/category-options'),
                Axios.get('/api/v1/thesis-year-options')
            ]), _.property('data'));

            this.hasThesisEditPerm = await hasPerm('thesis.change_thesis');

            if (await hasPerm('accounts.view_user'))
                this.teacherOptions = (await Axios.get('/api/v1/teacher-options')).data;
        }
    });
</script>
