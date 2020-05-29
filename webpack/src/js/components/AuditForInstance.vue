<template>
    <v-dialog v-model="dialog" max-width="80vw" max-height="60vh" :fullscreen="$vuetify.breakpoint.smAndDown">
        <template v-slot:activator="{ on }">
            <v-btn icon color="orange" outlined v-on="on" class="ma-2">
                <v-icon>mdi-history</v-icon>
            </v-btn>
        </template>

        <v-card>
            <v-card-title>{{ $t('History for instance') }} {{ data.__str__ || data.__model__ || $t('Unknown') }}
            </v-card-title>
            <v-card-text>
                <v-progress-linear indeterminate v-if="$asyncComputed.data.updating"></v-progress-linear>
                <v-expansion-panels popout focusable>
                    <v-expansion-panel
                        v-for="row in data.results"
                        :key="row.id"
                    >

                        <v-expansion-panel-header>
                            <v-row no-gutters>
                                <v-col cols="3">
                                    <v-icon>mdi-clock</v-icon>
                                    {{ (new Date(row.timestamp)).toLocaleString() }}
                                </v-col>
                                <v-col cols="2">
                                    <v-icon>{{ actionToIcon(row.action) }}</v-icon>
                                    {{ row.__str__ }}
                                </v-col>
                                <v-col cols="2">
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
                                    v-for="(v, k) of row.row_data" :key="k"
                                    :class="{'orange accent-1': (row.changed_fields || {})[k]}"
                                >
                                    <td class="py-1 col-1 text-right"><code>{{ k }}</code></td>
                                    <td class="py-1 col-3" v-for="v_ in [v || '', (row.changed_fields ? row.changed_fields[k] : '') || '']">
                                        <template v-if="['t', 'f'].includes(v_)">
                                            <v-icon small
                                                :color="{'t': 'green', 'f': 'red'}[v_]"
                                            >{{ {'t': 'mdi-checkbox-marked-outline', 'f':
                                                'mdi-checkbox-blank-outline'}[v_] }}
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
                                        <template v-else>{{ v_ || '---' }}</template>
                                    </td>
                                </tr>
                                </tbody>
                            </v-simple-table>

                        </v-expansion-panel-content>

                    </v-expansion-panel>
                </v-expansion-panels>
            </v-card-text>
        </v-card>
    </v-dialog>
</template>

<script type="text/tsx">
    import _ from 'lodash';
    import Axios from '../axios';

    export default {
        name: 'AuditForInstance',
        props: {
            modelPk: {
                type: String
            },
            modelName: {
                type: String
            }
        },
        data() {
            return {
                dialog: false
            };
        },
        asyncComputed: {
            data: {
                async get() {
                    return Axios.get(`/api/v1/audit-log/for-instance/${this.modelName}/${this.modelPk}`).then(r => r.data);
                },
                default: []
            }
        },
        methods: {
            actionToIcon(action) {
                return {
                    'I': 'mdi-plus-box',
                    'U': 'mdi-pen',
                    'D': 'mdi-trash-can-outline',
                    'T': 'mdi-trash-can-outline'
                }[action];
            },
            truncateValue(v) {
                return _.truncate(v, {length: 45});
            }
        }
    };
</script>

<style scoped>

</style>