import React, { useEffect, useState } from 'react';
import { View, ScrollView } from 'react-native';
import { Appbar, SegmentedButtons, List, FAB, Dialog, Portal, Button, TextInput } from 'react-native-paper';
import { getMealPlans, getWorkoutPlans, createMealPlan, createWorkoutPlan } from '@/services/plans';

export default function PlansScreen({ route, navigation }: any) {
  const member = route.params?.member;
  const [type, setType] = useState<'workout' | 'meal'>('workout');
  const [workouts, setWorkouts] = useState<any[]>([]);
  const [meals, setMeals] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [name, setName] = useState('');
  const [details, setDetails] = useState('');
  const [durationWeeks, setDurationWeeks] = useState('4');
  const [goal, setGoal] = useState('Weight Loss');

  const load = async () => {
    const [w, m] = await Promise.all([
      getWorkoutPlans(member.id),
      getMealPlans(member.id),
    ]);
    setWorkouts(w);
    setMeals(m);
  };

  useEffect(() => { load(); }, []);

  const onAdd = async () => {
    if (type === 'workout') {
      await createWorkoutPlan({ user_id: member.id, plan_name: name, plan_details: details, duration_weeks: Number(durationWeeks), created_by: member.id });
    } else {
      await createMealPlan({ user_id: member.id, meal_name: name, meal_details: details, goal, created_by: member.id });
    }
    setOpen(false);
    setName(''); setDetails('');
    load();
  };

  return (
    <View style={{ flex: 1 }}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content title="Plans" subtitle={member?.name} />
      </Appbar.Header>
      <SegmentedButtons
        value={type}
        onValueChange={(v: any) => setType(v)}
        buttons={[
          { value: 'workout', label: 'Workout' },
          { value: 'meal', label: 'Meal' },
        ]}
        style={{ margin: 12 }}
      />
      <ScrollView style={{ flex: 1 }}>
        {(type === 'workout' ? workouts : meals).map((p) => (
          <List.Item key={`${type}-${p.id}`} title={p.plan_name || p.meal_name} description={(p.plan_details || p.meal_details)} />
        ))}
      </ScrollView>
      <FAB icon="plus" style={{ position: 'absolute', right: 16, bottom: 16 }} onPress={() => setOpen(true)} />
      <Portal>
        <Dialog visible={open} onDismiss={() => setOpen(false)}>
          <Dialog.Title>Add {type === 'workout' ? 'Workout' : 'Meal'} Plan</Dialog.Title>
          <Dialog.Content>
            <TextInput label="Name" value={name} onChangeText={setName} style={{ marginBottom: 8 }} />
            <TextInput label="Details (JSON or text)" value={details} onChangeText={setDetails} multiline style={{ marginBottom: 8 }} />
            {type === 'workout' ? (
              <TextInput label="Duration Weeks" value={durationWeeks} onChangeText={setDurationWeeks} keyboardType="number-pad" />
            ) : (
              <TextInput label="Goal" value={goal} onChangeText={setGoal} />
            )}
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setOpen(false)}>Cancel</Button>
            <Button onPress={onAdd}>Save</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </View>
  );
}