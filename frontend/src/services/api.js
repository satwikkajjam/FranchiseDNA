import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:5002/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
});

export const getPopulationData = () => api.get('/population');

export const searchAreas = (query) => api.get(`/population/search?q=${encodeURIComponent(query)}`);

export const getFranchises = () => api.get('/franchises');

export const getFranchise = (id) => api.get(`/franchises/${id}`);

export const geocodeArea = (area) => api.get(`/geocode?area=${encodeURIComponent(area)}`);

export const runAnalysis = (data) => api.post('/analyze', data);

export const generatePdfReport = (data) =>
  api.post('/report/pdf', data, { responseType: 'blob' });

export const getHeatmapData = () => api.get('/heatmap');

export const getReports = () => api.get('/reports');

export default api;
