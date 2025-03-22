import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import { DataProvider } from './contexts/DataContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import HomePage from './pages/HomePage';
import AboutPage from './pages/AboutPage';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import ResumeManagementPage from './pages/ResumeManagementPage';
import InfoManagementPage from './pages/InfoManagementPage';
import AccountPage from './pages/AccountPage';
import GeneratePage from './pages/GeneratePage';
import ForgotPasswordPage from './pages/ForgotPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import { Instagram, Github, Linkedin } from 'lucide-react';

function App() {
  return (
    <AuthProvider>
      <DataProvider>
        <Router>
          <div className="min-h-screen bg-gray-50 flex flex-col">
            <Navbar />
            <main className="flex-grow">
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/forgot-password" element={<ForgotPasswordPage />} />
                <Route path="/reset-password" element={<ResetPasswordPage />} />
                <Route 
                  path="/resume-management" 
                  element={
                    <ProtectedRoute>
                      <ResumeManagementPage />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/info-management" 
                  element={
                    <ProtectedRoute>
                      <InfoManagementPage />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/generate" 
                  element={
                    <ProtectedRoute>
                      <GeneratePage />
                    </ProtectedRoute>
                  } 
                />
                <Route 
                  path="/account" 
                  element={
                    <ProtectedRoute>
                      <AccountPage />
                    </ProtectedRoute>
                  } 
                />
              </Routes>
            </main>
            <footer className="bg-gray-800 text-white py-3">
              <div className="container mx-auto px-4 text-center">
                <div className="flex justify-center space-x-10">
                  <a 
                    href="https://www.instagram.com/the_same_supriyo/" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="hover:text-gray-400"
                  >
                    <Instagram size={20} />
                  </a>
                  <a 
                    href="https://github.com/supriyopaul" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="hover:text-gray-400"
                  >
                    <Github size={20} />
                  </a>
                  <a 
                    href="https://www.linkedin.com/in/supriyopaul95/" 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    className="hover:text-gray-400"
                  >
                    <Linkedin size={20} />
                  </a>
                </div>
              </div>
            </footer>
          </div>
        </Router>
      </DataProvider>
    </AuthProvider>
  );
}

export default App;
