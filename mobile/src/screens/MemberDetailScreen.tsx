import React from 'react';
import { View } from 'react-native';
import { Appbar, Text } from 'react-native-paper';

export default function MemberDetailScreen({ route, navigation }: any) {
  const { member } = route.params || {};
  return (
    <View style={{ flex: 1 }}>
      <Appbar.Header>
        <Appbar.BackAction onPress={() => navigation.goBack()} />
        <Appbar.Content title="Member" />
      </Appbar.Header>
      <View style={{ padding: 16 }}>
        {member ? (
          <>
            <Text variant="titleLarge">{member.name}</Text>
            <Text>{member.phone}</Text>
            <Text>{member.email}</Text>
            <Text>Status: {member.status}</Text>
          </>
        ) : (
          <Text>New member form coming soon.</Text>
        )}
      </View>
    </View>
  );
}