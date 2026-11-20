import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('riskwise_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
};

export const mlAPI = {
  predict: (data) => api.post('/predict', data),
  getMetrics: () => api.get('/model/metrics'),
  getInfo: () => api.get('/model/info'),
};

export const transactionAPI = {
  list: (params) => api.get('/transactions', { params }),
  getById: (id) => api.get(`/transactions/${id}`),
};

export const alertAPI = {
  list: (params) => api.get('/alerts', { params }),
  update: (id, data) => api.patch(`/alerts/${id}`, data),
};

export const investigationAPI = {
  list: (params) => api.get('/investigations', { params }),
  create: (data) => api.post('/investigations', data),
  getById: (id) => api.get(`/investigations/${id}`),
  addNote: (id, data) => api.post(`/investigations/${id}/notes`, data),
};

export const analyticsAPI = {
  overview: () => api.get('/analytics/overview'),
  riskDistribution: () => api.get('/analytics/risk-distribution'),
  trends: () => api.get('/analytics/trends'),
};

export const userAPI = {
  list: () => api.get('/users'),
  updateRole: (id, role) => api.patch(`/users/${id}/role`, { role }),
};

export const systemAPI = {
  health: () => api.get('/health'),
};

export default api;
