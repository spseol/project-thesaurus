import Vue from 'vue';
import Vuex, {createNamespacedHelpers} from 'vuex';
import thesis from './thesis';

Vue.use(Vuex);
const store = new Vuex.Store({
    modules: {
        thesis
    }
});


export const thesisStore = createNamespacedHelpers('thesis');

export default store;