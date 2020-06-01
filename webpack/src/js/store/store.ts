import Vue from 'vue';
import Vuex, {createNamespacedHelpers} from 'vuex';
import options from './options';
import perms from './perms';
import reservation from './reservation';
import thesis from './thesis';

Vue.use(Vuex);
const store = new Vuex.Store({
    modules: {
        thesis,
        options,
        perms,
        reservation
    }
});


export const thesisStore = createNamespacedHelpers('thesis');
export const optionsStore = createNamespacedHelpers('options');
export const permsStore = createNamespacedHelpers('perms');
export const reservationStore = createNamespacedHelpers('reservation');

export default store;