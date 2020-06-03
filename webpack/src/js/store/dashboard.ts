import _ from 'lodash';
import Axios from '../axios';

export enum DASHBOARD_MUTATIONS {
    STORE_DASHBOARD = 'Store dashboard',
}

export enum DASHBOARD_ACTIONS {
    LOAD_DASHBOARD = 'Load dashboard',
}

const state = {
    theses_ready_for_review: [],
    reservations_ready_for_prepare: [],
    theses_just_submitted: [],
    author_theses: []
};
type State = typeof state;


export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [DASHBOARD_MUTATIONS.STORE_DASHBOARD](state: State, data) {
            Object.assign(state, data);
        }
    },
    actions: {
        async [DASHBOARD_ACTIONS.LOAD_DASHBOARD]({commit}) {
            this.$asyncStart(DASHBOARD_ACTIONS.LOAD_DASHBOARD);
            return Axios.get('/api/v1/dashboard').then(r => {
                if (r.status == 200) {
                    this.$asyncEnd(DASHBOARD_ACTIONS.LOAD_DASHBOARD);
                    commit(DASHBOARD_MUTATIONS.STORE_DASHBOARD, r.data);
                } else {
                    this.$asyncFail(DASHBOARD_ACTIONS.LOAD_DASHBOARD);
                }
            });
        }
    },
    getters: {
        reservedThesesRegistrationNumbers: (state) => _.map(
            state.reservations_ready_for_prepare,
            _.property('thesis_registration_number')
        ).sort(),

        hasData: (state) => (
            state.theses_ready_for_review.length &&
            state.reservations_ready_for_prepare.length &&
            state.theses_just_submitted.length &&
            state.author_theses.length
        )
    }
};