import Vue from 'vue';
import Vuex, {createNamespacedHelpers} from 'vuex';
import options from './options';
import perms from './perms';
import thesis from './thesis';

Vue.use(Vuex);
const store = new Vuex.Store({
    modules: {
        thesis,
        options,
        perms
    }
});


export const thesisStore = createNamespacedHelpers('thesis');
export const optionsStore = createNamespacedHelpers('options');
export const permsStore = createNamespacedHelpers('perms');

export default store;