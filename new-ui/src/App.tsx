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
            <footer className="bg-gray-800 text-white py-6">
              <div className="container mx-auto px-4 text-center">
                <p>&copy; {new Date().getFullYear()} Applibot. All rights reserved.</p>
                <p className="text-gray-400 text-sm mt-2">
                  Powered by Retrieval Augmented Generation (RAG) technology
                </p>
              </div>
            </footer>
          </div>
        </Router>
      </DataProvider>
    </AuthProvider>
  );
}

export default App;