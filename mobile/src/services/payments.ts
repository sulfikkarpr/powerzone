import { api } from '@/services/api';

export async function getReminders(userId: number) {
  const res = await api.get(`/payments/reminders/${userId}`);
  return res.data;
}

export async function createReminder(data: { user_id: number; due_date: string; amount: number; }) {
  const res = await api.post('/payments/reminders', data);
  return res.data;
}

export async function markPaid(id: number) {
  const res = await api.post(`/payments/reminders/${id}/mark-paid`);
  return res.data;
}