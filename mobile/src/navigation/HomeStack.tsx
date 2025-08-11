import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import MembersScreen from '@/screens/MembersScreen';
import MemberDetailScreen from '@/screens/MemberDetailScreen';
import PlansScreen from '@/screens/PlansScreen';
import ProgressScreen from '@/screens/ProgressScreen';
import PaymentsScreen from '@/screens/PaymentsScreen';

const Stack = createNativeStackNavigator();

export default function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Members" component={MembersScreen} />
      <Stack.Screen name="MemberDetail" component={MemberDetailScreen} />
      <Stack.Screen name="Plans" component={PlansScreen} />
      <Stack.Screen name="Progress" component={ProgressScreen} />
      <Stack.Screen name="Payments" component={PaymentsScreen} />
    </Stack.Navigator>
  );
}