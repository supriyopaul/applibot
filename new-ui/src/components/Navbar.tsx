import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Bot, LogOut, Zap } from 'lucide-react';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-indigo-600 text-white shadow-md">
      <div className="container mx-auto px-4 py-3">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2 text-xl font-bold">
            <Bot size={24} />
            <span>Applibot</span>
          </Link>
          
          <div className="flex space-x-6">
            <Link to="/about" className="hover:text-indigo-200 transition-colors">
              About
            </Link>
            
            {user ? (
              <>
                <Link to="/resume-management" className="hover:text-indigo-200 transition-colors">
                  Resume Management
                </Link>
                <Link to="/info-management" className="hover:text-indigo-200 transition-colors">
                  Info Management
                </Link>
                <Link to="/generate" className="flex items-center hover:text-indigo-200 transition-colors">
                  <Zap size={18} className="mr-1" />
                  Generate
                </Link>
                <Link to="/account" className="hover:text-indigo-200 transition-colors">
                  Account
                </Link>
                <button 
                  onClick={handleLogout}
                  className="flex items-center hover:text-indigo-200 transition-colors"
                >
                  <LogOut size={18} className="mr-1" />
                  Logout
                </button>
              </>
            ) : (
              <Link to="/login" className="hover:text-indigo-200 transition-colors">
                Login
              </Link>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;