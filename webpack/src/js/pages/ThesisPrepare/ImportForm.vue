<template>
    <v-card :loading="loading">
        <v-card-title>{{ $t('Bulk theses import') }}</v-card-title>
        <v-card-text>
            <v-form @submit.prevent="submit" v-model="valid">
                <v-alert color="blue" text>
                    <v-row no-gutters>
                        <v-col cols="6">
                            <h3 class="headline">{{ $t('File format') }}</h3>
                            <v-list>
                                <v-subheader>{{ $t('thesis.import.preferredType') }}</v-subheader>
                                <v-list-item>
                                    <v-list-item-icon>
                                        <v-icon>mdi-file-excel</v-icon>
                                    </v-list-item-icon>
                                    <v-list-item-content>
                                        <v-list-item-title>
                                            {{ $t('Excel file') }}
                                        </v-list-item-title>
                                        <v-list-item-subtitle>
                                            {{ $t('thesis.import.ExcelFormatDescription') }}
                                        </v-list-item-subtitle>
                                        <v-list-item-action-text>
                                            <v-btn
                                                :href="columns.file_examples.xlsx" v-if="columns.file_examples.xlsx"
                                                text small outlined class="mt-1"
                                            >
                                                <v-icon small>mdi-download</v-icon>
                                                {{ $t('thesis.import.downloadExampleExcelFile') }}
                                            </v-btn>
                                        </v-list-item-action-text>
                                    </v-list-item-content>
                                </v-list-item>
                                <v-subheader>{{ $t('thesis.import.possibleType') }}</v-subheader>
                                <v-list-item>
                                    <v-list-item-icon>
                                        <v-icon>mdi-file</v-icon>
                                    </v-list-item-icon>
                                    <v-list-item-content>
                                        <v-list-item-title>
                                            {{ $t('CSV file') }}
                                        </v-list-item-title>
                                        <v-list-item-subtitle>
                                            {{ $t('thesis.import.CSVFormatDescription') }}
                                        </v-list-item-subtitle>
                                        <v-list-item-action-text>
                                            <v-btn
                                                :href="columns.file_examples.csv" v-if="columns.file_examples.csv"
                                                text small outlined class="mt-1"
                                            >
                                                <v-icon small>mdi-download</v-icon>
                                                {{ $t('thesis.import.downloadExampleCSVFile') }}
                                            </v-btn>
                                        </v-list-item-action-text>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-col>
                        <v-col cols="6">
                            <h3 class="headline">{{ $t('Columns') }}</h3>
                            <v-list>
                                <v-list-item v-for="col in columns.columns" :key="col.title">
                                    <v-list-item-icon>
                                        <v-icon>mdi-{{ col.icon }}</v-icon>
                                    </v-list-item-icon>
                                    <v-list-item-content>
                                        <v-list-item-title v-text="col.title"></v-list-item-title>
                                        <v-list-item-subtitle v-text="col.description"></v-list-item-subtitle>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-col>
                    </v-row>
                    <v-progress-linear indeterminate v-if="$asyncComputed.columns.updating"></v-progress-linear>
                </v-alert>
                <v-text-field
                    v-model="published_at"
                    :counter="7"
                    :rules="[v => !!v, v => /\d{4}\/\d{2}/.test(v) || $t('thesis.publishedAtNotInFormat')]"
                    :label="$t('Published at')" prepend-icon="mdi-calendar"
                    required
                ></v-text-field>

                <v-file-input
                    :label="$t('File to import')" v-model="file"
                    accept="text/csv,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ></v-file-input>

                <v-row no-gutters>
                    <v-spacer></v-spacer>
                    <v-btn type="submit" color="success" :loading="loading" :disabled="!valid || !published_at || !file">
                        {{ $t('thesis.import.loadAndCheck') }}
                    </v-btn>
                </v-row>
            </v-form>
        </v-card-text>

        <v-dialog v-model="importDialog">
            <v-card>
                <v-card-text>
                    <v-simple-table fixed-header height="60vh">
                        <thead>
                        <tr>
                            <th>#</th>
                            <th v-for="col in columns.columns">{{ col.title }}</th>
                            <th>{{ $t('Status') }}</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr
                            v-for="(tr, i) in data.statuses"
                            :class="{'red lighten-4': tr.error}"
                        >

                            <td class="text-right">#{{ i + 1 }}</td>
                            <td v-for="td in tr.statuses" :class="{'red lighten-4': td.error}">
                                <v-icon v-if="td.error" color="red" small>mdi-exclamation-thick</v-icon>

                                <span :class="{caption: td.error}">
                                    {{ td.success ? '' : (td.value || '') }}
                                </span>

                                <v-icon v-if="td.success && !tr.error" color="success">mdi-check</v-icon>
                            </td>

                        </tr>
                        </tbody>
                    </v-simple-table>
                    <div class="d-flex mt-3 align-center">
                        <v-spacer></v-spacer>

                        <v-alert color="red" text v-if="data.error">
                            {{ $t('thesis.import.containingErrors') }}
                        </v-alert>

                        <v-alert color="info" text v-if="!data.error && data.statuses" class="mb-0 mr-3">
                            {{ $t('thesis.import.totalTheses') }}:
                            {{ data.statuses.length }}
                        </v-alert>

                        <v-alert color="green" text v-if="!data.error" class="mb-0">
                            <v-checkbox
                                v-if="!data.error"
                                v-model="importAgreement" hide-details
                                :label="$t('thesis.import.importAgreement')"
                                class="mr-3 mt-0 pt-0"
                            ></v-checkbox>
                        </v-alert>
                        <v-btn
                            v-if="!data.error"
                            :disabled="data.error || !importAgreement"
                            @click="submitFinal"
                            class="align-self-center ml-5"
                            type="submit" color="green" large
                        >
                            {{ $t('Final import') }}
                        </v-btn>
                    </div>
                </v-card-text>
            </v-card>
        </v-dialog>
    </v-card>
</template>

<script type="text/tsx">
    import Vue from 'vue';
    import Axios from '../../axios';
    import {asyncComputed, asyncOptions, notificationBus, readFileAsync} from '../../utils';

    export default Vue.extend({
        name: 'ImportForm',
        asyncComputed: {
            categoryOptions: asyncOptions('/api/v1/category-options'),
            columns: asyncComputed('/api/v1/thesis-import/columns', {default: {file_examples: {}, columns: []}})
        },
        data() {
            return {
                loading: false,
                file: null,
                data: {},
                importDialog: false,
                importAgreement: false,
                valid: false,
                published_at: new Date().toISOString().substr(0, 7).replace('-', '/'),
            };
        },
        methods: {
            async submit() {
                this.loading = true;

                const resp = await this.send();
                if (!resp.data.success) {
                    notificationBus.warning(resp.data.message);
                } else {
                    this.importDialog = true;
                    this.data = resp.data;
                }

                this.loading = false;
            },
            async submitFinal() {
                if (this.data.error) {
                    notificationBus.warning(this.$t('Cannot import file with errors'));
                    return;
                }

                this.loading = true;
                const resp = await this.send(true);

                if (resp.data.success) {
                    notificationBus.success(resp.data.message);
                    this.importDialog = false;
                    await this.$router.push(this.$i18nRoute({name: 'thesis-list'}));
                } else {
                    notificationBus.warning(resp.data.message);
                }
                this.data = resp.data;
                this.importAgreement = false;
                this.loading = false;
            },
            async send(final = false) {
                let formData = new FormData();
                await readFileAsync(this.file);
                formData.append('published_at', this.published_at);
                formData.append('import', this.file);
                if (final)
                    formData.append('final', 'true');

                return await Axios.post(`/api/v1/thesis-import`, formData, {
                    headers: {'Content-Type': 'multipart/form-data'}
                });
            }
        }
    });
</script>

<style scoped>

</style>