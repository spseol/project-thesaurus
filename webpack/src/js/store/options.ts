import Axios from '../axios';

export enum OPTIONS_MUTATIONS {
    SET = 'Set',
    INITIALIZED = 'Initialized',
    SET_LOAD_REQUEST = 'Set load request'
}

export enum OPTIONS_ACTIONS {
    LOAD_OPTIONS = 'Load options',
    LOAD_TEACHER = 'Load teacher',
}

const state = {
    category: [],
    teacher: [],
    userFilter: [],
    thesisYear: [],
    thesisState: [],
    typeAttachment: [],

    initialized: null,
    loadRequest: null
};
type State = typeof state;


export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [OPTIONS_MUTATIONS.SET](state: State, f) {
            f(state);
        },
        [OPTIONS_MUTATIONS.INITIALIZED](state: State) {
            state.initialized = true;
        },
        [OPTIONS_MUTATIONS.SET_LOAD_REQUEST](state: State, request) {
            state.loadRequest = request;
        }
    },
    actions: {
        async [OPTIONS_ACTIONS.LOAD_OPTIONS]({state: State, commit}) {
            if (state.initialized) return;
            if (state.loadRequest) return state.loadRequest;

            commit(
                OPTIONS_MUTATIONS.SET_LOAD_REQUEST,
                Promise.all([
                    Axios.get('/api/v1/user-filter-options').then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.userFilter = r.data)
                    ),
                    Axios.get('/api/v1/category-options').then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.category = r.data)
                    ),
                    Axios.get('/api/v1/thesis-year-options').then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.thesisYear = r.data)
                    ),
                    Axios.get('/api/v1/thesis-state-options').then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.thesisState = r.data)
                    ),
                    Axios.get('/api/v1/type-attachment').then(
                        r => commit(OPTIONS_MUTATIONS.SET, s => s.typeAttachment = r.data)
                    )
                ]).then(r => {
                    commit(OPTIONS_MUTATIONS.INITIALIZED);
                })
            );
            return state.loadRequest;
        },
        async [OPTIONS_ACTIONS.LOAD_TEACHER]({commit}) {
            return await Axios.get('/api/v1/teacher-options').then(
                r => commit(OPTIONS_MUTATIONS.SET, s => s.teacher = r.data)
            );
        }
    }
};