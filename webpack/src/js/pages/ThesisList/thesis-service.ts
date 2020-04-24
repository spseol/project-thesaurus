import * as _ from 'lodash';
import * as qs from 'qs';
import {DataOptions, DataTableHeader} from 'vuetify';
import Axios from '../../api-client';

export interface MappedDataTableHeader extends DataTableHeader {
    mapped?: string
}

export default class ThesisService {

    constructor(
        private headers: Array<MappedDataTableHeader>
    ) {
    }

    async loadData(options: DataOptions, search: any) {
        const {page, sortBy, sortDesc} = options;

        const remap = (value) => (_.find(this.headers, {value})).mapped || value.replace('.', '__');

        return await Axios.get(`/api/v1/thesis/?${qs.stringify({
            page,
            search: search,
            ordering: _.map(
                _.zip(sortBy, sortDesc),
                ([col, desc]) => `${desc ? '-' : ''}${remap(col).split('.')[0]}`
            ).join(',')
        })}`);
    }
}