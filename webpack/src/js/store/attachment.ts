import * as _ from 'lodash';
import Vue from 'vue';
import Axios from '../axios';
import {Thesis} from '../types';
import {readFileAsync} from '../utils';

export enum ATTACHMENT_MUTATIONS {
    DELETE_THESIS_ATTACHMENT = 'Delete attachment',
    ADD_THESIS_ATTACHMENT = 'Add attachment',
}

export enum ATTACHMENT_ACTIONS {
    DELETE_ATTACHMENT = 'Delete attachment',
    UPLOAD_ATTACHMENT = 'Upload attachment',
}

const state = {};
type State = typeof state;


export default {
    namespaced: true,
    state: state as State,

    mutations: {
        [ATTACHMENT_MUTATIONS.DELETE_THESIS_ATTACHMENT](state, {attachment_id, thesis_id, rootState}) {
            const thesis: Thesis = _.find(rootState.thesis.theses.results, {id: thesis_id});

            Vue.delete(
                thesis.attachments,
                _.findIndex(thesis.attachments, {id: attachment_id})
            );
        },
        [ATTACHMENT_MUTATIONS.ADD_THESIS_ATTACHMENT](state, {thesis_id, attachment, rootState}) {
            const thesis: Thesis = _.find(rootState.thesis.theses.results, {id: thesis_id});

            thesis.attachments.push(attachment);
        }
    },
    actions: {
        async [ATTACHMENT_ACTIONS.DELETE_ATTACHMENT]({commit, state: State, rootState}, {attachment_id, thesis_id}) {
            await Axios.delete(`/api/v1/attachment/${attachment_id}`).then(r => {
                commit(ATTACHMENT_MUTATIONS.DELETE_THESIS_ATTACHMENT, {attachment_id, thesis_id, rootState});
            });
        },

        async [ATTACHMENT_ACTIONS.UPLOAD_ATTACHMENT]({commit, state: State, rootState}, {thesis_id, attachment}) {
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
                if (r.status == 201)
                    commit(ATTACHMENT_MUTATIONS.ADD_THESIS_ATTACHMENT, {
                        thesis_id,
                        attachment: r.data,
                        rootState
                    });

                return r.data;
            });
        }
    }
};