import _ from 'lodash-es';
import {Commit} from 'vuex';
import Axios from '../axios';
import {Reservation, Thesis} from '../types';

export enum DASHBOARD_MUTATIONS {
    STORE_DASHBOARD = 'Store dashboard',
}

export enum DASHBOARD_ACTIONS {
    LOAD_DASHBOARD = 'Load dashboard',
}

class State {
    theses_ready_for_review: Thesis[] = [];
    theses_just_submitted: Thesis[] = [];
    author_theses: Thesis[] = [];
    reservations_ready_for_prepare: Reservation[] = [];
}

export default {
    namespaced: true,
    state: new State(),
    mutations: {
        [DASHBOARD_MUTATIONS.STORE_DASHBOARD](state: State, data: State) {
            Object.assign(state, data);
        }
    },
    actions: {
        async [DASHBOARD_ACTIONS.LOAD_DASHBOARD]({commit}: { commit: Commit }): Promise<State> {
            this.$asyncStart(DASHBOARD_ACTIONS.LOAD_DASHBOARD);
            return Axios.get('/api/v1/dashboard').then(r => {
                if (r.status == 200) {
                    this.$asyncEnd(DASHBOARD_ACTIONS.LOAD_DASHBOARD);
                    commit(DASHBOARD_MUTATIONS.STORE_DASHBOARD, r.data);

                }
                return r.data;
            });
        }
    },
    getters: {
        reservedThesesRegistrationNumbers: (state: State): Array<string> =>
            _.map<Reservation, string>(
                state.reservations_ready_for_prepare,
                _.property<Reservation, string>('thesis_registration_number')
            ).sort(),

        hasData: (state): boolean => !!(
            state.theses_ready_for_review.length ||
            state.reservations_ready_for_prepare.length ||
            state.theses_just_submitted.length ||
            state.author_theses.length
        )
    }
};