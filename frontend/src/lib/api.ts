/**
 * API Client
 */
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const projectsApi = {
  list: (params?: any) => api.get('/api/projects', { params }),
  get: (id: number) => api.get(`/api/projects/${id}`),
  create: (data: any) => api.post('/api/projects', data),
  delete: (id: number) => api.delete(`/api/projects/${id}`),
};

export const agentsApi = {
  list: (params?: any) => api.get('/api/agents', { params }),
  get: (id: string) => api.get(`/api/agents/${id}`),
  stats: (id: string) => api.get(`/api/agents/${id}/stats`),
};

export const settingsApi = {
  getConfig: () => api.get('/api/settings/config'),
  listApiKeys: () => api.get('/api/settings/api-keys'),
  createApiKey: (data: any) => api.post('/api/settings/api-keys', data),
  updateApiKey: (provider: string, data: any) =>
    api.patch(`/api/settings/api-keys/${provider}`, data),
  deleteApiKey: (provider: string) =>
    api.delete(`/api/settings/api-keys/${provider}`),
};

export const healthApi = {
  check: () => api.get('/api/health'),
  detailed: () => api.get('/api/health/detailed'),
};
