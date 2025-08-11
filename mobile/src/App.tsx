import React from 'react';
import { Provider as ReduxProvider } from 'react-redux';
import { store } from '@/store';
import RootNavigator from '@/navigation';
import { Provider as PaperProvider } from 'react-native-paper';
import { theme } from '@/theme';
import { StatusBar } from 'expo-status-bar';

export default function App() {
  return (
    <ReduxProvider store={store}>
      <PaperProvider theme={theme}>
        <StatusBar style="auto" />
        <RootNavigator />
      </PaperProvider>
    </ReduxProvider>
  );
}