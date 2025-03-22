import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';

const ResetPasswordPage: React.FC = () => {
  const [token, setToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [message, setMessage] = useState('');
  const { resetPassword } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await resetPassword(token, newPassword, confirmPassword);
    if (response && response.message) {
      setMessage(response.message);
    } else {
      setMessage('Failed to reset password.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-center py-12 px-4">
      <h2 className="text-3xl font-bold mb-6">Reset Password</h2>
      <form className="w-full max-w-md bg-white p-8 rounded shadow" onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="token" className="block text-gray-700">Reset Token</label>
          <input
            id="token"
            type="text"
            required
            value={token}
            onChange={(e) => setToken(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded"
            placeholder="Enter your reset token"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="newPassword" className="block text-gray-700">New Password</label>
          <input
            id="newPassword"
            type="password"
            required
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded"
            placeholder="Enter new password"
          />
        </div>
        <div className="mb-4">
          <label htmlFor="confirmPassword" className="block text-gray-700">Confirm New Password</label>
          <input
            id="confirmPassword"
            type="password"
            required
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            className="mt-1 w-full px-3 py-2 border rounded"
            placeholder="Confirm new password"
          />
        </div>
        <button type="submit" className="w-full py-2 px-4 bg-indigo-600 text-white rounded hover:bg-indigo-700">
          Reset Password
        </button>
      </form>
      {message && (
        <div className="mt-4 text-center text-green-600">
          {message}
        </div>
      )}
      <div className="mt-4">
        <Link to="/login" className="text-indigo-600 hover:underline">Back to Login</Link>
      </div>
    </div>
  );
};

export default ResetPasswordPage;
