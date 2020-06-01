import StaticAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';
import {notificationBus, pageContext} from './utils';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
    validateStatus: function(status) {
        return (status >= 200 && status < 300) || status == 400 || status == 403; // default
    }
};

const Axios: AxiosInstance = StaticAxios.create(config);

Axios.interceptors.response.use(null, (error) => {
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

