import React, { createContext, useState, useEffect, ReactNode } from 'react';
import { Resume, SavedInfo, DataContextType } from '../types';
import { useAuth } from './AuthContext';

const DataContext = createContext<DataContextType | undefined>(undefined);

interface DataProviderProps {
  children: ReactNode;
}

export const DataProvider: React.FC<DataProviderProps> = ({ children }) => {
  const { user } = useAuth();
  const [resumes, setResumes] = useState<Resume[]>([]);
  const [savedInfo, setSavedInfo] = useState<SavedInfo[]>([]);

  // Load data when user changes
  useEffect(() => {
    if (user) {
      const userResumes = JSON.parse(localStorage.getItem(`resumes_${user.email}`) || '[]');
      const userSavedInfo = JSON.parse(localStorage.getItem(`savedInfo_${user.email}`) || '[]');
      
      setResumes(userResumes);
      setSavedInfo(userSavedInfo);
    } else {
      setResumes([]);
      setSavedInfo([]);
    }
  }, [user]);

  const addResume = (content: string) => {
    if (!user) return;
    
    const newResume: Resume = {
      id: Date.now().toString(),
      content,
      createdAt: new Date(),
    };
    
    const updatedResumes = [newResume, ...resumes];
    setResumes(updatedResumes);
    localStorage.setItem(`resumes_${user.email}`, JSON.stringify(updatedResumes));
  };

  const deleteResume = (id: string) => {
    if (!user) return;
    
    const updatedResumes = resumes.filter(resume => resume.id !== id);
    setResumes(updatedResumes);
    localStorage.setItem(`resumes_${user.email}`, JSON.stringify(updatedResumes));
  };

  const addSavedInfo = (content: string) => {
    if (!user) return;
    
    const newInfo: SavedInfo = {
      id: Date.now().toString(),
      content,
      createdAt: new Date(),
    };
    
    const updatedInfo = [newInfo, ...savedInfo];
    setSavedInfo(updatedInfo);
    localStorage.setItem(`savedInfo_${user.email}`, JSON.stringify(updatedInfo));
  };

  const updateSavedInfo = (id: string, content: string) => {
    if (!user) return;
    
    const updatedInfo = savedInfo.map(info => 
      info.id === id ? { ...info, content } : info
    );
    
    setSavedInfo(updatedInfo);
    localStorage.setItem(`savedInfo_${user.email}`, JSON.stringify(updatedInfo));
  };

  const deleteSavedInfo = (id: string) => {
    if (!user) return;
    
    const updatedInfo = savedInfo.filter(info => info.id !== id);
    setSavedInfo(updatedInfo);
    localStorage.setItem(`savedInfo_${user.email}`, JSON.stringify(updatedInfo));
  };

  return (
    <DataContext.Provider value={{ 
      resumes, 
      savedInfo, 
      addResume, 
      deleteResume, 
      addSavedInfo, 
      updateSavedInfo, 
      deleteSavedInfo 
    }}>
      {children}
    </DataContext.Provider>
  );
};

export const useData = () => {
  const context = React.useContext(DataContext);
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider');
  }
  return context;
};