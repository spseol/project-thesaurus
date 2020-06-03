import Vue from 'vue';
import Vuex, {createNamespacedHelpers, Store as VuexStore} from 'vuex';

import attachment from './attachment';
import audit from './audit';
import dashboard from './dashboard';
import options from './options';
import perms from './perms';
import reservation from './reservation';
import review from './review';
import thesis from './thesis';

Vue.use(Vuex);

interface Store<T> extends VuexStore<T> {
    $asyncStart(identifier: string): any;

    $asyncEnd(identifier: string): any;

    $asyncFail(identifier: string, message?: string): any;
}

const createCallsPlugin = () => (store: VuexStore<any>) => {
    (store as Store<any>).$asyncStart = function(identifier: string) {
        return this.commit('calls/START', {identifier}, {root: true});
    };
    (store as Store<any>).$asyncEnd = function(identifier: string) {
        return this.commit('calls/END', {identifier}, {root: true});
    };
    (store as Store<any>).$asyncFail = function(identifier: string, message?: string) {
        return this.commit('calls/END', {identifier, message}, {root: true});
    };
};

export const createStore = (): Store<any> => {
    return new Vuex.Store({
        modules: {
            attachment,
            audit,
            dashboard,
            options,
            perms,
            reservation,
            review,
            thesis

        },
        plugins: [createCallsPlugin()]
        // @ts-ignore
        // strict: process.env.NODE_ENV !== 'production'
    }) as Store<any>;
};


export const auditStore = createNamespacedHelpers('audit');
export const attachmentStore = createNamespacedHelpers('attachment');
export const dashboardStore = createNamespacedHelpers('dashboard');
export const optionsStore = createNamespacedHelpers('options');
export const permsStore = createNamespacedHelpers('perms');
export const reservationStore = createNamespacedHelpers('reservation');
export const thesisStore = createNamespacedHelpers('thesis');
export const reviewStore = createNamespacedHelpers('review');


