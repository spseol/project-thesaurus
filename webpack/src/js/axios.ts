import OrigAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';
import {eventBus} from './utils';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
    validateStatus: function(status) {
        return (status >= 200 && status < 300) || status == 400; // default
    }
};

const Axios: AxiosInstance = OrigAxios.create(config);

Axios.interceptors.response.use(null, (error) => {
    if (error.response.status === 403) {
        eventBus.flash({color: 'warning', text: error.response.data?.detail || 'Access denied.'});
    } else if (error.response.status >= 500) {
        eventBus.flash({color: 'error', text: error.response.data?.error || 'Server error.'});
    }
    console.warn(error.response.data);
    return Promise.reject(error);
});

export default Axios;

