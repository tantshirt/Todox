'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import type { User, AuthResponse } from '@/types/auth';
import * as api from './api';

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

async function fetchCurrentUser(token: string): Promise<User> {
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'}/auth/me`, {
    headers: {
      'Authorization': `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error('Failed to fetch user');
  }

  return response.json();
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check for stored token on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchCurrentUser(token)
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('access_token');
        })
        .finally(() => setIsLoading(false));
    } else {
      setIsLoading(false);
    }
  }, []);

  const login = async (email: string, password: string) => {
    const response: AuthResponse = await api.login(email, password);
    
    // Storing JWT in localStorage for MVP simplicity.
    // Production consideration: Use httpOnly cookies to prevent XSS attacks.
    localStorage.setItem('access_token', response.access_token);
    
    const user = await fetchCurrentUser(response.access_token);
    setUser(user);
    toast.success('Login successful!');
    router.push('/tasks');
  };

  const register = async (email: string, password: string) => {
    await api.register(email, password);
    toast.success('Registration successful! Please log in.');
    router.push('/auth/login');
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
    toast.success('Logged out successfully');
    router.push('/auth/login');
  };

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
}
