import React, { useEffect, useState } from 'react';
import { View, FlatList } from 'react-native';
import { Appbar, FAB, List, Dialog, Portal, Button, TextInput } from 'react-native-paper';
import { getProgressLogs, createProgress, updateProgress, deleteProgress } from '@/services/progress';

export default function ProgressScreen({ route, navigation }: any) {
  const member = route.params?.member;
  const [logs, setLogs] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [editing, setEditing] = useState<any | null>(null);
  const [weight, setWeight] = useState('');
  const [bodyFat, setBodyFat] = useState('');
  const [bmi, setBmi] = useState('');

  const load = async () => {
    const data = await getProgressLogs(member.id);
    setLogs(data);
  };

  useEffect(() => { load(); }, []);

  const onSave = async () => {
    const payload = {
      user_id: member.id,
      weight: Number(weight),
      body_fat_percentage: Number(bodyFat),
      bmi: Number(bmi),
      log_date: new Date().toISOString(),
    };
    if (editing) {
      await updateProgress(editing.id, payload);
    } else {
      await createProgress(payload);
    }
    setOpen(false);
    setEditing(null);
    setWeight(''); setBodyFat(''); setBmi('');
    load();
  };

  const onEdit = (log: any) => {
    setEditing(log);
    setWeight(String(log.weight));
    setBodyFat(String(log.body_fat_percentage));
    setBmi(String(log.bmi));
    setOpen(true);
  };

  const onDelete = async (log: any) => {
    await deleteProgress(log.id);
    load();
  };

  return (
    <View style={{ flex: 1 }}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content title="Progress" subtitle={member?.name} />
      </Appbar.Header>
      <FlatList
        data={logs}
        keyExtractor={(i) => i.id.toString()}
        renderItem={({ item }) => (
          <List.Item
            title={`${item.weight} kg • BMI ${item.bmi}`}
            description={new Date(item.log_date).toLocaleString()}
            onPress={() => onEdit(item)}
            right={(props) => <Button onPress={() => onDelete(item)}>Delete</Button>}
          />
        )}
      />
      <FAB icon="plus" style={{ position: 'absolute', right: 16, bottom: 16 }} onPress={() => setOpen(true)} />
      <Portal>
        <Dialog visible={open} onDismiss={() => setOpen(false)}>
          <Dialog.Title>{editing ? 'Edit' : 'Add'} Progress</Dialog.Title>
          <Dialog.Content>
            <TextInput label="Weight (kg)" value={weight} onChangeText={setWeight} keyboardType="decimal-pad" style={{ marginBottom: 8 }} />
            <TextInput label="Body Fat %" value={bodyFat} onChangeText={setBodyFat} keyboardType="decimal-pad" style={{ marginBottom: 8 }} />
            <TextInput label="BMI" value={bmi} onChangeText={setBmi} keyboardType="decimal-pad" />
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setOpen(false)}>Cancel</Button>
            <Button onPress={onSave}>Save</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
    </View>
  );
}