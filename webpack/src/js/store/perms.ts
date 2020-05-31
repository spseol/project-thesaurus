import _ from 'lodash';
import Vue from 'vue';
import {hasPerm} from '../user';

export enum PERMS_MUTATIONS {
    SET_PERM = 'Set perm'
}

export enum PERMS_ACTIONS {
    LOAD_PERMS = '📡Load options'
}

export enum PERMS {
    VIEW_AUDIT = 'audit_view_auditlog',
    CHANGE_THESIS = 'thesis_change_thesis',
    VIEW_USER = 'accounts_view_user',
}

const state = {
    perms: {}
};
type State = typeof state;

export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [PERMS_MUTATIONS.SET_PERM](state: State, {perm, value}) {
            Vue.set(state.perms, perm, value);
        }
    },
    actions: {
        async [PERMS_ACTIONS.LOAD_PERMS]({commit}) {
            return await Promise.all(
                _.values(PERMS).map(
                    perm => hasPerm(perm.split('_', 1).join('.')
                    ).then(
                        value => commit(PERMS_MUTATIONS.SET_PERM, {perm, value})
                    )
                )
            );
        }
    }
};