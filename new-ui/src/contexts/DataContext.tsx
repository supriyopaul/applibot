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

  // Fetch resumes from the backend whenever the user changes
  useEffect(() => {
    if (user) {
      fetch('http://0.0.0.0:9000/resumes/', {
        headers: {
          'token': user.token,
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error('Failed to fetch resumes');
          }
          return res.json();
        })
        .then((data) => {
          // Map backend resume fields to frontend structure
          const mappedResumes = data.map((item: any) => ({
            id: item.id.toString(),
            content: item.content,
            createdAt: new Date(item.created_at),
          }));
          setResumes(mappedResumes);
        })
        .catch((err) => {
          console.error(err);
          setResumes([]);
        });
    } else {
      setResumes([]);
    }
  }, [user]);

  // Fetch saved info from the backend whenever the user changes
  useEffect(() => {
    if (user) {
      fetch('http://0.0.0.0:9000/users/infos/', {
        headers: {
          'token': user.token,
        },
      })
        .then((res) => {
          if (!res.ok) {
            throw new Error('Failed to fetch info');
          }
          return res.json();
        })
        .then((data) => {
          // Assume each info record has fields: id, text, created_at
          const mappedInfo = data.map((item: any) => ({
            id: item.id,
            content: item.text,
            createdAt: item.created_at ? new Date(item.created_at) : new Date(),
          }));
          setSavedInfo(mappedInfo);
        })
        .catch((err) => {
          console.error(err);
          setSavedInfo([]);
        });
    } else {
      setSavedInfo([]);
    }
  }, [user]);

  const addResume = async (content: string) => {
    if (!user) return;
    try {
      const response = await fetch('http://0.0.0.0:9000/resume/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'token': user.token,
        },
        body: new URLSearchParams({
          resume_content: content,
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to add resume');
      }
      const data = await response.json();
      const newResume: Resume = {
        id: data.id.toString(),
        content: data.content,
        createdAt: new Date(data.created_at),
      };
      setResumes((prev) => [newResume, ...prev]);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteResume = async (id: string) => {
    if (!user) return;
    try {
      const response = await fetch("http://0.0.0.0:9000/resume/?resume_id=" + id, {
        method: 'DELETE',
        headers: {
          'token': user.token,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete resume');
      }
      setResumes((prev) => prev.filter((resume) => resume.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  const addSavedInfo = async (content: string) => {
    if (!user) return;
    try {
      const response = await fetch('http://0.0.0.0:9000/info/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'token': user.token,
        },
        body: new URLSearchParams({
          info_text: content,
        }),
      });
      if (!response.ok) {
        throw new Error('Failed to add info');
      }
      const data = await response.json();
      const newInfo: SavedInfo = {
        id: data.id, // assuming backend returns the info record with an "id"
        content: data.text, // and "text" contains the formatted info
        createdAt: data.created_at ? new Date(data.created_at) : new Date(),
      };
      setSavedInfo((prev) => [newInfo, ...prev]);
    } catch (err) {
      console.error(err);
    }
  };

  const deleteSavedInfo = async (id: string) => {
    if (!user) return;
    try {
      const response = await fetch("http://0.0.0.0:9000/info/?info_id=" + id, {
        method: 'DELETE',
        headers: {
          'token': user.token,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to delete info');
      }
      setSavedInfo((prev) => prev.filter((info) => info.id !== id));
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <DataContext.Provider value={{ 
      resumes, 
      savedInfo, 
      addResume, 
      deleteResume, 
      addSavedInfo, 
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
