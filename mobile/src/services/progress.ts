import { api } from '@/services/api';

export async function getProgressLogs(userId: number) {
  const res = await api.get(`/progress/${userId}`);
  return res.data;
}

export async function createProgress(data: any) {
  const res = await api.post('/progress', data);
  return res.data;
}

export async function updateProgress(id: number, data: any) {
  const res = await api.put(`/progress/${id}`, data);
  return res.data;
}

export async function deleteProgress(id: number) {
  const res = await api.delete(`/progress/${id}`);
  return res.data;
}