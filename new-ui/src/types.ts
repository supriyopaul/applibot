export interface User {
  email: string;
  password: string;
  apiKey?: string;
}

export interface Resume {
  id: string;
  content: string;
  createdAt: Date;
}

export interface SavedInfo {
  id: string;
  content: string;
  createdAt: Date;
}

export interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => void;
  signup: (email: string, password: string, confirmPassword: string) => void;
  logout: () => void;
  updateCredentials: (email: string, password: string, newPassword: string) => void;
  updateApiKey: (apiKey: string) => void;
}

export interface DataContextType {
  resumes: Resume[];
  savedInfo: SavedInfo[];
  addResume: (content: string) => void;
  deleteResume: (id: string) => void;
  addSavedInfo: (content: string) => void;
  updateSavedInfo: (id: string, content: string) => void;
  deleteSavedInfo: (id: string) => void;
}