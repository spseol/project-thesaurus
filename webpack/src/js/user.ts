import Axios from './axios';


async function hasPerm(perm: string): Promise<boolean> {
    return (await Axios.get(`/api/v1/has-perm/${perm}`)).data;
}

export default hasPerm;