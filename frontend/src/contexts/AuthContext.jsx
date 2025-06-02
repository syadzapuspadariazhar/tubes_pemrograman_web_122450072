import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user is already logged in on app start
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const token = localStorage.getItem('authToken');
      if (!token) {
        setIsLoading(false);
        return;
      }

      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // Verify token with backend
      const response = await axios.get(`${API_BASE_URL}/api/auth/verify`);
      
      if (response.data.valid) {
        setIsAuthenticated(true);
        setUser(response.data.user);
      } else {
        // Token is invalid, remove it
        localStorage.removeItem('authToken');
        delete axios.defaults.headers.common['Authorization'];
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      // Remove invalid token
      localStorage.removeItem('authToken');
      delete axios.defaults.headers.common['Authorization'];
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      setIsLoading(true);

      const response = await axios.post(`${API_BASE_URL}/api/auth/login`, {
        username,
        password
      });

      const { token, user } = response.data;

      // Store token
      localStorage.setItem('authToken', token);
      
      // Set axios default header
      axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

      // Update state
      setIsAuthenticated(true);
      setUser(user);

      return { success: true };
    } catch (error) {
      console.error('Login failed:', error);
      
      // Handle different error types
      if (error.response?.status === 401) {
        throw new Error('Username atau password salah');
      } else if (error.response?.status >= 500) {
        throw new Error('Server error. Silakan coba lagi nanti.');
      } else if (error.code === 'ECONNABORTED') {
        throw new Error('Request timeout. Silakan coba lagi.');
      } else {
        throw new Error('Login gagal. Silakan coba lagi.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    // Remove token from storage
    localStorage.removeItem('authToken');
    
    // Remove axios default header
    delete axios.defaults.headers.common['Authorization'];
    
    // Update state
    setIsAuthenticated(false);
    setUser(null);
  };

  const value = {
    isAuthenticated,
    user,
    isLoading,
    login,
    logout,
    checkAuthStatus
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export { AuthContext };
