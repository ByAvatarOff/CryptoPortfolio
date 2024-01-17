import axios from "axios";


let BASE_URL = 'http://127.0.0.1:8000/';

export const requestTemplate = axios.create({
  baseURL: BASE_URL,
});


requestTemplate.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers["Authorization"] = 'Bearer ' + token;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

requestTemplate.interceptors.response.use(
  response => response,
  error => {
    if (error.response.status === 401) {
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);