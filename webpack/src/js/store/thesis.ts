import * as _ from 'lodash';
import * as qs from 'qs';
import Vue from 'vue';
import Axios from '../axios';
import {Thesis} from '../types';
import {readFileAsync} from '../utils';

export enum THESIS_MUTATIONS {
    SET_THESIS_LIST_RESPONSE = 'Set thesis list response',
    DELETE_THESIS_REVIEW = 'Delete thesis review',
    DELETE_THESIS_ATTACHMENT = 'Delete thesis attachment',
    ADD_THESIS_ATTACHMENT = 'Add thesis attachment',
}

export enum THESIS_ACTIONS {
    LOAD_THESES = '📡Load theses',
    SAVE_THESIS = 'Save thesis',
    DELETE_REVIEW = 'Delete thesis review',
    DELETE_ATTACHMENT = 'Delete thesis attachment',
    UPLOAD_ATTACHMENT = 'Upload thesis attachment',
}

const state = {
    theses: {results: [], count: 0}
};
type State = typeof state;


export default {
    namespaced: true,
    state: state as State,
    mutations: {
        [THESIS_MUTATIONS.SET_THESIS_LIST_RESPONSE](state: State, response) {
            state.theses.results = response.results;
            state.theses.count = response.count;
        },
        [THESIS_MUTATIONS.DELETE_THESIS_REVIEW](state, {review_id, thesis_id}) {
            const thesis: Thesis = _.find(state.theses.results, {id: thesis_id});

            Vue.delete(
                thesis.reviews,
                _.findIndex(thesis.reviews, {id: review_id})
            );
        },
        [THESIS_MUTATIONS.DELETE_THESIS_ATTACHMENT](state, {attachment_id, thesis_id}) {
            const thesis: Thesis = _.find(state.theses.results, {id: thesis_id});

            Vue.delete(
                thesis.attachments,
                _.findIndex(thesis.attachments, {id: attachment_id})
            );
        },
        [THESIS_MUTATIONS.ADD_THESIS_ATTACHMENT](state, {thesis_id, attachment}) {
            const thesis: Thesis = _.find(state.theses.results, {id: thesis_id});

            thesis.attachments.push(attachment);
        }
    },
    actions: {
        async [THESIS_ACTIONS.LOAD_THESES](store, {options, filters, headers}) {
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


            store.commit(THESIS_MUTATIONS.SET_THESIS_LIST_RESPONSE, response);

        },

        async [THESIS_ACTIONS.SAVE_THESIS](store, data) {
            return (await Axios.patch(
                `/api/v1/thesis/${data.id}`,
                {
                    ...data,
                    supervisor_id: data.supervisor?.id,
                    opponent_id: data.opponent?.id,
                    authors: data.authors,
                    category_id: data.category?.id
                }
            )).data;
        },

        async [THESIS_ACTIONS.DELETE_REVIEW]({commit, state: State}, {review_id, thesis_id}) {
            await Axios.delete(`/api/v1/review/${review_id}`).then(r => {
                commit(THESIS_MUTATIONS.DELETE_THESIS_REVIEW, {review_id, thesis_id});
            });
        },
        async [THESIS_ACTIONS.DELETE_ATTACHMENT]({commit, state: State}, {attachment_id, thesis_id}) {
            await Axios.delete(`/api/v1/attachment/${attachment_id}`).then(r => {
                commit(THESIS_MUTATIONS.DELETE_THESIS_ATTACHMENT, {attachment_id, thesis_id});
            });
        },
        async [THESIS_ACTIONS.UPLOAD_ATTACHMENT]({commit, state: State}, {thesis_id, attachment}) {

            const form = new FormData();
            await readFileAsync(attachment.file);

            form.append('file', attachment.file);
            form.append('thesis_id', thesis_id);
            form.append('type_attachment_id', attachment.type_attachment.id);

            return Axios.post(
                `/api/v1/attachment`,
                form,
                {headers: {'Content-Type': 'multipart/form-data'}}
            ).then(r => {
                // TODO: check 200
                commit(THESIS_MUTATIONS.ADD_THESIS_ATTACHMENT, {
                    thesis_id,
                    attachment: r.data
                });

                return r.data;
            });
        }
    }
};