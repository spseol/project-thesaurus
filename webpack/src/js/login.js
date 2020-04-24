import createVue from './app';
import Login from './Login';

createVue({
    router: undefined,
    render: h => h(Login),
}).$mount('#app');