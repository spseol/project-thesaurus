<template>
    <v-dialog
        v-model="dialog" v-if="canViewAudit"
        max-width="80em" :fullscreen="$vuetify.breakpoint.smAndDown"
    >
        <template v-slot:activator="{ on }">
            <v-btn fab dark elevation="2" color="primary" v-on="on" class="ma-2" :x-small="small" :small="!small">
                <v-icon :small="small">mdi-clock-outline</v-icon>
            </v-btn>
        </template>

        <v-card>
            <v-card-title>
                <v-skeleton-loader type="text" :loading="!$calls.isDone(call(AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE))" width="100%">
                    <template v-if="logs">
                        <v-icon>mdi-timeline-clock-outline</v-icon>
                        <span class="mx-1">{{ $t('Audit') }}</span> |
                        <span class="font-weight-regular mx-1">{{ logs.__model__ }}</span> |
                        <span class="font-weight-bold ml-1">{{ truncateValue(logs.__str__) || $t('Unknown') }}</span>
                    </template>
                </v-skeleton-loader>
            </v-card-title>
            <v-card-text>
                <v-progress-linear
                    indeterminate
                    v-if="$calls.isPending(call(AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE)) || $calls.isPending(AUDIT_ACTIONS.LOAD_MAPPINGS)"
                >
                </v-progress-linear>

                <v-scale-transition>
                    <v-expansion-panels
                        v-if="$calls.isDone(call(AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE)) && $calls.isDone(AUDIT_ACTIONS.LOAD_MAPPINGS)"
                        v-model="openedPanels" multiple popout focusable
                    >
                        <v-expansion-panel
                            v-for="r in logs.results"
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
                                        v-for="[column_name, column_old_value, column_label] in sortRowData(r)"
                                        :key="column_name"
                                        :class="{'orange accent-1': column_name in (r.changed_fields || {})}"
                                    >
                                        <td class="py-1 col-1 text-right">
                                            <v-tooltip
                                                :disabled="!tableColumnToHelpText(r.__table__, column_name)"
                                                icon="mdi-info" bottom
                                            >
                                                <template v-slot:activator="{ on }">
                                                    <code
                                                        v-on="on" v-text="column_label"
                                                    ></code>
                                                </template>

                                                {{ tableColumnToHelpText(r.__table__, column_name) }}
                                            </v-tooltip>
                                        </td>

                                        <td
                                            v-for="value in [column_old_value || '', (r.changed_fields || {})[column_name] || '']"
                                            class="py-1 col-3"
                                        >
                                            <!-- boolean, show checkboxes -->
                                            <template v-if="['t', 'f'].includes(value)">
                                                <v-icon small :color="booleanToConf(value).color">
                                                    {{ booleanToConf(value).icon }}
                                                </v-icon>
                                            </template>

                                            <!-- long text, show truncated and tooltip -->
                                            <template v-else-if="value.length > 50">
                                                <v-tooltip top max-width="70vw">
                                                    <template v-slot:activator="{ on }">
                                                    <span v-on="on">
                                                        {{ truncateValue(value) }}
                                                    </span>
                                                    </template>
                                                    '{{ value }}'
                                                </v-tooltip>
                                            </template>

                                            <!-- otherwise filter by function -->
                                            <template v-else>
                                                {{ filterDisplayValue(r.__table__, column_name, value) }}

                                                <!-- maybe has own audit logs, display in following conditions -->
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
                                                ></audit-for-instance>

                                                <!-- object recursion -->
                                                <v-icon small v-if="pksToIgnore.includes(value) || value === modelPk">
                                                    mdi-rotate-left
                                                </v-icon>
                                            </template>
                                        </td>
                                    </tr>
                                    </tbody>
                                </v-simple-table>
                            </v-expansion-panel-content>
                        </v-expansion-panel>
                    </v-expansion-panels>
                </v-scale-transition>

                <v-row justify="center" v-if="next" class="mt-3">
                    <v-btn
                        large color="blue" dark @click="loadNext"
                        :loading="$calls.isPending(AUDIT_ACTIONS.LOAD_AUDIT_NEXT)"
                    >
                        {{ $t('Load older logs') }}
                    </v-btn>
                </v-row>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script type="text/tsx">
    import _ from 'lodash-es';
    import moment from 'moment';
    import {AUDIT_ACTIONS, callIdentifier} from '../store/audit';
    import {auditStore} from '../store/store';
    import {hasPerm} from '../user';

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
                next: null,
                openedPanels: [0],
                AUDIT_ACTIONS
            };
        },
        computed: {
            ...auditStore.mapGetters([
                'filterDisplayValue',
                'tableColumnToLabel',
                'tableColumnToHelpText',
                'actionSubtitle',
                'auditLogsForModel'
            ]),
            ...auditStore.mapState(['mappings']),
            logs() {
                return this.auditLogsForModel(this.modelName, this.modelPk);
            }
        },
        watch: {
            dialog(new_) {
                new_ && this[AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE]({model: this.modelName, pk: this.modelPk});
            }
        },
        methods: {
            ...auditStore.mapActions([
                AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE,
                AUDIT_ACTIONS.LOAD_MAPPINGS,
                AUDIT_ACTIONS.LOAD_AUDIT_NEXT
            ]),
            call(identifier) {
                return callIdentifier(identifier, this.modelName, this.modelPk);
            },
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
            dateToRelative(date) {
                return moment(date, null, this.$i18n.locale).fromNow();
            },
            sortRowData(row) {
                return _.sortBy(
                    _.toPairs(
                        row.row_data
                    ).map(
                        ([key, value]) => [key, value, this.tableColumnToLabel(row.__table__, key)]
                    ),
                    _.property('2.length')
                );
            },

            async loadNext() {
                const {
                    next,
                    results
                } = await this[AUDIT_ACTIONS.LOAD_AUDIT_NEXT]({model: this.modelName, pk: this.modelPk});

                this.loaded.push(...results);
                this.next = next;
            }
        },
        async created() {
            this.canViewAudit = await hasPerm('audit.view_auditlog');

            await this[AUDIT_ACTIONS.LOAD_MAPPINGS]();
        }
    };
</script>

<style scoped>

</style>