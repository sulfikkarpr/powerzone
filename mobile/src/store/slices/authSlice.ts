import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { api } from '@/services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  token: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: AuthState = {
  token: null,
  loading: false,
  error: null,
};

export const loginThunk = createAsyncThunk(
  'auth/login',
  async (payload: { email: string; password: string }) => {
    const res = await api.post('/auth/login', payload);
    return res.data.access_token as string;
  }
);

const slice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    setToken(state, action) {
      state.token = action.payload;
    },
    logout(state) {
      state.token = null;
      AsyncStorage.removeItem('authToken');
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loginThunk.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginThunk.fulfilled, (state, action) => {
        state.loading = false;
        state.token = action.payload;
        AsyncStorage.setItem('authToken', action.payload);
      })
      .addCase(loginThunk.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Login failed';
      });
  },
});

export const { setToken, logout } = slice.actions;
export default slice.reducer;