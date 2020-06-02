import _ from 'lodash';
import Vue from 'vue';
import Axios from '../axios';

export enum AUDIT_MUTATIONS {
    STORE_AUDIT_FOR_INSTANCE = 'Store audit for instance',
    APPEND_AUDIT_FOR_INSTANCE = 'Append audit for instance',
    STORE_MAPPINGS = 'Store mappings',
}

export enum AUDIT_ACTIONS {
    LOAD_AUDIT_FOR_INSTANCE = 'Load audit for instance',
    LOAD_MAPPINGS = 'Load audit mappings',
    LOAD_AUDIT_NEXT = 'Load audit next',
}

const state = {
    audit: {},
    mappings: null
};
type State = typeof state;

export default {
    namespaced: true,
    state: state as State,

    mutations: {
        [AUDIT_MUTATIONS.STORE_AUDIT_FOR_INSTANCE](state, {model, pk, data}) {
            Vue.set(
                state.audit,
                model,
                state.audit[model] || {}
            );
            Vue.set(
                state.audit[model],
                pk,
                data
            );
        },
        [AUDIT_MUTATIONS.APPEND_AUDIT_FOR_INSTANCE](state, {model, pk, data}) {
            const newRecord = {
                ...data,
                results: [...state.audit[model][pk].results, ...data.results]
            };
            Vue.set(
                state.audit[model],
                pk,
                newRecord
            );
        },
        [AUDIT_MUTATIONS.STORE_MAPPINGS](state, mappings) {
            Vue.set(state, 'mappings', mappings);
        }
    },
    actions: {
        async [AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE]({commit, dispatch, state}, {model, pk}) {
            if (state.audit[model] && state.audit[model][pk]) return state.audit[model][pk];

            return Axios.get(
                `/api/v1/audit/for-instance/${model}/${pk}`
            ).then(r => {
                if (r.status == 200) {
                    commit(
                        AUDIT_MUTATIONS.STORE_AUDIT_FOR_INSTANCE,
                        {model, pk, data: r.data}
                    );
                }
                return r.data;
            });
        },
        async [AUDIT_ACTIONS.LOAD_AUDIT_NEXT]({commit, dispatch, state}, {model, pk}) {
            const url = state.audit[model][pk]?.next;

            if (!url) return dispatch(AUDIT_ACTIONS.LOAD_AUDIT_FOR_INSTANCE, {model, pk});

            return Axios.get(url).then(r => {
                if (r.status == 200) {
                    commit(
                        AUDIT_MUTATIONS.APPEND_AUDIT_FOR_INSTANCE,
                        {model, pk, data: r.data}
                    );
                    return state.audit[model][pk];
                }
                return r.data;
            });
        },
        async [AUDIT_ACTIONS.LOAD_MAPPINGS]({commit, state}) {
            if (state.mappings) return state.mappings;

            commit(
                AUDIT_MUTATIONS.STORE_MAPPINGS,
                Axios.get('/api/v1/audit/mappings').then(r => {
                    if (r.status == 200)
                        commit(AUDIT_MUTATIONS.STORE_MAPPINGS, r.data);

                    return r.data;
                })
            );
            return state.mappings;
        }
    },
    getters: {
        auditLogsForModel: (state) =>
            (model, pk) =>
                (state.audit[model] || {})[pk] || {results: []},

        filterDisplayValue: (state) =>
            (table, column, value) => (
                (state.mappings.table_columns_to_choices[table] || {})[column] || {})[value]
                || state.mappings.primary_keys_to_labels[value]
                || value
                || '---',

        tableColumnToLabel: (state) => (table, column) =>
            (state.mappings.table_columns_to_labels[table] || {})[column]?.toLowerCase(),

        actionSubtitle: (state, getters) => (row) => _.truncate(
            _.keys(
                row.changed_fields || {}
            ).map(
                k => getters.tableColumnToLabel(row.__table__, k)
            ).join(','),
            {length: 30}
        )


    }
};