import ThesisList from './ThesisList';
import createVueFactory from '../base-vue';


export default function installThesisList(el, data = {}) {
    return createVueFactory({
        data: () => data,

        components: {ThesisList},
        template: '<ThesisList />',
    }).$mount(el);
}