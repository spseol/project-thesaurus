import * as _ from 'lodash';
import * as qs from 'qs';
import {DataOptions, DataTableHeader} from 'vuetify';
import Axios from '../../axios';

export default class ThesisService {
    async loadData(options: DataOptions, filter: Array<any>, headers: Array<DataTableHeader>) {
        const {page, sortBy, sortDesc} = options;

        const remap = (value) => value.replace('.', '__');

        return await Axios.get(`/api/v1/thesis?${qs.stringify({
            page,
            search: _.map(filter, (i) => i.username || i.id || i).join(' '),
            ordering: _.map(
                _.zip(sortBy, sortDesc),
                ([col, desc]) => `${desc ? '-' : ''}${remap(col).split('.')[0]}`
            ).join(',')
        })}`);
    }
}