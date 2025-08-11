import React, { useEffect, useState } from 'react';
import { View, FlatList } from 'react-native';
import { Appbar, FAB, List, Dialog, Portal, Button, TextInput, Snackbar } from 'react-native-paper';
import { getReminders, createReminder, markPaid } from '@/services/payments';
import { sendMessage } from '@/services/messaging';

export default function PaymentsScreen({ route, navigation }: any) {
  const member = route.params?.member;
  const [items, setItems] = useState<any[]>([]);
  const [open, setOpen] = useState(false);
  const [amount, setAmount] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [snack, setSnack] = useState<string | null>(null);

  const load = async () => {
    const data = await getReminders(member.id);
    setItems(data);
  };

  useEffect(() => { load(); }, []);

  const onAdd = async () => {
    await createReminder({ user_id: member.id, amount: Number(amount), due_date: dueDate });
    setOpen(false); setAmount(''); setDueDate('');
    load();
  };

  const onPaid = async (id: number) => {
    await markPaid(id);
    load();
  };

  const onSendWhatsApp = async (rem: any) => {
    const msg = `Hi ${member.name}, please complete your payment of Rs ${rem.amount}. UPI: ${rem.upi_link}`;
    try {
      await sendMessage(member.phone, msg);
      setSnack('Message sent');
    } catch (e: any) {
      setSnack('Failed to send');
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content title="Payments" subtitle={member?.name} />
      </Appbar.Header>
      <FlatList
        data={items}
        keyExtractor={(i) => i.id.toString()}
        renderItem={({ item }) => (
          <List.Item
            title={`Rs ${item.amount} • ${item.status}`}
            description={`${item.due_date}  ${item.upi_link ? 'UPI available' : ''}`}
            right={(props) => (
              <View style={{ flexDirection: 'row', alignItems: 'center' }}>
                <Button onPress={() => onSendWhatsApp(item)}>WhatsApp</Button>
                {item.status !== 'paid' && <Button onPress={() => onPaid(item.id)}>Mark Paid</Button>}
              </View>
            )}
          />
        )}
      />
      <FAB icon="plus" style={{ position: 'absolute', right: 16, bottom: 16 }} onPress={() => setOpen(true)} />
      <Portal>
        <Dialog visible={open} onDismiss={() => setOpen(false)}>
          <Dialog.Title>Add Reminder</Dialog.Title>
          <Dialog.Content>
            <TextInput label="Amount (Rs)" value={amount} onChangeText={setAmount} keyboardType="decimal-pad" style={{ marginBottom: 8 }} />
            <TextInput label="Due Date (YYYY-MM-DD)" value={dueDate} onChangeText={setDueDate} />
          </Dialog.Content>
          <Dialog.Actions>
            <Button onPress={() => setOpen(false)}>Cancel</Button>
            <Button onPress={onAdd}>Save</Button>
          </Dialog.Actions>
        </Dialog>
      </Portal>
      <Snackbar visible={!!snack} onDismiss={() => setSnack(null)} duration={2000}>{snack}</Snackbar>
    </View>
  );
}