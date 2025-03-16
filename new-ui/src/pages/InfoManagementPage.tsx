import React, { useState } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { useData } from '../contexts/DataContext';
import { Clipboard, Trash2, Edit } from 'lucide-react';
import 'react-tabs/style/react-tabs.css';

const InfoManagementPage: React.FC = () => {
  const [infoToFormat, setInfoToFormat] = useState('');
  const [formattedInfo, setFormattedInfo] = useState('');
  const [infoToSave, setInfoToSave] = useState('');
  const [editingInfo, setEditingInfo] = useState<{ id: string; content: string } | null>(null);
  const { savedInfo, addSavedInfo, updateSavedInfo, deleteSavedInfo } = useData();

  const handleFormatInfo = () => {
    if (infoToFormat.trim()) {
      // Simple formatting for demonstration
      // In a real app, this would use the OpenAI API
      const formatted = infoToFormat
        .split('\n')
        .filter(line => line.trim())
        .map(line => line.trim())
        .join('\n\n');
      
      setFormattedInfo(formatted);
    }
  };

  const handleSaveInfo = () => {
    if (infoToSave.trim()) {
      addSavedInfo(infoToSave);
      setInfoToSave('');
    }
  };

  const handleUpdateInfo = () => {
    if (editingInfo && editingInfo.content.trim()) {
      updateSavedInfo(editingInfo.id, editingInfo.content);
      setEditingInfo(null);
    }
  };

  const handleCopyToClipboard = () => {
    navigator.clipboard.writeText(formattedInfo);
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">Information Management</h1>
            
            <Tabs className="mb-4">
              <TabList className="flex border-b border-gray-200 mb-6 overflow-x-auto">
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Format Information
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Save Information
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Manage Saved Info
                </Tab>
              </TabList>
              
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="info-to-format" className="block text-sm font-medium text-gray-700 mb-1">
                      Enter information to format
                    </label>
                    <textarea
                      id="info-to-format"
                      rows={8}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste or type your information here..."
                      value={infoToFormat}
                      onChange={(e) => setInfoToFormat(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={handleFormatInfo}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Format
                    </button>
                  </div>
                  
                  {formattedInfo && (
                    <div className="mt-6">
                      <div className="flex justify-between items-center mb-2">
                        <label className="block text-sm font-medium text-gray-700">
                          Formatted Output
                        </label>
                        <button
                          onClick={handleCopyToClipboard}
                          className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm"
                        >
                          <Clipboard size={16} className="mr-1" />
                          Copy to Clipboard
                        </button>
                      </div>
                      <div className="relative">
                        <textarea
                          rows={8}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                          value={formattedInfo}
                          onChange={(e) => setFormattedInfo(e.target.value)}
                        ></textarea>
                      </div>
                    </div>
                  )}
                </div>
              </TabPanel>
              
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="info-to-save" className="block text-sm font-medium text-gray-700 mb-1">
                      Enter information to save
                    </label>
                    <textarea
                      id="info-to-save"
                      rows={10}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste or type your information here..."
                      value={infoToSave}
                      onChange={(e) => setInfoToSave(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={handleSaveInfo}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Save
                    </button>
                  </div>
                </div>
              </TabPanel>
              
              <TabPanel>
                {savedInfo.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    No information saved yet. Add your first information in the "Save Information" tab.
                  </div>
                ) : (
                  <div className="space-y-6">
                    {editingInfo ? (
                      <div className="border border-indigo-200 rounded-lg p-4 bg-indigo-50">
                        <div className="mb-2 text-sm font-medium text-indigo-700">
                          Editing Information
                        </div>
                        <textarea
                          rows={8}
                          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 mb-3"
                          value={editingInfo.content}
                          onChange={(e) => setEditingInfo({ ...editingInfo, content: e.target.value })}
                        ></textarea>
                        <div className="flex justify-end space-x-2">
                          <button
                            onClick={() => setEditingInfo(null)}
                            className="px-3 py-1 bg-gray-200 text-gray-800 rounded-md hover:bg-gray-300 focus:outline-none"
                          >
                            Cancel
                          </button>
                          <button
                            onClick={handleUpdateInfo}
                            className="px-3 py-1 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none"
                          >
                            Save Changes
                          </button>
                        </div>
                      </div>
                    ) : (
                      savedInfo.map((info) => (
                        <div key={info.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                          <div className="flex justify-between items-start mb-2">
                            <div className="text-sm text-gray-500">
                              Created: {formatDate(info.createdAt)}
                            </div>
                            <div className="flex space-x-2">
                              <button
                                onClick={() => setEditingInfo({ id: info.id, content: info.content })}
                                className="text-indigo-500 hover:text-indigo-700 focus:outline-none"
                                aria-label="Edit information"
                              >
                                <Edit size={18} />
                              </button>
                              <button
                                onClick={() => deleteSavedInfo(info.id)}
                                className="text-red-500 hover:text-red-700 focus:outline-none"
                                aria-label="Delete information"
                              >
                                <Trash2 size={18} />
                              </button>
                            </div>
                          </div>
                          <div className="whitespace-pre-wrap bg-gray-50 p-3 rounded border border-gray-100 text-gray-800 max-h-60 overflow-y-auto">
                            {info.content}
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                )}
              </TabPanel>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  );
};

export default InfoManagementPage;