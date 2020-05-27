import OrigAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';
import {eventBus, pageContext} from './utils';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
    validateStatus: function(status) {
        return (status >= 200 && status < 300) || status == 400; // default
    }
};

const Axios: AxiosInstance = OrigAxios.create(config);

Axios.interceptors.response.use(null, (error) => {
    if (error?.response.status === 403) {
        eventBus.flash({color: 'warning', text: error.response.data?.detail || 'Access denied.'});
    } else if (error?.response.status >= 500) {
        eventBus.flash({color: 'error', text: error.response.data?.error || 'Server error.'});
    }
    return Promise.reject(error);
});

Axios.interceptors.request.use(
    (config) => {
        config.headers['Accept-Language'] = pageContext.locale;
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default Axios;

