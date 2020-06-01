import Vue from 'vue';
import Vuex, {createNamespacedHelpers} from 'vuex';
import attachment from './attachment';
import options from './options';
import perms from './perms';
import reservation from './reservation';
import thesis from './thesis';

Vue.use(Vuex);

const createStore = () => {
    return new Vuex.Store({
        modules: {
            thesis,
            options,
            perms,
            reservation,
            attachment
        }
        // @ts-ignore
        // strict: process.env.NODE_ENV !== 'production'
    });
};


export const attachmentStore = createNamespacedHelpers('attachment');
export const optionsStore = createNamespacedHelpers('options');
export const permsStore = createNamespacedHelpers('perms');
export const reservationStore = createNamespacedHelpers('reservation');
export const thesisStore = createNamespacedHelpers('thesis');

export default createStore;