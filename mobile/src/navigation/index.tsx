import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import LoginScreen from '@/screens/LoginScreen';
import HomeStack from '@/navigation/HomeStack';
import AnalyticsScreen from '@/screens/AnalyticsScreen';
import { useSelector } from 'react-redux';
import { RootState } from '@/store';
import { MaterialIcons } from '@expo/vector-icons';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function AuthedTabs() {
  return (
    <Tab.Navigator>
      <Tab.Screen
        name="Home"
        component={HomeStack}
        options={{ headerShown: false, tabBarIcon: ({ color, size }) => (<MaterialIcons name="group" color={color} size={size} />) }}
      />
      <Tab.Screen
        name="Analytics"
        component={AnalyticsScreen}
        options={{ tabBarIcon: ({ color, size }) => (<MaterialIcons name="insights" color={color} size={size} />) }}
      />
    </Tab.Navigator>
  );
}

export default function RootNavigator() {
  const token = useSelector((s: RootState) => s.auth.token);

  return (
    <NavigationContainer>
      <Stack.Navigator>
        {token ? (
          <Stack.Screen name="App" component={AuthedTabs} options={{ headerShown: false }} />
        ) : (
          <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}