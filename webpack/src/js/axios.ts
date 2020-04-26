import OrigAxios, {AxiosInstance, AxiosRequestConfig} from 'axios';

const config: AxiosRequestConfig = {
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFTOKEN'
};

const Axios: AxiosInstance = OrigAxios.create(config);

export default Axios;

