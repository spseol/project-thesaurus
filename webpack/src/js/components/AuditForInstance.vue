<template>
    <v-dialog
        v-model="dialog" v-if="canViewAudit"
        max-width="80vw" max-height="60vh" :fullscreen="$vuetify.breakpoint.smAndDown"
    >
        <template v-slot:activator="{ on }">
            <v-btn fab dark elevation="2" color="orange" v-on="on" class="ma-2" :x-small="small" :small="!small">
                <v-icon :x-small="small" color="black">mdi-timeline-clock-outline</v-icon>
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <v-icon class="mr-2">mdi-timeline-clock-outline</v-icon>
                <span class="mr-2">{{ $t('Audit') }}</span>|
                <span class="font-weight-regular mx-2">{{ data.__model__ }}</span>|
                <span class="font-weight-bold mx-2">{{ data.__str__  || $t('Unknown') }}</span>
            </v-card-title>
            <v-card-text>
                <v-progress-linear indeterminate v-if="$asyncComputed.data.updating || $asyncComputed.mappings.updating"></v-progress-linear>
                <v-expansion-panels popout focusable v-if="$asyncComputed.data.success && $asyncComputed.mappings.success">
                    <v-expansion-panel
                        v-for="row in [...data.results, ...loaded]"
                        :key="row.id"
                    >
                        <v-expansion-panel-header>
                            <v-row no-gutters>
                                <v-col cols="5">
                                    <v-icon>mdi-clock</v-icon>
                                    {{ dateToRelative(row.timestamp) }}
                                    <span class="caption grey--text">({{ (new Date(row.timestamp)).toLocaleString($i18n.locale) }})</span>
                                </v-col>
                                <v-col cols="2">
                                    <v-icon>{{ actionToIcon(row.action) }}</v-icon>
                                    {{ row.__str__ }}
                                </v-col>
                                <v-col cols="4">
                                    <v-icon>mdi-account-box</v-icon>
                                    {{ row.user ? row.user.full_name : '-' }}
                                </v-col>

                            </v-row>
                        </v-expansion-panel-header>

                        <v-expansion-panel-content>
                            <v-simple-table v-if="row.row_data" dense>
                                <thead>
                                <tr>
                                    <th class="text-right">{{ $t('Attribute') }}</th>
                                    <th>{{ $t('Before event') }}</th>
                                    <th>{{ $t('After event') }}</th>
                                </tr>
                                </thead>
                                <tbody>
                                <tr
                                    v-for="(v, column_name) of row.row_data" :key="column_name"
                                    :class="{'orange accent-1': (row.changed_fields || {})[column_name]}"
                                >
                                    <td class="py-1 col-1 text-right">
                                        <code>{{ tableColumnToLabel(row.__table__, column_name) }}</code>
                                    </td>
                                    <td class="py-1 col-3" v-for="v_ in [v || '', (row.changed_fields ? row.changed_fields[column_name] : '') || '']">

                                        <template v-if="['t', 'f'].includes(v_)">
                                            <v-icon small :color="booleanToConf(v_).color">
                                                {{ booleanToConf(v_).icon }}
                                            </v-icon>
                                        </template>

                                        <template v-else-if="v_.length > 50">

                                            <v-tooltip top max-width="70vw">
                                                <template v-slot:activator="{ on }">
                                                    <span v-on="on">
                                                        {{ truncateValue(v_) }}
                                                    </span>
                                                </template>
                                                {{ v_ }}
                                            </v-tooltip>
                                        </template>

                                        <template v-else>
                                            {{ filterValue(row.__table__, column_name, v_) }}
                                            <audit-for-instance
                                                v-if="v_ && v_ !== modelPk && mappings.foreign_key_to_model[column_name] && !pksToIgnore.includes(v_)"
                                                :model-name="mappings.foreign_key_to_model[column_name]"
                                                :model-pk="v_" small
                                                :pks-to-ignore="[...pksToIgnore, modelPk]"
                                            ></audit-for-instance>
                                        </template>
                                    </td>
                                </tr>
                                </tbody>
                            </v-simple-table>
                        </v-expansion-panel-content>
                    </v-expansion-panel>
                </v-expansion-panels>

                <v-row justify="center" v-if="next" class="mt-3">
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
    import {asyncComputed} from '../utils';

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
                    if (!await hasPerm('audit.view_auditlog')) return {};
                    const data = await Axios.get(`/api/v1/audit-log/for-instance/${this.modelName}/${this.modelPk}`).then(r => r.data);
                    this.next = data.next;
                    return data;
                },
                default: {},
                lazy: true,
                watch: ['$i18n.locale']
            },
            mappings: asyncComputed(
                '/api/v1/audit-log/mappings',
                {
                    default: {
                        foreign_key_to_model: {},
                        table_columns_to_labels: {},
                        table_columns_to_choices: {}
                    },
                    perm: 'audit.view_auditlog',
                    lazy: true
                }
            )
        },
        methods: {
            actionToIcon(action) {
                return {
                    'I': 'mdi-database-plus',
                    'U': 'mdi-database-edit',
                    'D': 'mdi-database-minus',
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
                return _.truncate(v, {length: 45});
            },
            tableColumnToLabel(table, column) {
                return (this.mappings.table_columns_to_labels[table] || {})[column].toLowerCase();
            },
            filterValue(table, column, value) {
                return ((this.mappings.table_columns_to_choices[table] || {})[column] || {})[value] || value || '---';
            },
            dateToRelative(date) {
                return moment(date, null, this.$i18n.locale).fromNow();
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