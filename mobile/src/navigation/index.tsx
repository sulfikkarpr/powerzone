import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import LoginScreen from '@/screens/LoginScreen';
import MembersScreen from '@/screens/MembersScreen';
import MemberDetailScreen from '@/screens/MemberDetailScreen';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';

const Stack = createNativeStackNavigator();

export default function RootNavigator() {
  const token = useSelector((s: RootState) => s.auth.token);

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {token ? (
          <>
            <Stack.Screen name="Members" component={MembersScreen} />
            <Stack.Screen name="MemberDetail" component={MemberDetailScreen} />
          </>
        ) : (
          <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}