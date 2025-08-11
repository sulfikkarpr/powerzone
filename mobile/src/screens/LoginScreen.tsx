import React, { useState } from 'react';
import { View } from 'react-native';
import { TextInput, Button, Text, ActivityIndicator } from 'react-native-paper';
import { useAppDispatch } from '@/store';
import { loginThunk } from '@/store/slices/authSlice';

export default function LoginScreen() {
  const dispatch = useAppDispatch();
  const [email, setEmail] = useState('admin@example.com');
  const [password, setPassword] = useState('ChangeMe123');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onLogin = async () => {
    try {
      setLoading(true);
      setError(null);
      await dispatch(loginThunk({ email, password })).unwrap();
    } catch (e: any) {
      setError(e?.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', padding: 16 }}>
      <Text variant="headlineMedium" style={{ marginBottom: 16 }}>Powerzone Admin</Text>
      <TextInput label="Email" value={email} onChangeText={setEmail} autoCapitalize="none" keyboardType="email-address" style={{ marginBottom: 12 }} />
      <TextInput label="Password" value={password} onChangeText={setPassword} secureTextEntry style={{ marginBottom: 12 }} />
      {error && <Text style={{ color: 'red', marginBottom: 12 }}>{error}</Text>}
      <Button mode="contained" onPress={onLogin} disabled={loading}>
        {loading ? <ActivityIndicator animating /> : 'Login'}
      </Button>
    </View>
  );
}