import React from 'react';
import { Bot, Shield, FileText, MessageSquare, BarChart } from 'lucide-react';

const AboutPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
          <div className="p-8">
            <div className="flex items-center justify-center mb-6">
              <Bot size={48} className="text-indigo-600" />
            </div>
            
            <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">
              About Applibot
            </h1>
            
            <div className="prose prose-lg max-w-none">
              <p className="mb-4">
                Applibot is crafted with <strong>Retrieval Augmented Generation (RAG)</strong> at its heart, serving as a guiding companion in the job-seeking saga. More than a mere application aid, Applibot is your strategic partner, designed to streamline the complexities of job hunting across all professions.
              </p>
              
              <p className="mb-4">
                The essence of Applibot lies in its ability to smarten your professional footprint. It neatly organizes your resumes, dresses your information in polished templates, and helps articulate cover letters that capture your unique voice. Beyond mere document management, Applibot draws upon your own experiences to provide nuanced responses to inquiries, direct messages, and personalized expressions of interest that align with the roles you aspire to fill.
              </p>
              
              <p className="mb-4">
                With an analytical feature that maps your abilities against job requirements, Applibot provides a mirror to reflect your fit for a position, guiding you to fine-tune your presentations to prospective employers.
              </p>
              
              <p className="mb-4">
                Security and simplicity are pillars of the Applibot experience, ensuring peace of mind and a straightforward, user-friendly interface. Whether you're a seasoned professional or just starting out, Applibot is here to support your journey to the next opportunity. Let's take the leap into your future career together. 🚀
              </p>
              
              <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 my-6">
                <p className="text-yellow-700">
                  <strong>Note</strong>: To fully harness the capabilities of Applibot, particularly the ones that interact with the <strong>GPT-4 model</strong>, you'll need an OpenAI API key that can access GPT-4. As of now, <strong>the GPT-4 access is a premium feature</strong>. Ensure you possess the necessary permissions.
                </p>
              </div>
            </div>
            
            <div className="mt-12 grid md:grid-cols-3 gap-6">
              <div className="bg-indigo-50 p-6 rounded-lg">
                <div className="flex justify-center mb-4">
                  <FileText size={32} className="text-indigo-600" />
                </div>
                <h3 className="text-lg font-semibold text-center mb-2">Document Management</h3>
                <p className="text-gray-600 text-center text-sm">
                  Organize and store all your professional documents in one secure location.
                </p>
              </div>
              
              <div className="bg-indigo-50 p-6 rounded-lg">
                <div className="flex justify-center mb-4">
                  <MessageSquare size={32} className="text-indigo-600" />
                </div>
                <h3 className="text-lg font-semibold text-center mb-2">AI-Powered Generation</h3>
                <p className="text-gray-600 text-center text-sm">
                  Create personalized application materials with advanced AI technology.
                </p>
              </div>
              
              <div className="bg-indigo-50 p-6 rounded-lg">
                <div className="flex justify-center mb-4">
                  <BarChart size={32} className="text-indigo-600" />
                </div>
                <h3 className="text-lg font-semibold text-center mb-2">Skills Analysis</h3>
                <p className="text-gray-600 text-center text-sm">
                  Compare your qualifications with job requirements to identify your strengths.
                </p>
              </div>
            </div>
            
            <div className="mt-12 flex justify-center">
              <div className="flex items-center text-indigo-600">
                <Shield size={20} className="mr-2" />
                <span className="text-sm font-medium">Secure & Privacy-Focused</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;