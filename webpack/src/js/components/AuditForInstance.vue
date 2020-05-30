<template>
    <v-dialog
        v-model="dialog" v-if="canViewAudit"
        max-width="80em" :fullscreen="$vuetify.breakpoint.smAndDown"
    >
        <template v-slot:activator="{ on }">
            <v-btn fab dark elevation="2" color="orange" v-on="on" class="ma-2" :x-small="small" :small="!small">
                <v-icon :x-small="small" color="black">mdi-timeline-clock-outline</v-icon>
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <v-skeleton-loader type="text" :loading="loading" width="100%">
                    <template v-if="data">
                        <v-icon>mdi-timeline-clock-outline</v-icon>
                        <span class="mx-1">{{ $t('Audit') }}</span> |
                        <span class="font-weight-regular mx-1">{{ data.__model__ }}</span> |
                        <span class="font-weight-bold ml-1">{{ truncateValue(data.__str__) || $t('Unknown') }}</span>
                    </template>
                </v-skeleton-loader>
            </v-card-title>
            <v-card-text>
                <v-progress-linear indeterminate v-if="loading"></v-progress-linear>
                <v-expansion-panels multiple popout focusable v-if="!loading" :value="[0]">
                    <v-expansion-panel
                        v-for="r in [...data.results, ...loaded]"
                        :key="r.id"
                    >
                        <v-expansion-panel-header ripple>
                            <v-row no-gutters justify="space-between">
                                <v-col cols="5">
                                    <v-icon>mdi-clock</v-icon>
                                    {{ dateToRelative(r.timestamp) }}
                                    <span class="caption grey--text">({{ (new Date(r.timestamp)).toLocaleString($i18n.locale) }})</span>
                                </v-col>
                                <v-col cols="3" :title="r.action_label">
                                    <v-icon>{{ actionToIcon(r.action) }}</v-icon>
                                    {{ r.__str__ }}

                                    <span class="caption grey--text">
                                        {{ actionSubtitle(r) }}
                                    </span>
                                </v-col>
                                <v-col cols="4">
                                    <v-icon>mdi-account-box</v-icon>
                                    {{ r.user ? r.user.full_name : '-' }}
                                </v-col>
                            </v-row>
                        </v-expansion-panel-header>

                        <v-expansion-panel-content>
                            <v-simple-table v-if="r.row_data" dense>
                                <thead>
                                <tr>
                                    <th class="text-right">{{ $t('Attribute') }}</th>
                                    <th>{{ $t('Before event') }}</th>
                                    <th>{{ $t('After event') }}</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr
                                    v-for="(column_old_value, column_name) of r.row_data" :key="column_name"
                                    :class="{'orange accent-1': column_name in (r.changed_fields || {})}"
                                >
                                    <td class="py-1 col-1 text-right">
                                        <code>{{ tableColumnToLabel(r.__table__, column_name) }}</code>
                                    </td>

                                    <td class="py-1 col-3" v-for="value in [column_old_value || '', (r.changed_fields || {})[column_name] || '']">

                                        <!-- boolean, show checkboxes -->
                                        <template v-if="['t', 'f'].includes(value)">
                                            <v-icon small :color="booleanToConf(value).color">
                                                {{ booleanToConf(value).icon }}
                                            </v-icon>
                                        </template>

                                        <!-- text, show truncated and in tooltip -->
                                        <template v-else-if="value.length > 50">
                                            <v-tooltip top max-width="70vw">
                                                <template v-slot:activator="{ on }">
                                                    <span v-on="on">
                                                        {{ truncateValue(value) }}
                                                    </span>
                                                </template>
                                                {{ value }}
                                            </v-tooltip>
                                        </template>

                                        <!-- otherwise try to format by state.choices -->
                                        <template v-else>
                                            {{ filterValue(r.__table__, column_name, value) }}

                                            <!-- show recursively if -->
                                            <!-- actually has some value -->
                                            <!-- not reference to self -->
                                            <!-- known mapping column to model -->
                                            <!-- no ignored -->
                                            <audit-for-instance
                                                v-if="value && value !== modelPk && mappings.foreign_key_to_model[column_name] && !pksToIgnore.includes(value)"
                                                :model-name="mappings.foreign_key_to_model[column_name]"
                                                :model-pk="value" small
                                                :pks-to-ignore="pksToIgnore.concat(modelPk)"
                                                :mappings-cache="mappings"
                                            ></audit-for-instance>
                                        </template>
                                    </td>
                                </tr>
                                </tbody>
                            </v-simple-table>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>

                <v-row justify="center" v-if="next && !loading" class="mt-3">
                    <v-btn large color="blue" dark @click="loadNext">{{ $t('Load older logs') }}</v-btn>
                </v-row>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import moment from 'moment';
    import Axios from '../axios';
    import {hasPerm} from '../user';
    import {getAuditMappings} from '../utils';

    export default {
        name: 'AuditForInstance',
        props: {
            modelPk: {
                type: String
            },
            modelName: {
                type: String
            },
            small: {
                type: Boolean
            },
            pksToIgnore: {
                type: Array,
                default: () => []
            },
            mappingsCache: {
                type: Object,
                default: null
            }
        },
        data() {
            return {
                dialog: false,
                canViewAudit: false,
                loaded: [],
                next: null
            };
        },
        asyncComputed: {
            data: {
                async get() {
                    if (!await hasPerm('audit.view_auditlog')) return {results: []};
                    if (!this.dialog) return {results: []};

                    const data = (await Axios.get(`/api/v1/audit-log/for-instance/${this.modelName}/${this.modelPk}`)).data;
                    this.next = data.next;
                    return data;
                },
                watch: ['$i18n.locale']
            },
            mappings: {
                async get() {
                    if (this.mappingsCache) return this.mappingsCache;
                    if (!(await hasPerm('audit.view_auditlog')))
                        return {
                            foreign_key_to_model: {},
                            table_columns_to_labels: {},
                            table_columns_to_choices: {}
                        };

                    return getAuditMappings();
                }
            }
        },
        computed: {
            loading() {
                return this.$asyncComputed.data.updating || this.$asyncComputed.mappings.updating;
            }
        },
        watch: {
            dialog(new_) {
                new_ && this.$asyncComputed.data.update();
            }
        },
        methods: {
            actionToIcon(action) {
                return {
                    'I': 'mdi-database-plus',
                    'U': 'mdi-database-edit',
                    'D': 'mdi-delete',
                    'T': 'mdi-database-remove'
                }[action];
            },
            booleanToConf(b) {
                return {
                    t: {icon: 'mdi-checkbox-marked-outline', color: 'green'},
                    f: {icon: 'mdi-checkbox-blank-outline', color: 'red'}
                }[b];
            },
            truncateValue(v) {
                return _.truncate(v, {length: 80});
            },
            tableColumnToLabel(table, column) {
                return (this.mappings.table_columns_to_labels[table] || {})[column]?.toLowerCase();
            },
            filterValue(table, column, value) {
                return ((this.mappings.table_columns_to_choices[table] || {})[column] || {})[value] || value || '---';
            },
            dateToRelative(date) {
                return moment(date, null, this.$i18n.locale).fromNow();
            },
            actionSubtitle(row) {
                return _.truncate(
                    _.keys(
                        row.changed_fields || {}
                    ).map(
                        k => this.tableColumnToLabel(row.__table__, k)
                    ).join(','),
                    {length: 30}
                );
            },
            async loadNext() {
                const data = (await Axios.get(this.next)).data;
                this.loaded.push(...data.results);
                this.next = data.next;
            }
        },
        async created() {
            this.canViewAudit = await hasPerm('audit.view_auditlog');
        }
    };
</script>

<style scoped>

</style>