import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthContextType } from '../types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  // On mount, load user from localStorage (including token if available)
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  useEffect(() => {
    const fetchApiKey = async () => {
      if (user && !user.apiKey) {
        try {
          const response = await fetch('http://0.0.0.0:9000/get_openai_key/', {
            headers: {
              'token': user.token,
            },
          });
          if (response.ok) {
            const data = await response.json();
            const updatedUser = { ...user, apiKey: data.openai_api_key };
            setUser(updatedUser);
            localStorage.setItem('user', JSON.stringify(updatedUser));
          }
        } catch (err) {
          console.error("Error fetching API key:", err);
        }
      }
    };
    fetchApiKey();
  }, [user]);

  const login = async (email: string, password: string) => {
    try {
      const response = await fetch('http://0.0.0.0:9000/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });
      if (!response.ok) throw new Error('Login failed');
      const data = await response.json();
      const newUser = { email, token: data.access_token, apiKey: null, password };
      setUser(newUser);
      localStorage.setItem('user', JSON.stringify(newUser));
      return true;
    } catch (err) {
      return false;
    }
  };

  const signup = async (email: string, password: string, confirmPassword: string) => {
    if (password !== confirmPassword) {
      return false;
    }
    try {
      const response = await fetch('http://0.0.0.0:9000/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });
      if (!response.ok) throw new Error('Signup failed');
      return await login(email, password);
    } catch (err) {
      return false;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const updateCredentials = async (email: string, currentPassword: string, newPassword: string) => {
    if (!user || !user.token) return false;
    try {
      const response = await fetch('http://0.0.0.0:9000/update_credentials', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'token': user.token,
        },
        body: new URLSearchParams({
          current_password: currentPassword,
          new_password: newPassword,
        }),
      });
      if (!response.ok) throw new Error('Failed to update credentials');
      const updatedUser = { ...user, password: newPassword };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      return true;
    } catch (err) {
      return false;
    }
  };

  const updateApiKey = async (apiKey: string) => {
    if (!user || !user.token) return false;
    try {
      const response = await fetch('http://0.0.0.0:9000/update_openai_key', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'token': user.token,
        },
        body: new URLSearchParams({
          new_openai_key: apiKey,
        }),
      });
      if (!response.ok) throw new Error('Failed to update API key');
      const updatedUser = { ...user, apiKey };
      setUser(updatedUser);
      localStorage.setItem('user', JSON.stringify(updatedUser));
      return true;
    } catch (err) {
      return false;
    }
  };

  const forgotPassword = async (email: string) => {
    try {
      const response = await fetch('http://0.0.0.0:9000/forgot_password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          email: email,
        }),
      });
      if (!response.ok) throw new Error('Failed to initiate password reset');
      const data = await response.json();
      return data;
    } catch (err) {
      return false;
    }
  };

  const resetPassword = async (token: string, newPassword: string, confirmPassword: string) => {
    try {
      const response = await fetch('http://0.0.0.0:9000/reset_password', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          token: token,
          new_password: newPassword,
          confirm_password: confirmPassword,
        }),
      });
      if (!response.ok) throw new Error('Failed to reset password');
      const data = await response.json();
      return data;
    } catch (err) {
      return false;
    }
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, updateCredentials, updateApiKey, forgotPassword, resetPassword }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = React.useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
