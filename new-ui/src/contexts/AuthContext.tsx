import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { User, AuthContextType } from '../types';

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const login = (email: string, password: string) => {
    // In a real app, you would validate against a backend
    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]');
    const foundUser = storedUsers.find(
      (u: User) => u.email === email && u.password === password
    );

    if (foundUser) {
      setUser(foundUser);
      localStorage.setItem('user', JSON.stringify(foundUser));
      return true;
    }
    return false;
  };

  const signup = (email: string, password: string, confirmPassword: string) => {
    if (password !== confirmPassword) {
      return false;
    }

    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]');
    const userExists = storedUsers.some((u: User) => u.email === email);

    if (userExists) {
      return false;
    }

    const newUser = { email, password };
    const updatedUsers = [...storedUsers, newUser];
    
    localStorage.setItem('users', JSON.stringify(updatedUsers));
    setUser(newUser);
    localStorage.setItem('user', JSON.stringify(newUser));
    return true;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const updateCredentials = (email: string, password: string, newPassword: string) => {
    if (!user) return false;

    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]');
    const userIndex = storedUsers.findIndex(
      (u: User) => u.email === user.email && u.password === password
    );

    if (userIndex === -1) return false;

    const updatedUser = { ...storedUsers[userIndex], email, password: newPassword };
    storedUsers[userIndex] = updatedUser;
    
    localStorage.setItem('users', JSON.stringify(storedUsers));
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
    return true;
  };

  const updateApiKey = (apiKey: string) => {
    if (!user) return false;

    const updatedUser = { ...user, apiKey };
    
    const storedUsers = JSON.parse(localStorage.getItem('users') || '[]');
    const userIndex = storedUsers.findIndex((u: User) => u.email === user.email);
    
    if (userIndex !== -1) {
      storedUsers[userIndex] = updatedUser;
      localStorage.setItem('users', JSON.stringify(storedUsers));
    }
    
    setUser(updatedUser);
    localStorage.setItem('user', JSON.stringify(updatedUser));
    return true;
  };

  return (
    <AuthContext.Provider value={{ user, login, signup, logout, updateCredentials, updateApiKey }}>
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