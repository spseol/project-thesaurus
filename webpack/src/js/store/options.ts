import Axios from '../axios';

export enum OPTIONS_MUTATIONS {
    SET = 'Set'
}

export enum OPTIONS_ACTIONS {
    LOAD_OPTIONS = 'Load options',
    LOAD_TEACHER = 'Load teacher',
}

const state = {
    userFilter: [],
    category: [],
    thesisYear: [],
    teacher: [],

    loadRequest: null
};
type State = typeof state;


export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [OPTIONS_MUTATIONS.SET](state: State, f) {
            f(state);
        }
    },
    actions: {
        async [OPTIONS_ACTIONS.LOAD_OPTIONS]({commit}) {
            return await Promise.all([
                Axios.get('/api/v1/user-filter-options').then(
                    r => commit(OPTIONS_MUTATIONS.SET, s => s.userFilter = r.data)
                ),
                Axios.get('/api/v1/category-options').then(
                    r => commit(OPTIONS_MUTATIONS.SET, s => s.category = r.data)
                ),
                Axios.get('/api/v1/thesis-year-options').then(
                    r => commit(OPTIONS_MUTATIONS.SET, s => s.thesisYear = r.data)
                )
            ]);
        },
        async [OPTIONS_ACTIONS.LOAD_TEACHER]({commit}) {
            return await Axios.get('/api/v1/teacher-options').then(
                r => commit(OPTIONS_MUTATIONS.SET, s => s.teacher = r.data)
            );
        }
    }
};