import VueRouter from 'vue-router';
import {Store} from 'vuex';
import {PERMS, PERMS_ACTIONS} from './store/perms';
import {eventBus} from './utils';

export function createRouter($t, store: Store<any>) {
    const router = new VueRouter({
        routes: [
            {
                path: '/:locale/', // unknown locales handles Django itself by locale middleware
                component: {template: '<keep-alive><router-view></router-view></keep-alive>'},
                children: [
                    {path: '', component: () => import('./pages/Dashboard/Page.vue'), name: 'dashboard'},
                    {
                        path: 'thesis/list',
                        component: () => import('./pages/ThesisList/Page.vue'),
                        name: 'thesis-list'
                    },
                    {
                        path: 'thesis/prepare',
                        component: () => import('./pages/ThesisPrepare/Page.vue'),
                        name: 'thesis-prepare',
                        meta: {perm: PERMS.ADD_THESIS}
                    },
                    {
                        path: 'thesis/submit/:id',
                        component: () => import('./pages/ThesisSubmit/Page.vue'),
                        name: 'thesis-submit'
                    },
                    {
                        path: 'reservations/list',
                        component: () => import('./pages/ReservationList/Page.vue'),
                        name: 'reservation-list',
                        meta: {perm: PERMS.CHANGE_RESERVATION}
                    },
                    {
                        path: 'exports',
                        component: () => import('./pages/Exports/Page.vue'),
                        name: 'exports',
                        meta: {perm: PERMS.VIEW_USER}
                    },
                    {
                        path: 'settings',
                        component: {template: '<div>Nonono</div>'},
                        name: 'settings'
                    },
                    {
                        path: 'review/:thesisId/:reviewId?',
                        component: () => import('./pages/ReviewSubmit/Page.vue'),
                        name: 'review-detail'
                    },
                    {path: '404', component: () => import('./components/404.vue'), name: '404'},
                    {path: '403', component: () => import('./components/403.vue'), name: '403'},
                    {path: '*', redirect: {name: '404'}}
                ]
            },
            {path: '*', redirect: {name: '404'}}
        ],
        mode: 'history'
    });

    router.beforeEach(async (to, from, next) => {
        await store.dispatch(`perms/${PERMS_ACTIONS.LOAD_PERMS}`);

        if (!(to.meta?.perm)) {
            next();
            return;
        }

        const allowed = store.state.perms.perms[to.meta.perm];

        if (allowed) {
            next();
        } else {
            eventBus.flash({color: 'warning', text: $t('Permission denied')});
            next({name: '403'});
        }
    });
    return router;
}