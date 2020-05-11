import Axios from './axios';

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

const hasPerm = memoize(hasPermUncached);

export default hasPerm;