import _ from 'lodash';
import {Commit} from 'vuex';
import Axios from '../axios';
import {Category, TypeAttachment, UserOption} from '../types';

export enum OPTIONS_MUTATIONS {
    SET = 'Set',
    INITIALIZED = 'Initialized',
    SET_LOAD_REQUEST = 'Set load request'
}

export enum OPTIONS_ACTIONS {
    LOAD_OPTIONS = 'Load options',
    RELOAD_OPTIONS = 'Reload options',
}

class State {
    category: Category[] = [];
    teacher: UserOption[] = [];
    userFilter: UserOption[] = [];
    thesisYear: { text: string, value: string }[] = [];
    thesisState: { text: string, value: string }[] = [];
    reservationState: { text: string, value: string }[] = [];
    typeAttachment: TypeAttachment[] = [];

    initialized: boolean = null;
    loadRequest: boolean = null;
}


export default {
    namespaced: true,
    state: new State,
    mutations: {
        [OPTIONS_MUTATIONS.SET](state: State, f: (State) => any) {
            f(state);
        },
        [OPTIONS_MUTATIONS.INITIALIZED](state: State, _initialized = true) {
            state.initialized = _initialized;
        },
        [OPTIONS_MUTATIONS.SET_LOAD_REQUEST](state: State, request) {
            state.loadRequest = request;
        }
    },
    actions: {
        async [OPTIONS_ACTIONS.RELOAD_OPTIONS]({dispatch, commit}) {
            commit(OPTIONS_MUTATIONS.SET_LOAD_REQUEST, null);
            commit(OPTIONS_MUTATIONS.INITIALIZED, false);

            return dispatch(OPTIONS_ACTIONS.LOAD_OPTIONS);
        },
        async [OPTIONS_ACTIONS.LOAD_OPTIONS]({state, commit}: { state: State, commit: Commit }) {
            if (state.initialized) return;
            if (state.loadRequest) return state.loadRequest;

            commit(
                OPTIONS_MUTATIONS.SET_LOAD_REQUEST,
                Promise.all([
                    Axios.get('/api/v1/user-filter-options', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.userFilter = r.data)
                    ),
                    Axios.get('/api/v1/category-options', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.category = r.data)
                    ),
                    Axios.get('/api/v1/thesis-year-options', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.thesisYear = r.data)
                    ),
                    Axios.get('/api/v1/thesis-state-options', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.thesisState = r.data)
                    ),
                    Axios.get('/api/v1/reservation-state-options', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.reservationState = r.data)
                    ),
                    Axios.get('/api/v1/type-attachment', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.typeAttachment = r.data)
                    ),
                    Axios.get('/api/v1/teacher-options', {allow403: true}).then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.teacher = r.data)
                    )
                ]).then(r => {
                    commit(OPTIONS_MUTATIONS.INITIALIZED);
                })
            );
            return state.loadRequest;
        }
    },
    getters: {
        typeAttachmentAcceptTypes: (state: State) =>
            (identifier): string =>
                _.find<TypeAttachment>(
                    state.typeAttachment,
                    {identifier}
                )?.allowed_content_types.join(',')
    }
};