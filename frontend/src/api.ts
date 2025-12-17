// frontend/src/api.ts
import axios from 'axios';

// Base URL and default key from environment
const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
const ENV_KEY = import.meta.env.VITE_API_KEY || 'demo-key';

// Use localStorage override if present
const initialKey = localStorage.getItem('apiKey') || ENV_KEY;

// Axios instance with dynamic API key
export const api = axios.create({
  baseURL: API_BASE,
  headers: { 'X-API-Key': initialKey },
});

// Utility to update API key at runtime (e.g. role switcher)
export function setApiKey(key: string) {
  api.defaults.headers['X-API-Key'] = key;
  localStorage.setItem('apiKey', key);
}

// ---- API functions ----

export async function getInsights() {
  const { data } = await api.get('/insights');
  return data;
}

export async function getSegments() {
  const { data } = await api.get('/segments');
  return data;
}

export async function getForecast(days = 30) {
  const { data } = await api.get('/forecast', { params: { days } });
  return data;
}

export async function uploadCSV(file: File) {
  const form = new FormData();
  form.append('file', file);
  const { data } = await api.post('/upload', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return data;
}

export async function seedDemo() {
  const { data } = await api.post('/seed');
  return data;
}

// ---- ML endpoints ----

export async function trainChurn() {
  const { data } = await api.post('/ml/churn/train');
  return data as { status: string; accuracy: number };
}

export async function predictChurn() {
  const { data } = await api.get('/ml/churn/predict');
  return data.results as {
    customer_id: string;
    recency: number;
    frequency: number;
    monetary: number;
    churn_probability: number;
  }[];
}

// ---- Analytics endpoints ----

export async function getAnomalies(z = 2.0) {
  const { data } = await api.get('/analytics/anomalies', { params: { z } });
  return data.anomalies as {
    date: string;
    amount: number;
    z: number;
    is_anomaly: boolean;
  }[];
}

// ---- Reports endpoints ----

export async function getSummaryReport() {
  const { data } = await api.get('/reports/summary');
  return data.summary as string;
}