import LocalForage from 'localforage';

export const axiosCacheStore: LocalForage = LocalForage.createInstance({
    name: 'thesaurus-axios-cache'
});

export const appCache: LocalForage = LocalForage.createInstance({
    name: 'thesaurus-cache'
});