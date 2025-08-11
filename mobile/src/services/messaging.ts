import { api } from '@/services/api';

export async function sendMessage(phone: string, message: string) {
  const res = await api.post('/messaging/send', { phone, message });
  return res.data;
}