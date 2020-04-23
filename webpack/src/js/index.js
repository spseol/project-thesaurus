// import 'scss/index.scss';
import createVueFactory from './components/base-vue';
import App from './components/App';


createVueFactory({
    el: '#app',
    render: h => h(App),
});