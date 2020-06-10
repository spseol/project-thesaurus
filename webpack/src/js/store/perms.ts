import _ from 'lodash';
import Vue from 'vue';
import {hasPerm} from '../user';

export enum PERMS_MUTATIONS {
    SET_PERM = 'Set perm',
    INITIALIZED = 'Initialized',
    SET_LOAD_REQUEST = 'Load request',
}

export enum PERMS_ACTIONS {
    LOAD_PERMS = '📡Load options'
}

export enum PERMS {
    VIEW_AUDIT = 'audit_view_auditlog',
    CHANGE_THESIS = 'thesis_change_thesis',
    VIEW_USER = 'accounts_view_user',
    CHANGE_RESERVATION = 'thesis_change_reservation',
    ADD_THESIS = 'thesis_add_thesis',
}

const state = {
    perms: {},
    initialized: false,

    loadRequest: null
};
type State = typeof state;

export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [PERMS_MUTATIONS.SET_PERM](state: State, {perm, value}) {
            Vue.set(state.perms, perm, value);
        },
        [PERMS_MUTATIONS.INITIALIZED](state: State) {
            state.initialized = true;
        },
        [PERMS_MUTATIONS.SET_LOAD_REQUEST](state: State, request: Promise<any>) {
            state.loadRequest = request;
        }
    },
    actions: {
        async [PERMS_ACTIONS.LOAD_PERMS]({commit, state: State}) {
            if (state.initialized) return;
            if (state.loadRequest) return state.loadRequest;

            commit(
                PERMS_MUTATIONS.SET_LOAD_REQUEST,
                Promise.all(
                    _.values(PERMS).map(
                        perm => hasPerm(
                            // only the first occurrence of _
                            perm.replace('_', '.')
                        ).then(
                            value => commit(PERMS_MUTATIONS.SET_PERM, {perm, value})
                        )
                    )
                ).then(r => {
                    commit(PERMS_MUTATIONS.INITIALIZED);
                })
            );
            return state.loadRequest;
        }
    }
};