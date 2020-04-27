// stolen from vuetify/src/util/helpers
export function defaultFilter(value: any, search: string | null, item: any) {
    return value != null &&
        search != null &&
        typeof value !== 'boolean' &&
        value.toString().toLocaleLowerCase().indexOf(search.toLocaleLowerCase()) !== -1;
}