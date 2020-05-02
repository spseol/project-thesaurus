import OrigAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN',
    // TODO: intercept 403 and 5XX
    validateStatus: function(status) {
        return (status >= 200 && status < 300) || status == 400; // default
    }
};

const Axios: AxiosInstance = OrigAxios.create(config);

export default Axios;

