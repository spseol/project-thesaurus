<template>
    <div>
        <v-data-table
            :headers="headers"
            :items="theses.results"
            :options.sync="options"
            :server-items-length="theses.count"
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
                    <thesis-detail-panel :thesis="item">
                    </thesis-detail-panel>
                </td>
            </template>

            <template v-slot:item.edit="{ item }">
                <v-dialog :fullscreen="$vuetify.breakpoint.smAndDown" max-width="80em"
                    v-model="item.editDialog">
                    <template v-slot:activator="{ on }">
                        <v-btn icon v-on="on" small>
                            <v-icon>mdi-file-document-edit-outline</v-icon>
                        </v-btn>
                    </template>
                    <ThesisEditPanel
                        :thesis="item"
                        @reload="load" @close="item.editDialog = false"
                    ></ThesisEditPanel>
                </v-dialog>
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

            <template v-slot:item.authors="{ item }">
                <span class="caption">
                {{ item.authors.map(a => a.full_name).join(', ') }}
                </span>
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
                    :save-text="$t('Save change')" :cancel-text="$t('Cancel edit')"
                    @save="persistThesisEdit(props.item.id, {[key + '_id']: userEditDialogModel.value})"
                    @open="userEditDialogModel = props.item[key] ? {text: props.item[key].full_name, value: props.item[key].id} : null"
                    large
                >
                    {{ (props.item[key] || {full_name: '---'}).full_name }}

                    <template v-slot:input>
                        <v-combobox
                            :items="optionsStore.teacher"
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

            <template v-slot:item.audit="{ item }">
                <audit-for-instance
                    model-name="thesis.thesis" :model-pk="item.id" small
                ></audit-for-instance>
            </template>
        </v-data-table>

        <!-- didnt find any better way to stop portal in case of another page view with disabled keep-alive -->
        <portal to="navbar-center" v-if="$route.name === 'thesis-list'">
            <v-toolbar dense color="transparent" elevation="0">
                <v-combobox
                    v-model="filterItems" multiple :items="optionsStore.userFilter"
                    flat solo-inverted solo prepend-inner-icon="mdi-magnify"
                    hide-details clearable chips
                    :label="$t('Search')"
                    :filter="userOptionsFilter"
                    menu-props="closeOnContentClick"
                >
                    <template v-slot:selection="{ attrs, item, select, selected, index, value }">
                        <!-- chip if item is user or manually types text -->
                        <v-chip v-if="!item.value || index === 0"
                            v-bind="attrs" :input-value="selected"
                            close @click="select" @click:close="removeFromFilter(item)"
                        >
                            <v-avatar left>
                                <v-icon v-if="item.value">mdi-account</v-icon>
                                <v-icon v-else>mdi-format-letter-case</v-icon>
                            </v-avatar>
                            <strong>{{ item.text || item }}</strong>
                        </v-chip>
                        <!-- maybe too much magic -->
                        <span
                            v-if="index === 1 && filterItems.length - manualFilterItems.length - (filterItems[0].value ? 1 : 0) > 0"
                            class="caption order-last"
                        >(+{{ filterItems.length - manualFilterItems.length - (filterItems[0].value ? 1 : 0) }} others)</span>
                    </template>

                    <template v-slot:item="{ item }">
                        {{ item.text || item }}
                    </template>
                </v-combobox>

                <v-divider v-if="$vuetify.breakpoint.mdAndUp" vertical class="mx-1"></v-divider>
                <v-select v-if="$vuetify.breakpoint.mdAndUp"
                    :items="optionsStore.category" v-model="categoryFilter" clearable
                    solo solo-inverted flat hide-details prepend-inner-icon="mdi-filter-outline"
                    :label="$t('Category')" style="max-width: 10em"
                ></v-select>

                <v-divider vertical class="mx-1" v-if="$vuetify.breakpoint.smAndUp"></v-divider>
                <v-select v-if="$vuetify.breakpoint.smAndUp"
                    :items="optionsStore.thesisYear" v-model="thesisYearFilter" clearable
                    flat solo-inverted hide-details prepend-inner-icon="mdi-calendar"
                    :label="$t('Publication year')" style="max-width: 10em"
                ></v-select>
            </v-toolbar>
        </portal>
    </div>
</template>

<script type="text/tsx">
    import * as _ from 'lodash';
    import Vue from 'vue';
    import {mapState} from 'vuex';
    import AuditForInstance from '../../components/AuditForInstance.vue';
    import {OPTIONS_ACTIONS} from '../../store/options';
    import {PERMS, PERMS_ACTIONS} from '../../store/perms';

    import {optionsStore, permsStore, thesisStore} from '../../store/store';
    import {THESIS_ACTIONS} from '../../store/thesis';
    import {notificationBus} from '../../utils';
    import ThesisEditPanel from './ThesisEditPanel.vue';
    import ThesisListActionBtn from './ThesisListActionBtn.vue';


    export default Vue.extend({
        components: {
            AuditForInstance,
            ThesisEditPanel,
            ThesisListActionBtn,
            ThesisDetailPanel: () => import('./ThesisDetailPanel.vue')
        },
        data() {
            return {
                loading: true,
                options: {},

                filterItems: [],
                categoryFilter: null,
                thesisYearFilter: null,

                userEditDialogModel: {}
            };
        },
        methods: {
            ...thesisStore.mapActions([
                THESIS_ACTIONS.LOAD_THESES,
                THESIS_ACTIONS.EDIT_THESIS
            ]),
            ...optionsStore.mapActions([OPTIONS_ACTIONS.LOAD_OPTIONS]),
            ...permsStore.mapActions([PERMS_ACTIONS.LOAD_PERMS]),
            addUserFilterFromDataTable(username) {
                this.filterItems.push(
                    _.find(this.optionsStore.userFilter, {username})
                );
            },
            removeFromFilter(item) {
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
            isThesisEditAllowed({state}) {
                // TODO: list all states
                return this.perms[PERMS.CHANGE_THESIS] && state != 'published';
            },

            async persistThesisEdit(thesis_id, data) {
                this.loading = true;
                await this[THESIS_ACTIONS.EDIT_THESIS]({
                    ...data,
                    id: thesis_id
                });
                notificationBus.success(this.$t('Successfully saved!'));
                this.loading = false;
            },
            async load() {
                this.loading = true;

                await this[THESIS_ACTIONS.LOAD_THESES]({
                    options: this.options,
                    filters: _.filter(_.concat(this.filterItems, this.categoryFilter, this.thesisYearFilter)),
                    headers: this.headers
                });

                this.loading = false;
            }
        },
        computed: {
            ...thesisStore.mapState(['theses']),
            ...permsStore.mapState(['perms']),
            ...mapState({optionsStore: 'options'}),
            headers() {
                const lgAndUp = this.$vuetify.breakpoint.lgAndUp;
                const mdAndUp = this.$vuetify.breakpoint.mdAndUp;
                const headers = [
                    {text: '', value: 'data-table-expand'},

                    {text: this.$t('Title'), value: 'title', width: '25%'},

                    this.perms[PERMS.CHANGE_THESIS] && lgAndUp && {text: this.$t('SN'), value: 'registration_number'},
                    {text: this.$t('Category'), value: 'category.title'},

                    mdAndUp && {text: this.$t('Year'), value: 'published_at'},

                    {
                        text: this.$t('Authors'), value: 'authors',
                        mapped: 'authors__username',
                        width: '15%'
                    },

                    lgAndUp && {
                        text: this.$t('Supervisor'),
                        value: 'supervisor.full_name',
                        mapped: 'supervisor__last_name',
                        width: '10%'
                    },
                    lgAndUp && {
                        text: this.$t('Opponent'),
                        value: 'opponent.full_name',
                        mapped: 'opponent__last_name',
                        width: '10%'
                    },
                    this.perms[PERMS.CHANGE_THESIS] && {text: '', value: 'edit'}
                ];

                headers.push({text: '', value: 'state', width: '10%'});
                this.perms[PERMS.VIEW_AUDIT] && headers.push({text: '', value: 'audit'});
                return _.compact(headers);
            },
            manualFilterItems() {
                return _.filter(this.filterItems, _.isString);
            }
        },
        async created() {
            this.debouncedLoad = _.debounce(this.load, 200);
            this.$watch(
                (vm) => ([vm.options, vm.$i18n.locale]),
                this.debouncedLoad,
                {deep: true, immediate: true}
            );
            this.$watch(
                (vm) => ([vm.filterItems, vm.categoryFilter, vm.thesisYearFilter]),
                () => {
                    this.options.page = 1;
                    this.debouncedLoad();
                }
            );

            await this[OPTIONS_ACTIONS.LOAD_OPTIONS]();
            await this[PERMS_ACTIONS.LOAD_PERMS]();
        }
    });
</script>
