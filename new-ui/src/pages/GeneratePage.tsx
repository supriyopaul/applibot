import React, { useState } from 'react';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import { Clipboard, Zap } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const GeneratePage: React.FC = () => {
  const { user } = useAuth();
  const [jobDescription, setJobDescription] = useState('');
  const [formText, setFormText] = useState('');
  const [recruiterDM, setRecruiterDM] = useState('');
  const [dmJobDescription, setDmJobDescription] = useState('');
  
  const [skillMatchOutput, setSkillMatchOutput] = useState('');
  const [expressionOutput, setExpressionOutput] = useState('');
  const [coverLetterOutput, setCoverLetterOutput] = useState('');
  const [formFillOutput, setFormFillOutput] = useState('');
  const [dmReplyOutput, setDmReplyOutput] = useState('');
  
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState('');

  const generateSkillMatch = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      // In a real app, this would call the OpenAI API
      // For demo purposes, we'll simulate a response
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setSkillMatchOutput(
        `Based on the job description, here's how your skills match:\n\n` +
        `✅ Strong match: Communication skills, project management\n` +
        `🟡 Moderate match: Technical expertise in required areas\n` +
        `❌ Areas to improve: Specific industry experience\n\n` +
        `Overall match score: 75%`
      );
    } catch (err) {
      setError('Failed to generate skill match. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateExpression = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setExpressionOutput(
        `Dear Hiring Manager,\n\n` +
        `I am writing to express my strong interest in the position advertised. ` +
        `With my background in the required field and passion for innovation, ` +
        `I believe I would be an excellent fit for your team.\n\n` +
        `I look forward to discussing how my skills align with your needs.\n\n` +
        `Sincerely,\n[Your Name]`
      );
    } catch (err) {
      setError('Failed to generate expression of interest. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateCoverLetter = async () => {
    if (!jobDescription.trim()) {
      setError('Please enter a job description');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setCoverLetterOutput(
        `Dear Hiring Team,\n\n` +
        `I am excited to apply for the position at your company. ` +
        `Throughout my career, I have developed the exact skills mentioned in your job posting, ` +
        `including [specific skills from job description].\n\n` +
        `In my previous role at [Previous Company], I successfully [relevant achievement]. ` +
        `This experience has prepared me well for the challenges of this position.\n\n` +
        `I am particularly drawn to your company because of [company value or project]. ` +
        `I am confident that my background and enthusiasm make me an ideal candidate.\n\n` +
        `Thank you for considering my application. I look forward to the opportunity to discuss ` +
        `how I can contribute to your team's success.\n\n` +
        `Sincerely,\n[Your Name]`
      );
    } catch (err) {
      setError('Failed to generate cover letter. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateFormFill = async () => {
    if (!formText.trim()) {
      setError('Please enter the form text');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setFormFillOutput(
        `[Name]: John Doe\n` +
        `[Email]: john.doe@example.com\n` +
        `[Phone]: (555) 123-4567\n` +
        `[Address]: 123 Main Street, Anytown, ST 12345\n\n` +
        `[Work Experience]: 5+ years in software development\n` +
        `[Education]: Bachelor's in Computer Science\n` +
        `[Skills]: JavaScript, React, Node.js, Python\n\n` +
        `[Why do you want to work here?]: I'm passionate about your company's mission to innovate in the tech space, and I believe my skills in web development would be a valuable addition to your team.`
      );
    } catch (err) {
      setError('Failed to generate form fill. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const generateDMReply = async () => {
    if (!recruiterDM.trim() || !dmJobDescription.trim()) {
      setError('Please enter both the recruiter\'s DM and job description');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      setDmReplyOutput(
        `Thank you for reaching out about the opportunity at [Company Name]!\n\n` +
        `I'm very interested in the position and believe my background in [relevant skill] ` +
        `aligns well with what you're looking for. I particularly appreciate the focus on ` +
        `[aspect from job description].\n\n` +
        `I'd love to discuss this opportunity further. Would you be available for a call ` +
        `this week? I'm flexible and can work around your schedule.\n\n` +
        `Looking forward to speaking with you!\n\n` +
        `Best regards,\n[Your Name]`
      );
    } catch (err) {
      setError('Failed to generate DM reply. Please try again.');
    } finally {
      setIsGenerating(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const renderApiKeyWarning = () => {
    if (!user?.apiKey) {
      return (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 mb-6">
          <div className="flex">
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                <strong>Note:</strong> You haven't set up your OpenAI API key yet. 
                The generation features are currently in demo mode with pre-defined responses. 
                To use the full AI capabilities, please add your API key in the{' '}
                <a href="/account" className="font-medium underline">Account</a> page.
              </p>
            </div>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
          <div className="p-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-8">Generate Content</h1>
            
            {renderApiKeyWarning()}
            
            {error && (
              <div className="bg-red-50 border-l-4 border-red-400 p-4 mb-6">
                <p className="text-red-700">{error}</p>
              </div>
            )}
            
            <Tabs className="mb-4">
              <TabList className="flex border-b border-gray-200 mb-6 overflow-x-auto">
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Skill Match
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Expression of Interest
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Cover Letter
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  Form Fill-up
                </Tab>
                <Tab className="px-6 py-2 font-medium text-gray-600 hover:text-indigo-600 cursor-pointer border-b-2 border-transparent hover:border-indigo-600 transition-colors whitespace-nowrap">
                  DM Reply
                </Tab>
              </TabList>
              
              {/* Skill Match Tab */}
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="job-description-skill" className="block text-sm font-medium text-gray-700 mb-1">
                      Job Description
                    </label>
                    <textarea
                      id="job-description-skill"
                      rows={8}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={generateSkillMatch}
                      disabled={isGenerating}
                      className={`flex items-center px-4 py-2 ${
                        isGenerating ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
                      } text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
                    >
                      {isGenerating ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Zap size={18} className="mr-1" />
                          Generate Skill Match
                        </>
                      )}
                    </button>
                  </div>
                  
                  {skillMatchOutput && (
                    <div className="mt-6">
                      <div className="flex justify-between items-center mb-2">
                        <label className="block text-sm font-medium text-gray-700">
                          Skill Match Analysis
                        </label>
                        <button
                          onClick={() => copyToClipboard(skillMatchOutput)}
                          className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm"
                        >
                          <Clipboard size={16} className="mr-1" />
                          Copy to Clipboard
                        </button>
                      </div>
                      <div className="relative">
                        <div className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 whitespace-pre-wrap h-64 overflow-y-auto">
                          {skillMatchOutput}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </TabPanel>
              
              {/* Expression of Interest Tab */}
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="job-description-expression" className="block text-sm font-medium text-gray-700 mb-1">
                      Job Description
                    </label>
                    <textarea
                      id="job-description-expression"
                      rows={8}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={generateExpression}
                      disabled={isGenerating}
                      className={`flex items-center px-4 py-2 ${
                        isGenerating ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
                      } text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
                    >
                      {isGenerating ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Zap size={18} className="mr-1" />
                          Generate Expression
                        </>
                      )}
                    </button>
                  </div>
                  
                  {expressionOutput && (
                    <div className="mt-6">
                      <div className="flex justify-between items-center mb-2">
                        <label className="block text-sm font-medium text-gray-700">
                          Expression of Interest
                        </label>
                        <button
                          onClick={() => copyToClipboard(expressionOutput)}
                          className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm"
                        >
                          <Clipboard size={16} className="mr-1" />
                          Copy to Clipboard
                        </button>
                      </div>
                      <div className="relative">
                        <div className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 whitespace-pre-wrap h-64 overflow-y-auto">
                          {expressionOutput}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </TabPanel>
              
              {/* Cover Letter Tab */}
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="job-description-cover" className="block text-sm font-medium text-gray-700 mb-1">
                      Job Description
                    </label>
                    <textarea
                      id="job-description-cover"
                      rows={8}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste the job description here..."
                      value={jobDescription}
                      onChange={(e) => setJobDescription(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={generateCoverLetter}
                      disabled={isGenerating}
                      className={`flex items-center px-4 py-2 ${
                        isGenerating ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
                      } text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
                    >
                      {isGenerating ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Zap size={18} className="mr-1" />
                          Generate Cover Letter
                        </>
                      )}
                    </button>
                  </div>
                  
                  {coverLetterOutput && (
                    <div className="mt-6">
                      <div className="flex justify-between items-center mb-2">
                        <label className="block text-sm font-medium text-gray-700">
                          Cover Letter
                        </label>
                        <button
                          onClick={() => copyToClipboard(coverLetterOutput)}
                          className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm"
                        >
                          <Clipboard size={16} className="mr-1" />
                          Copy to Clipboard
                        </button>
                      </div>
                      <div className="relative">
                        <div className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 whitespace-pre-wrap h-64 overflow-y-auto">
                          {coverLetterOutput}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </TabPanel>
              
              {/* Form Fill-up Tab */}
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="form-text" className="block text-sm font-medium text-gray-700 mb-1">
                      Empty Form Text
                    </label>
                    <textarea
                      id="form-text"
                      rows={8}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste the empty form here..."
                      value={formText}
                      onChange={(e) => setFormText(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={generateFormFill}
                      disabled={isGenerating}
                      className={`flex items-center px-4 py-2 ${
                        isGenerating ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
                      } text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
                    >
                      {isGenerating ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Zap size={18} className="mr-1" />
                          Generate Form Fill
                        </>
                      )}
                    </button>
                  </div>
                  
                  {formFillOutput && (
                    <div className="mt-6">
                      <div className="flex justify-between items-center mb-2">
                        <label className="block text-sm font-medium text-gray-700">
                          Filled Form
                        </label>
                        <button
                          onClick={() => copyToClipboard(formFillOutput)}
                          className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm"
                        >
                          <Clipboard size={16} className="mr-1" />
                          Copy to Clipboard
                        </button>
                      </div>
                      <div className="relative">
                        <div className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 whitespace-pre-wrap h-64 overflow-y-auto">
                          {formFillOutput}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </TabPanel>
              
              {/* DM Reply Tab */}
              <TabPanel>
                <div className="space-y-4">
                  <div>
                    <label htmlFor="recruiter-dm" className="block text-sm font-medium text-gray-700 mb-1">
                      Recruiter's DM
                    </label>
                    <textarea
                      id="recruiter-dm"
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste the recruiter's message here..."
                      value={recruiterDM}
                      onChange={(e) => setRecruiterDM(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div>
                    <label htmlFor="dm-job-description" className="block text-sm font-medium text-gray-700 mb-1">
                      Job Description
                    </label>
                    <textarea
                      id="dm-job-description"
                      rows={4}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="Paste the job description here..."
                      value={dmJobDescription}
                      onChange={(e) => setDmJobDescription(e.target.value)}
                    ></textarea>
                  </div>
                  
                  <div className="flex justify-end">
                    <button
                      onClick={generateDMReply}
                      disabled={isGenerating}
                      className={`flex items-center px-4 py-2 ${
                        isGenerating ? 'bg-indigo-400' : 'bg-indigo-600 hover:bg-indigo-700'
                      } text-white rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
                    >
                      {isGenerating ? (
                        <>
                          <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          Generating...
                        </>
                      ) : (
                        <>
                          <Zap size={18} className="mr-1" />
                          Generate DM Reply
                        </>
                      )}
                    </button>
                  </div>
                  
                  {dmReplyOutput && (
                    <div className="mt-6">
                      <div className="flex justify-between items-center mb-2">
                        <label className="block text-sm font-medium text-gray-700">
                          DM Reply
                        </label>
                        <button
                          onClick={() => copyToClipboard(dmReplyOutput)}
                          className="flex items-center text-indigo-600 hover:text-indigo-800 text-sm"
                        >
                          <Clipboard size={16} className="mr-1" />
                          Copy to Clipboard
                        </button>
                      </div>
                      <div className="relative">
                        <div className="w-full px-3 py-2 border border-gray-300 rounded-md bg-gray-50 whitespace-pre-wrap h-64 overflow-y-auto">
                          {dmReplyOutput}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </TabPanel>
            </Tabs>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GeneratePage;