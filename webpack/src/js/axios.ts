import StaticAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';

import {setupCache} from 'axios-cache-adapter';
import {axiosCacheStore} from './cache';
import {notificationBus, pageContext} from './utils';

declare var __DEVELOPMENT__: boolean;


// Create `axios-cache-adapter` instance
const cache = setupCache({
    maxAge: 15 * 60 * 1000, // 15 minutes,
    debug: __DEVELOPMENT__,
    store: axiosCacheStore,
    readHeaders: true,
    // include user, locale, path and params to cache key
    key(req: AxiosRequestConfig): string {
        return [
            pageContext.user.username,
            pageContext.locale,
            req.url,
            (new URLSearchParams(req.params)).toString()
        ].filter(Boolean).join('|');
    }
});

const config: AxiosRequestConfig = {
    // defined by django
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
    validateStatus: function(status) {
        return (status >= 200 && status < 300) || status == 400 || status == 403; // default
    }
};

export const Axios: AxiosInstance = StaticAxios.create(config);
// TODO: fix cache adapter
// export const CachedAxios: AxiosInstance = StaticAxios.create({...config, adapter: cache.adapter});
export const CachedAxios = Axios;

const errorResponseHandler = (error) => {
    if (error?.response?.status === 401) {
        window.location.reload();
    } else if (error?.response?.status === 403) {
        if (error?.response?.config?.allow403) {
            return;
        }
        notificationBus.warning(error.response?.data?.detail || 'Access denied.');
    } else if (error?.response?.status >= 500) {
        notificationBus.flash({color: 'error', text: error.response.data?.error || 'Server error.'});
    }
    return Promise.reject(error);
};

const localeRequestHandler = (config) => {
    config.headers['Accept-Language'] = pageContext.locale;
    return config;
};

Axios.interceptors.response.use(null, errorResponseHandler);
CachedAxios.interceptors.response.use(null, errorResponseHandler);

Axios.interceptors.request.use(localeRequestHandler);
CachedAxios.interceptors.request.use(localeRequestHandler);

export default Axios;
