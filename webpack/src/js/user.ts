import {CachedAxios} from './axios';
import {memoize, pageContext} from './utils';


async function hasPermUncached(perm: string): Promise<boolean> {
    return (await CachedAxios.get(`/api/v1/has-perm/${perm}`)).data;
}

export async function hasGroup(group: string): Promise<boolean> {
    return (await pageContext.groups.indexOf(group) >= 0);
}

/**
 * @type {(perm: string) => Promise<Boolean>}
 */
export const hasPerm = memoize(hasPermUncached);
