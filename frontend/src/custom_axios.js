import axios from 'axios';

const REST_URL = process.env.VUE_APP_REST_API

export default axios.create({
    baseURL: REST_URL,
    withCredentials: true,
})