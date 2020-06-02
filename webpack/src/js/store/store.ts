import Vue from 'vue';
import Vuex, {createNamespacedHelpers} from 'vuex';
import attachment from './attachment';
import audit from './audit';
import options from './options';
import perms from './perms';
import reservation from './reservation';
import review from './review';
import thesis from './thesis';

Vue.use(Vuex);

const createStore = () => {
    return new Vuex.Store({
        modules: {
            audit,
            thesis,
            options,
            perms,
            reservation,
            attachment,
            review
        }
        // @ts-ignore
        // strict: process.env.NODE_ENV !== 'production'
    });
};


export const auditStore = createNamespacedHelpers('audit');
export const attachmentStore = createNamespacedHelpers('attachment');
export const optionsStore = createNamespacedHelpers('options');
export const permsStore = createNamespacedHelpers('perms');
export const reservationStore = createNamespacedHelpers('reservation');
export const thesisStore = createNamespacedHelpers('thesis');
export const reviewStore = createNamespacedHelpers('review');

export default createStore;