process.env.VUE_APP_REST_API = process.env.NODE_ENV === 'production' ?
    process.env.REST_API_URL : 'http://localhost:8000/api/v1.0/';

module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
        ? process.env.VUE_PUBLIC_PATH // URL for production server
        : '/',
        assetsDir: 'static'
};