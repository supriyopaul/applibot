import React, { useState } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { useData } from '../contexts/DataContext';
import { Trash2 } from 'lucide-react';
import 'react-tabs/style/react-tabs.css';

const ResumeManagementPage: React.FC = () => {
  const [resumeContent, setResumeContent] = useState('');
  const { resumes, addResume, deleteResume } = useData();

  const handleSaveResume = () => {
    if (resumeContent.trim()) {
      addResume(resumeContent);
      setResumeContent('');
    }
  };

  const formatDate = (date: Date) => {
    return new Date(date).toLocaleString();
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">Resume Management</h1>
            
            <Tabs className="mb-4">
              <TabList className="flex border-b border-gray-200 mb-6">
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors">
                  Save a New Resume
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors">
                  View/Manage Resumes
                </Tab>
              </TabList>
              
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="resume-content" className="block text-sm font-medium text-gray-700 mb-1">
                      Enter your resume content
                    </label>
                    <textarea
                      id="resume-content"
                      rows={15}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste or type your resume here..."
                      value={resumeContent}
                      onChange={(e) => setResumeContent(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={handleSaveResume}
                      className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      Save Resume
                    </button>
                  </div>
                </div>
              </TabPanel>
              
              <TabPanel>
                {resumes.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    No resumes saved yet. Add your first resume in the "Save a New Resume" tab.
                  </div>
                ) : (
                  <div className="space-y-6">
                    {resumes.map((resume) => (
                      <div key={resume.id} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                        <div className="flex justify-between items-start mb-2">
                          <div className="text-sm text-gray-500">
                            Created: {formatDate(resume.createdAt)}
                          </div>
                          <button
                            onClick={() => deleteResume(resume.id)}
                            className="text-red-500 hover:text-red-700 focus:outline-none"
                            aria-label="Delete resume"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                        <div className="whitespace-pre-wrap bg-gray-50 p-3 rounded border border-gray-100 text-gray-800 max-h-60 overflow-y-auto">
                          {resume.content}
                        </div>
                      </div>
                    ))}
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

export default ResumeManagementPage;