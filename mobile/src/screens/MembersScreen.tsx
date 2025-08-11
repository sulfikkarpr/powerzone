import React, { useEffect, useState } from 'react';
import { FlatList, View } from 'react-native';
import { Appbar, List, FAB } from 'react-native-paper';
import { api } from '@/services/api';

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

  const load = async () => {
    const res = await api.get<Member[]>('/users', { params: { status: 'active' } });
    setMembers(res.data.filter(m => m.role === 'member'));
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
          />
        )}
      />
      <FAB icon="plus" style={{ position: 'absolute', bottom: 16, right: 16 }} onPress={() => navigation.navigate('MemberDetail', { member: null })} />
    </View>
  );
}