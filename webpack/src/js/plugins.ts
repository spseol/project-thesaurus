import {hasGroup, hasPerm} from './user';

export const I18nRoutePlugin = {
    install(Vue, options) {
        Vue.prototype.$i18nRoute = function(to) {
            return Object.assign({}, to, {params: {locale: this.$i18n.locale, ...(to.params || {})}});
        };
    }
};

export const DjangoPermsPlugin = {
    PERM_REGEX: /[a-z][a-z_]+\.[a-z_]+/i,
    _implementation(resolver) {
        return (el, bindings, vnode) => {
            if (!bindings.arg) return;
            // dot is modifier sign for vue directives and also app splitter for Django perms, needed manual parse
            // {name: has-perm, rawName: 'v-has-perm:not:thesis.add_reservation',
            //  arg: 'not:thesis', modifiers: {add_reservation: true,},};

            // {name: 'has-perm', rawName: 'v-has-perm:[item.perm]', arg: 'thesis.view_thesis', modifiers: {}};
            const value = this.PERM_REGEX.test(bindings.arg) ? bindings.arg : bindings.rawName.replace(/v-[^:]+:/g, '');

            el.style.display = 'none';
            resolver(value).then((allowed) => {
                if (allowed)
                    el.style.display = null;
                else
                    el.style.display = 'none';
            }).catch(() => {
                    el.style.display = 'none';
                }
            );
        };
    },

    install(Vue, options) {
        // TODO: think about https://github.com/mblarsen/vue-browser-acl
        Vue.directive('has-perm', {inserted: this._implementation(hasPerm)});

        Vue.directive('has-group', {inserted: this._implementation(hasGroup)});
    }
};
