import * as _ from 'lodash-es';
import * as qs from 'qs';
import Vue from 'vue';
import {DataOptions} from 'vuetify/types';
import Axios from '../axios';
import {Category, SelectOption, Thesis, ThesisTableHeader, UserOption} from '../types';
import {formatDataTableOrdering, readFileAsync} from '../utils';

export enum THESIS_MUTATIONS {
    SET_THESIS_LIST_RESPONSE = 'Set thesis list response',
    DELETE_THESIS_REVIEW = 'Delete thesis review',
    STORE_THESIS = 'Store thesis',
    UPDATE_THESIS = 'Update thesis',
}

export enum THESIS_ACTIONS {
    LOAD_THESES = '📡Load theses',
    SAVE_THESIS = 'Save thesis',
    EDIT_THESIS = 'Edit thesis',
    RELOAD_THESIS = 'Reload thesis',
    DELETE_REVIEW = 'Delete thesis review',
    SUBMIT_EXTERNAL_REVIEW = 'Submit external review',
    PUBLISH_THESIS = 'Publish thesis',
    SEND_TO_REVIEW = 'Send to review',
    SEND_TO_SUBMIT = 'Send to submit',
}

const state = {
    theses: {results: [] as Array<Thesis>, count: 0}
};
type State = typeof state;


export class ThesisListFilters {
    public readonly teacher: UserOption[];
    public readonly search: string[];

    constructor(
        private readonly teacherOrSearch: (UserOption & string)[],
        public readonly categories: Category[],
        public readonly years: SelectOption[]
    ) {
        [this.teacher, this.search] = _.partition(teacherOrSearch, v => !!v.value);
    }

    public asParams() {
        return {
            search: this.search.join(' '),
            teacher: this.teacher.map(i => i.username).join(','),
            category: this.categories.map(c => c.id).join(','),
            year: this.years.map(c => c.value).join(',')
        };
    }
}


export default {
    namespaced: true,
    state: state as State,

    mutations: {
        [THESIS_MUTATIONS.SET_THESIS_LIST_RESPONSE](state: State, response) {
            Vue.set(state.theses, 'results', response.results);
            Vue.set(state.theses, 'count', response.count);
        },
        [THESIS_MUTATIONS.STORE_THESIS](state: State, thesis) {
            Vue.set(
                state.theses.results,
                _.findIndex(state.theses.results, {id: thesis.id}),
                thesis
            );
        },
        [THESIS_MUTATIONS.UPDATE_THESIS](state: State, data) {
            const index = _.findIndex(state.theses.results, {id: data.id});

            Vue.set(
                state.theses.results,
                index,
                _.merge({}, state.theses.results[index], data)
            );
        },
        [THESIS_MUTATIONS.DELETE_THESIS_REVIEW](state, {review_id, thesis_id}) {
            const thesis: Thesis = _.find(state.theses.results, {id: thesis_id});

            Vue.delete(
                thesis.reviews,
                _.findIndex(thesis.reviews, {id: review_id})
            );
        }
    },
    actions: {
        async [THESIS_ACTIONS.LOAD_THESES](store, {
            options,
            filters,
            headers
        }: { filters: ThesisListFilters, options: DataOptions, headers: ThesisTableHeader[] }) {
            const {page, itemsPerPage} = options;

            const query = qs.stringify({
                page,
                ordering: formatDataTableOrdering(options, headers),
                page_size: itemsPerPage,
                ...filters.asParams()
            });

            const response = (await Axios.get(`/api/v1/thesis?${query}`)).data;

            store.commit(THESIS_MUTATIONS.SET_THESIS_LIST_RESPONSE, response);
        },

        async [THESIS_ACTIONS.SAVE_THESIS]({commit, dispatch}, data) {
            return dispatch(
                THESIS_ACTIONS.EDIT_THESIS,
                {
                    ...data,
                    supervisor_id: data.supervisor?.id,
                    opponent_id: data.opponent?.id,
                    authors: data.authors,
                    category_id: data.category?.id
                }
            );
        },

        async [THESIS_ACTIONS.EDIT_THESIS]({commit}, data) {
            return Axios.patch(
                `/api/v1/thesis/${data.id}`,
                data
            ).then(r => {
                if (r.status == 200)
                    commit(THESIS_MUTATIONS.STORE_THESIS, r.data);
                return r.data;
            });
        },

        async [THESIS_ACTIONS.RELOAD_THESIS]({commit}, thesis_id) {
            return Axios.get(
                `/api/v1/thesis/${thesis_id}`
            ).then(r => {
                commit(THESIS_MUTATIONS.STORE_THESIS, r.data);
                return r.data;
            });
        },

        async [THESIS_ACTIONS.PUBLISH_THESIS]({commit}, thesis_id) {
            return Axios.patch(
                `/api/v1/thesis/${thesis_id}/publish`
            ).then(r => {
                if (r.status == 200)
                    commit(THESIS_MUTATIONS.STORE_THESIS, r.data);
                return r;
            });
        },

        async [THESIS_ACTIONS.DELETE_REVIEW]({commit, state: State}, {review_id, thesis_id}) {
            await Axios.delete(`/api/v1/review/${review_id}`).then(r => {
                commit(THESIS_MUTATIONS.DELETE_THESIS_REVIEW, {review_id, thesis_id});
            });
        },

        async [THESIS_ACTIONS.SUBMIT_EXTERNAL_REVIEW]({commit, state: State}, {thesis_id, review}) {
            let data = new FormData();

            await readFileAsync(review.review);
            data.append('review', review.review);
            data.append('reviewer', review.reviewer);

            return Axios.post(
                `/api/v1/thesis/${thesis_id}/submit_external_review`,
                data,
                {headers: {'Content-Type': 'multipart/form-data'}}
            ).then(r => {
                commit(THESIS_MUTATIONS.STORE_THESIS, r.data);

                return r.data;
            });
        },

        async [THESIS_ACTIONS.SEND_TO_REVIEW]({commit, state: State}, {thesis_id}) {
            return Axios.patch(
                `/api/v1/thesis/${thesis_id}/send_to_review`
            ).then(r => {
                if (r.status == 200)
                    commit(THESIS_MUTATIONS.STORE_THESIS, r.data);

                return r.data;
            });
        },
        async [THESIS_ACTIONS.SEND_TO_SUBMIT]({commit, state: State}, {thesis_id}) {
            return Axios.patch(
                `/api/v1/thesis/${thesis_id}/send_to_submit`
            ).then(r => {
                if (r.status == 200)
                    commit(THESIS_MUTATIONS.STORE_THESIS, r.data);

                return r.data;
            });
        }
    },
    getters: {
        availableExternalReviewersOptions: () => (thesis: Thesis) =>
            _.map(
                _.filter(
                    ['supervisor', 'opponent'],
                    (key) => (
                        // show option to upload if:
                        !_.find( // does not already have uploaded review
                            thesis.attachments,
                            {
                                type_attachment: {identifier: `${key}_review`}
                            }
                        ) && // and
                        thesis[key]?.id && // has set user
                        !thesis[key]?.is_active && // is not active (is external
                        !_.find( // but without internal review
                            thesis.reviews,
                            {
                                user: {id: thesis[key].id}
                            }
                        )
                    )
                ),
                (k) => [k, thesis[k]] // format to [key, User]
            )
    }
};