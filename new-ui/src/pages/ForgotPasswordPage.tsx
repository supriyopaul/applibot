import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const ForgotPasswordPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [resetUrl, setResetUrl] = useState('');
  const [message, setMessage] = useState('');
  const { forgotPassword } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await forgotPassword(email);
    if (response && response.reset_url) {
      setResetUrl(response.reset_url);
      setMessage('A password reset link has been generated:');
    } else {
      setMessage('If an account with that email exists, a reset link has been sent.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center py-12 px-4">
      <h2 className="text-3xl font-bold mb-6">Forgot Password</h2>
      <form className="w-full max-w-md bg-white p-8 rounded shadow" onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700">Email address</label>
          <input
            id="email"
            type="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded"
            placeholder="Enter your email"
          />
        </div>
        <button type="submit" className="w-full py-2 px-4 bg-indigo-600 text-white rounded hover:bg-indigo-700">
          Send Reset Link
        </button>
      </form>
      {message && (
        <div className="mt-4 text-center">
          <p className="text-green-600">{message}</p>
          {resetUrl && (
            <a href={resetUrl} className="text-indigo-600 hover:underline">{resetUrl}</a>
          )}
        </div>
      )}
      <div className="mt-4">
        <Link to="/login" className="text-indigo-600 hover:underline">Back to Login</Link>
      </div>
    </div>
  );
};

export default ForgotPasswordPage;
