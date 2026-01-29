import axios from 'axios';

const api = axios.create({
  baseURL: 'https://ervelus-web-service-324377414272.us-central1.run.app',
  withCredentials: true
});

export default api;