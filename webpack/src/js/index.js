// import 'bootstrap-material-design/js/bootstrapMaterialDesign'
import 'scss/index.scss';
// import 'bootstrap';
import Vue from 'vue';
import vuetify from './plugins/vuetify-plugin'; // path to vuetify export
import ThesisList from './components/ThesisList';

new Vue({
    vuetify,
    components: {ThesisList},
    template: '<v-app><ThesisList /></v-app>',
}).$mount('#app');