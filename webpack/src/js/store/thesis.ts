import * as _ from 'lodash';
import * as qs from 'qs';
import Axios from '../axios';

export enum MUTATIONS {
    SET_THESIS_LIST_RESPONSE = 'Set thesis list response'
}

export enum ACTIONS {
    LOAD_THESES = '📡Load theses'
}

const state = {
    theses: {results: [], count: 0}
};
type State = typeof state;


export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [MUTATIONS.SET_THESIS_LIST_RESPONSE](state: State, response) {
            state.theses.results = response.results;
            state.theses.count = response.count;
        }
    },
    actions: {
        async [ACTIONS.LOAD_THESES](store, {options, filters, headers}) {
            const {page, sortBy, sortDesc} = options;
            let header;
            const remap = (value) => ((header = _.find(headers, {value})) && header.mapped) ? header.mapped : value.replace('.', '__');
            const query = qs.stringify({
                page,
                search: _.map(filters, (i) => i.username || i.id || i).join(' '),
                ordering: _.map(
                    _.zip(sortBy, sortDesc),
                    ([col, desc]) => `${desc ? '-' : ''}${remap(col).split('.')[0]}`
                ).join(',')
            });

            const response = (await Axios.get(`/api/v1/thesis?${query}`)).data;


            store.commit(MUTATIONS.SET_THESIS_LIST_RESPONSE, response);

        }
    }
};