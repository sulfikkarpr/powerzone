import { api } from '@/services/api';

export async function getWorkoutPlans(userId: number) {
  const res = await api.get(`/plans/workout/${userId}`);
  return res.data;
}

export async function getMealPlans(userId: number) {
  const res = await api.get(`/plans/meal/${userId}`);
  return res.data;
}

export async function createWorkoutPlan(data: { user_id: number; plan_name: string; plan_details: any; duration_weeks: number; created_by: number; }) {
  const res = await api.post('/plans/workout', data);
  return res.data;
}

export async function createMealPlan(data: { user_id: number; meal_name: string; meal_details: any; goal: string; created_by: number; }) {
  const res = await api.post('/plans/meal', data);
  return res.data;
}