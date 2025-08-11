import { api } from '@/services/api';

export async function getRevenue(params: { start_date?: string; end_date?: string; granularity: 'weekly' | 'monthly'; }) {
  const res = await api.post('/analytics/revenue', params);
  return res.data as { points: { period: string; amount: number }[]; total: number };
}

export async function getInsights() {
  const res = await api.get('/analytics/member-insights');
  return res.data;
}