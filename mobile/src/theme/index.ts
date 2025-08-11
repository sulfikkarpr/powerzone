import { MD3LightTheme } from 'react-native-paper';
import Constants from 'expo-constants';

const primary = (Constants.expoConfig?.extra as any)?.PRIMARY_COLOR || '#1e90ff';

export const theme = {
  ...MD3LightTheme,
  colors: {
    ...MD3LightTheme.colors,
    primary,
  },
};