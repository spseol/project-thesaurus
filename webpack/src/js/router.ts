import VueRouter from 'vue-router';
import {hasPerm} from './user';
import {eventBus} from './utils';

export function createRouter($t) {
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
                        meta: {perm: 'thesis.add_thesis'}
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
                        meta: {perm: 'thesis.change_reservation'}
                    },
                    {
                        path: 'exports',
                        component: () => import('./pages/Exports/Page.vue'),
                        name: 'exports',
                        meta: {perm: 'accounts.view_user'}
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

    router.beforeEach((to, from, next) => {
        if (!(to.meta?.perm)) {
            next();
            return;
        }
        hasPerm(to.meta.perm).then(allow => {
            if (allow) {
                next();
            } else {
                eventBus.flash({color: 'warning', text: $t('Permission denied')});
                next({name: '403'});
            }
        }).catch(() => {
            eventBus.flash({color: 'warning', text: $t('Unknown problem')});
            next({name: '403'});
        });
    });
    return router;
}