import React, { useState } from 'react';
import { useData } from '../contexts/DataContext';
import { useAuth } from '../contexts/AuthContext';
import { Clipboard } from 'lucide-react';

const InfoManagementPage: React.FC = () => {
  const { user } = useAuth();
  const { savedInfo, addSavedInfo, deleteSavedInfo } = useData();
  const [infoText, setInfoText] = useState('');
  const [error, setError] = useState('');
  const [formattedInfo, setFormattedInfo] = useState('');

  // Block access if API key is not set
  if (!user?.apiKey) {
    return (
      <div className="min-h-screen flex justify-center items-center">
        <p className="text-xl text-red-500">
          Please update your OpenAI API key in the Account page to access Info Management.
        </p>
      </div>
    );
  }

  const handleFormatInfo = async () => {
    if (!infoText.trim()) {
      setError('Please enter info text');
      return;
    }
    setError('');
    try {
      const response = await fetch('http://0.0.0.0:9000/format-info/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          token: user?.token || '',
        },
        body: new URLSearchParams({
          unformatted_info_text: infoText,
        }),
      });
      if (!response.ok) throw new Error('Failed to format info');
      let data = await response.text();
      // If data is wrapped in quotes, remove them.
      if (data.startsWith('"') && data.endsWith('"')) {
        data = data.slice(1, -1);
      }
      // Replace literal "\n" with actual newlines.
      const processed = data.replace(/\\n/g, "\n");
      setFormattedInfo(processed);
    } catch (err) {
      console.error(err);
      setError('Error formatting info');
    }
  };

  const handleSaveInfo = async () => {
    if (!infoText.trim()) {
      setError('Please enter info text');
      return;
    }
    setError('');
    try {
      await addSavedInfo(infoText);
      setInfoText('');
    } catch (err) {
      console.error(err);
      setError('Error saving info');
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <h1 className="text-3xl font-bold text-gray-800 mb-8">Info Management</h1>
        {error && (
          <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
            <p className="text-red-700">{error}</p>
          </div>
        )}
        <div className="space-y-4">
          <label htmlFor="info-text" className="block text-sm font-medium text-gray-700">
            Enter Info Text
          </label>
          <textarea
            id="info-text"
            rows={6}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="Enter info text here..."
            value={infoText}
            onChange={(e) => setInfoText(e.target.value)}
          ></textarea>
          <div className="flex space-x-4">
            <button
              onClick={handleFormatInfo}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
            >
              Format Info
            </button>
            <button
              onClick={handleSaveInfo}
              className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
            >
              Save Info
            </button>
          </div>
          {formattedInfo && (
            <div className="mt-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-700">Formatted Info</span>
                <button
                  onClick={() => copyToClipboard(formattedInfo)}
                  className="text-indigo-600 hover:text-indigo-800"
                >
                  <Clipboard size={16} />
                </button>
              </div>
              <div className="p-4 border border-gray-200 rounded bg-gray-50 whitespace-pre-wrap">
                {formattedInfo}
              </div>
            </div>
          )}
        </div>
        <div className="mt-12">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">Saved Info</h2>
          {savedInfo.length === 0 ? (
            <div className="text-gray-500">No info saved yet.</div>
          ) : (
            savedInfo.map((info) => (
              <div key={info.id} className="border border-gray-200 rounded p-4 mb-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 text-sm">
                    {new Date(info.createdAt).toLocaleString()}
                  </span>
                  <button
                    onClick={() => deleteSavedInfo(info.id)}
                    className="text-red-500 hover:text-red-700"
                  >
                    Delete
                  </button>
                </div>
                <div className="mt-2 whitespace-pre-wrap">{info.content}</div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default InfoManagementPage;
