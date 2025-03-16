import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Key, User } from 'lucide-react';

const AccountPage: React.FC = () => {
  const { user, updateCredentials, updateApiKey } = useAuth();
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmNewPassword, setConfirmNewPassword] = useState('');
  const [apiKey, setApiKey] = useState(user?.apiKey || '');
  const [credentialsError, setCredentialsError] = useState('');
  const [credentialsSuccess, setCredentialsSuccess] = useState('');
  const [apiKeySuccess, setApiKeySuccess] = useState('');

  const handleUpdateCredentials = (e: React.FormEvent) => {
    e.preventDefault();
    setCredentialsError('');
    setCredentialsSuccess('');
    
    if (!currentPassword || !newPassword || !confirmNewPassword) {
      setCredentialsError('Please fill in all fields');
      return;
    }
    
    if (newPassword !== confirmNewPassword) {
      setCredentialsError('New passwords do not match');
      return;
    }
    
    const success = updateCredentials(user?.email || '', currentPassword, newPassword);
    
    if (success) {
      setCredentialsSuccess('Credentials updated successfully');
      setCurrentPassword('');
      setNewPassword('');
      setConfirmNewPassword('');
    } else {
      setCredentialsError('Current password is incorrect');
    }
  };

  const handleUpdateApiKey = (e: React.FormEvent) => {
    e.preventDefault();
    setApiKeySuccess('');
    
    const success = updateApiKey(apiKey);
    
    if (success) {
      setApiKeySuccess('API key updated successfully');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-8">Account Settings</h1>
          
          <div className="bg-white rounded-xl shadow-md overflow-hidden mb-8">
            <div className="p-8">
              <div className="flex items-center mb-6">
                <User size={24} className="text-indigo-600 mr-2" />
                <h2 className="text-xl font-semibold text-gray-800">Update Credentials</h2>
              </div>
              
              {credentialsError && (
                <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-4">
                  <p className="text-red-700">{credentialsError}</p>
                </div>
              )}
              
              {credentialsSuccess && (
                <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
                  <p className="text-green-700">{credentialsSuccess}</p>
                </div>
              )}
              
              <form onSubmit={handleUpdateCredentials} className="space-y-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                    Email
                  </label>
                  <input
                    type="email"
                    id="email"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 bg-gray-100"
                    value={user?.email || ''}
                    disabled
                  />
                </div>
                
                <div>
                  <label htmlFor="current-password" className="block text-sm font-medium text-gray-700 mb-1">
                    Current Password
                  </label>
                  <input
                    type="password"
                    id="current-password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                  />
                </div>
                
                <div>
                  <label htmlFor="new-password" className="block text-sm font-medium text-gray-700 mb-1">
                    New Password
                  </label>
                  <input
                    type="password"
                    id="new-password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                  />
                </div>
                
                <div>
                  <label htmlFor="confirm-new-password" className="block text-sm font-medium text-gray-700 mb-1">
                    Confirm New Password
                  </label>
                  <input
                    type="password"
                    id="confirm-new-password"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    value={confirmNewPassword}
                    onChange={(e) => setConfirmNewPassword(e.target.value)}
                  />
                </div>
                
                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Update Credentials
                  </button>
                </div>
              </form>
            </div>
          </div>
          
          <div className="bg-white rounded-xl shadow-md overflow-hidden">
            <div className="p-8">
              <div className="flex items-center mb-6">
                <Key size={24} className="text-indigo-600 mr-2" />
                <h2 className="text-xl font-semibold text-gray-800">OpenAI API Key</h2>
              </div>
              
              {apiKeySuccess && (
                <div className="bg-green-50 border-l-4 border-green-400 p-4 mb-4">
                  <p className="text-green-700">{apiKeySuccess}</p>
                </div>
              )}
              
              <div className="mb-4">
                <p className="text-gray-600 mb-4">
                  To use the advanced features of Applibot, you need to provide your OpenAI API key with GPT-4 access.
                </p>
                <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-4">
                  <p className="text-yellow-700">
                    <strong>Note:</strong> Your API key is stored securely in your browser's local storage. We never send your API key to our servers.
                  </p>
                </div>
              </div>
              
              <form onSubmit={handleUpdateApiKey} className="space-y-4">
                <div>
                  <label htmlFor="api-key" className="block text-sm font-medium text-gray-700 mb-1">
                    OpenAI API Key
                  </label>
                  <input
                    type="password"
                    id="api-key"
                    className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                    placeholder="sk-..."
                    value={apiKey}
                    onChange={(e) => setApiKey(e.target.value)}
                  />
                </div>
                
                <div className="flex justify-end">
                  <button
                    type="submit"
                    className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Save API Key
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountPage;