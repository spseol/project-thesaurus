import createVue from './app';
import Login from './Login';

console.log('Pičo!');
createVue({
    router: undefined,
    render: h => h(Login),
}).$mount('#app');