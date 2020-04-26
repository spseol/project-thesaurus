import Axios, {AxiosInstance, AxiosRequestConfig} from 'axios';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN'
};

const axios: AxiosInstance = Axios.create(config);

export default axios;

