import React from 'react';
import { Link } from 'react-router-dom';
import { FileText, Info, MessageSquare } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const HomePage: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-indigo-700 text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-5xl font-bold mb-6">
            Your AI-Powered Job Application Assistant
          </h1>
          <p className="text-xl md:text-2xl mb-8 max-w-3xl mx-auto">
            Streamline your job search with intelligent resume management and personalized application materials.
          </p>
          {!user && (
            <div className="flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/signup"
                className="bg-white text-indigo-700 hover:bg-indigo-100 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
              >
                Get Started
              </Link>
              <Link
                to="/login"
                className="bg-transparent border-2 border-white hover:bg-white hover:text-indigo-700 px-8 py-3 rounded-lg font-semibold text-lg transition-colors"
              >
                Login
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Features Section */}
      <div className="py-16 container mx-auto px-4">
        <h2 className="text-3xl font-bold text-center mb-12 text-gray-800">
          What Applibot Can Do For You
        </h2>
        
        <div className="grid md:grid-cols-3 gap-8">
          <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow">
            <div className="flex justify-center mb-4">
              <div className="bg-indigo-100 p-3 rounded-full">
                <FileText size={32} className="text-indigo-600" />
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center text-gray-800">Resume Management</h3>
            <p className="text-gray-600 text-center">
              Store and monitor your evolving resumes in one place. Keep track of different versions for different job types.
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow">
            <div className="flex justify-center mb-4">
              <div className="bg-indigo-100 p-3 rounded-full">
                <Info size={32} className="text-indigo-600" />
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center text-gray-800">Info Management</h3>
            <p className="text-gray-600 text-center">
              Enter your information once and use it for multiple applications. Format and organize your professional details.
            </p>
          </div>
          
          <div className="bg-white p-8 rounded-xl shadow-md hover:shadow-lg transition-shadow">
            <div className="flex justify-center mb-4">
              <div className="bg-indigo-100 p-3 rounded-full">
                <MessageSquare size={32} className="text-indigo-600" />
              </div>
            </div>
            <h3 className="text-xl font-semibold mb-3 text-center text-gray-800">Custom Generation</h3>
            <p className="text-gray-600 text-center">
              Automatically generate personalized cover letters and responses, each tailored to the job's specific requirements.
            </p>
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-100 py-16">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold mb-6 text-gray-800">Ready to Streamline Your Job Search?</h2>
          <p className="text-xl mb-8 text-gray-600 max-w-2xl mx-auto">
            Join Applibot today and transform your job application process with AI-powered tools.
          </p>
          {!user ? (
            <Link
              to="/signup"
              className="bg-indigo-600 text-white hover:bg-indigo-700 px-8 py-3 rounded-lg font-semibold text-lg transition-colors inline-block"
            >
              Sign Up Now
            </Link>
          ) : (
            <Link
              to="/resume-management"
              className="bg-indigo-600 text-white hover:bg-indigo-700 px-8 py-3 rounded-lg font-semibold text-lg transition-colors inline-block"
            >
              Go to Dashboard
            </Link>
          )}
        </div>
      </div>
    </div>
  );
};

export default HomePage;