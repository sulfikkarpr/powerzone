import React, { useEffect, useState } from 'react';
import { FlatList, View } from 'react-native';
import { Appbar, List, FAB, Menu } from 'react-native-paper';
import { api } from '@/services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface Member {
  id: number;
  name: string;
  phone: string;
  email: string;
  role: string;
  status: string;
}

export default function MembersScreen({ navigation }: any) {
  const [members, setMembers] = useState<Member[]>([]);
  const [menuVisible, setMenuVisible] = useState<number | null>(null);

  const load = async () => {
    try {
      const res = await api.get<Member[]>('/users', { params: { status: 'active' } });
      const data = res.data.filter(m => m.role === 'member');
      setMembers(data);
      await AsyncStorage.setItem('cache:members', JSON.stringify(data));
    } catch (e) {
      const cached = await AsyncStorage.getItem('cache:members');
      if (cached) setMembers(JSON.parse(cached));
    }
  };

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', load);
    load();
    return unsubscribe;
  }, [navigation]);

  return (
    <View style={{ flex: 1 }}>
      <Appbar.Header>
        <Appbar.Content title="Members" />
      </Appbar.Header>
      <FlatList
        data={members}
        keyExtractor={(item) => item.id.toString()}
        renderItem={({ item }) => (
          <List.Item
            title={item.name}
            description={`${item.phone} • ${item.email}`}
            onPress={() => navigation.navigate('MemberDetail', { member: item })}
            right={() => (
              <Menu
                visible={menuVisible === item.id}
                onDismiss={() => setMenuVisible(null)}
                anchor={<List.Icon icon="dots-vertical" onPress={() => setMenuVisible(item.id)} />}
              >
                <Menu.Item onPress={() => { setMenuVisible(null); navigation.navigate('Plans', { member: item }); }} title="Plans" />
                <Menu.Item onPress={() => { setMenuVisible(null); navigation.navigate('Progress', { member: item }); }} title="Progress" />
                <Menu.Item onPress={() => { setMenuVisible(null); navigation.navigate('Payments', { member: item }); }} title="Payments" />
              </Menu>
            )}
          />
        )}
      />
      <FAB icon="plus" style={{ position: 'absolute', bottom: 16, right: 16 }} onPress={() => navigation.navigate('MemberDetail', { member: null })} />
    </View>
  );
}