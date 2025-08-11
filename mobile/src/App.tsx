import React from 'react';
import { Provider as ReduxProvider } from 'react-redux';
import { store } from '@/store';
import RootNavigator from '@/navigation';
import { Provider as PaperProvider, MD3LightTheme } from 'react-native-paper';
import { StatusBar } from 'expo-status-bar';

export default function App() {
  return (
    <ReduxProvider store={store}>
      <PaperProvider theme={MD3LightTheme}>
        <StatusBar style="auto" />
        <RootNavigator />
      </PaperProvider>
    </ReduxProvider>
  );
}