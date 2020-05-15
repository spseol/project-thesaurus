import hasPerm from './user';

export const I18nRoutePlugin = {
    install(Vue, options) {
        Vue.prototype.$i18nRoute = function(to) {
            return Object.assign({}, to, {params: {locale: this.$i18n.locale, ...(to.params || {})}});
        };
    }
};

export const DjangoPermsPlugin = {
    _implementation(negate = false) {
        return ((_negate = negate) =>
                (el, bindings, vnode) => {
                    if (!bindings.arg) return;
                    // dot is modifier sign for vue directives and also app splitter for Django perms, needed manual parse
                    // {name: has-perm, rawName: 'v-has-perm:not:thesis.add_reservation',
                    //  arg: 'not:thesis', modifiers: {add_reservation: true,},};

                    // {name: 'has-perm', rawName: 'v-has-perm:[item.perm]', arg: 'thesis.view_thesis', modifiers: {}};
                    const perm = bindings.arg.indexOf('.') >= 0 ? bindings.arg : bindings.rawName.replace(/v-has(-not)?-perm:/g, '');

                    el.style.display = _negate ? null : 'none';
                    hasPerm(perm).then((allowed) => {
                        if (allowed)
                            el.style.display = _negate ? 'none' : null;
                        else
                            el.style.display = _negate ? null : 'none';
                    }).catch(() => {
                            el.style.display = _negate ? null : 'none';
                        }
                    );
                }
        )(negate);
    },

    install(Vue, options) {
        // TODO: think about https://github.com/mblarsen/vue-browser-acl
        Vue.directive('has-perm', {inserted: this._implementation(false)});
        // TODO: not working
        // Vue.directive('has-not-perm', {inserted: this._implementation(true)});
    }
};
