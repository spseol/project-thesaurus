import * as _ from 'lodash-es';
import qs from 'qs';
import Vue from 'vue';
import Axios from '../axios';
import {formatDataTableOrdering} from '../utils';
import {THESIS_ACTIONS} from './thesis';

export enum RESERVATION_MUTATIONS {
    SET_RESERVATION_LIST_RESPONSE = 'Set reservation list response',
    STORE_RESERVATION = 'Store reservation',
    NEW_RESERVATION = 'New reservation',
}

export enum RESERVATION_ACTIONS {
    CREATE_RESERVATION = 'Create reservation',
    LOAD_RESERVATIONS = 'Load reservations',
    CANCEL_RESERVATION = 'Cancel reservation',
    EDIT_RESERVATION = 'Edit reservation',
}

const state = {
    reservations: {results: [], count: 0}
};
type State = typeof state;

export default {
    namespaced: true,
    state: state as State,

    mutations: {
        [RESERVATION_MUTATIONS.SET_RESERVATION_LIST_RESPONSE](state: State, response) {
            Vue.set(state.reservations, 'results', response.results);
            Vue.set(state.reservations, 'count', response.count);
        },
        [RESERVATION_MUTATIONS.STORE_RESERVATION](state: State, reservation) {
            Vue.set(
                state.reservations.results,
                _.findIndex(state.reservations.results, {id: reservation.id}),
                reservation
            );
        },
        [RESERVATION_MUTATIONS.NEW_RESERVATION](state: State, reservation) {
            Vue.set(
                state.reservations,
                'results',
                [reservation, ...state.reservations.results]
            );
            state.reservations.count += 1;
        }
    },
    actions: {
        async [RESERVATION_ACTIONS.LOAD_RESERVATIONS]({commit}, {state, search, options, headers} = {
            options: {page: 1, sortBy: [], sortDesc: []},
            state: '',
            search: '',
            headers: []
        }) {
            this.$asyncStart(RESERVATION_ACTIONS.LOAD_RESERVATIONS);
            const {page = 1} = options;
            const ordering = formatDataTableOrdering(options, headers);

            return Axios.get(
                `/api/v1/reservation?${qs.stringify({state, search, ordering, page})}`
            ).then(r => {
                if (r.status == 200)
                    commit(RESERVATION_MUTATIONS.SET_RESERVATION_LIST_RESPONSE, r.data);

                this.$asyncEnd(RESERVATION_ACTIONS.LOAD_RESERVATIONS);
                return r.data;
            });
        },

        async [RESERVATION_ACTIONS.CREATE_RESERVATION]({commit, dispatch}, {thesis_id}) {
            return Axios.post(
                `/api/v1/reservation`,
                {thesis_id}
            ).then(r => {
                if (r.status == 201) {
                    commit(RESERVATION_MUTATIONS.NEW_RESERVATION, r.data);
                    dispatch('thesis/' + THESIS_ACTIONS.RELOAD_THESIS, r.data.thesis_id, {root: true});
                }
                return r.data;
            });
        },
        async [RESERVATION_ACTIONS.CANCEL_RESERVATION]({commit, dispatch}, {reservation_id}) {
            return Axios.patch(
                `/api/v1/reservation/${reservation_id}/cancel`
            ).then(r => {
                if (r.status == 200) {
                    commit(RESERVATION_MUTATIONS.STORE_RESERVATION, r.data);
                    dispatch('thesis/' + THESIS_ACTIONS.RELOAD_THESIS, r.data.thesis_id, {root: true});
                }
                return r.data;
            });
        },
        async [RESERVATION_ACTIONS.EDIT_RESERVATION]({commit, dispatch}, {reservation_id, data}) {
            return Axios.patch(
                `/api/v1/reservation/${reservation_id}`,
                data
            ).then(r => {
                if (r.data.id) {
                    commit(RESERVATION_MUTATIONS.STORE_RESERVATION, r.data);
                    dispatch('thesis/' + THESIS_ACTIONS.RELOAD_THESIS, r.data.thesis_id, {root: true});
                }
                return r.data;
            });
        }

    },
    getters: {
        orderedByImportance({state: State}) {
            const inSort = ['ready', 'running', 'created'];
            return _.sortBy(
                _.filter(
                    state.reservations.results,
                    r => inSort.indexOf(r.state) >= 0
                ),
                s => ['ready', 'running', 'created'].indexOf(s.state)
            );
        }
    }
};