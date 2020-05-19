import Axios from './axios';
import {pageContext} from './utils';

function memoize(method) {
    let cache = {};

    return async function(...args) {
        let key = JSON.stringify(args);
        cache[key] = cache[key] || method.apply(this, args);
        return cache[key];
    };
}

async function hasPermUncached(perm: string): Promise<boolean> {
    return (await Axios.get(`/api/v1/has-perm/${perm}`)).data;
}

export async function hasGroup(group: string): Promise<boolean> {
    return (await pageContext.groups.indexOf(group) >= 0);
}

/**
 * @type {(perm: string) => Promise<Boolean>}
 */
export const hasPerm = memoize(hasPermUncached);
