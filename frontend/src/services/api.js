import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // URL вашого Django-бекенду
  withCredentials: true, // Дозволяє автоматично надсилати cookies
});

// Автоматично додаємо CSRF-токен до запитів
api.interceptors.request.use(config => {
  const csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1];
  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
});

export default api;