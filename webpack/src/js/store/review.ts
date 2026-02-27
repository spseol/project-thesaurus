import * as _ from 'lodash-es';
import Axios from '../axios';
import {THESIS_MUTATIONS} from './thesis';

export enum REVIEW_MUTATIONS {

}

export enum REVIEW_ACTIONS {
    LOAD_REVIEWS = 'Load reviews',
}

const state = {};
type State = typeof state;

export default {
    namespaced: true,
    state: state as State,

    mutations: {},
    actions: {
        async [REVIEW_ACTIONS.LOAD_REVIEWS]({commit, dispatch, rootState}, thesis_id) {
            return Axios.get(
                `/api/v1/thesis/${thesis_id}/reviews`
            ).then(r => {
                if (r.status == 200) {
                    const oldThesis = _.find(rootState.thesis.theses.results, {id: thesis_id});
                    const thesis = {
                        ...oldThesis,
                        reviews: r.data
                    };
                    commit('thesis/' + THESIS_MUTATIONS.UPDATE_THESIS, thesis, {root: true});
                }
                return r.data;
            });
        }
    }
};