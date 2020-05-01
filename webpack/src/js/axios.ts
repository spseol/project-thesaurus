import OrigAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN'
    // TODO: intercept 403 and 5XX
};

const Axios: AxiosInstance = OrigAxios.create(config);

export default Axios;

