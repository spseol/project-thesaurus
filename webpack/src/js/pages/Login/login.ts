import createVue from './../../app';
import Login from './Login.vue';

createVue({
    router: undefined,
    store: undefined,
    render: h => h(Login)
}).$mount('#app');