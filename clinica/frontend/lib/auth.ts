import api from './api';
import Cookies from 'js-cookie';
import { LoginResponse, Usuario } from '@/types';

export const authService = {
  async login(username: string, password: string): Promise<LoginResponse> {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);

    const response = await api.post<LoginResponse>('/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });

    // Guardar token en cookie
    Cookies.set('token', response.data.access_token, { expires: 7 });

    // Obtener datos del usuario
    const userResponse = await api.get<Usuario>('/auth/me');
    Cookies.set('user', JSON.stringify(userResponse.data), { expires: 7 });

    return response.data;
  },

  async logout(): Promise<void> {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Error en logout:', error);
    } finally {
      Cookies.remove('token');
      Cookies.remove('user');
    }
  },

  async getCurrentUser(): Promise<Usuario | null> {
    try {
      const response = await api.get<Usuario>('/auth/me');
      return response.data;
    } catch (error) {
      return null;
    }
  },

  isAuthenticated(): boolean {
    return !!Cookies.get('token');
  },

  getUser(): Usuario | null {
    const userStr = Cookies.get('user');
    if (!userStr) return null;
    try {
      return JSON.parse(userStr);
    } catch {
      return null;
    }
  },
};