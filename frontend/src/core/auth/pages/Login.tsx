import React, { useState, FormEvent } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import api from '@services/api';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    console.log('Form submission started');
    
    if (isLoading) {
      console.log('Already processing login request');
      return;
    }
    
    setError('');
    setIsLoading(true);
    
    try {
      console.log('Making login request with email:', formData.email);
      const response = await api.post('/auth/login', formData);
      console.log('Login response:', response);
      
      if (!response.data) {
        console.error('No response data received');
        throw new Error('No response data received');
      }
      
      const { access_token, user } = response.data;
      if (!access_token) {
        console.error('No access token in response');
        throw new Error('Authentication failed - no token received');
      }
      
      console.log('Login successful, storing token');
      localStorage.setItem('token', access_token);
      api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Verify token works
      try {
        console.log('Testing token with users endpoint');
        const testResponse = await api.get('/api/users');
        console.log('Test API call successful:', testResponse.data);
        navigate('/', { replace: true });
      } catch (testError: any) {
        console.error('Test API call failed:', testError);
        throw new Error('Token verification failed');
      }
    } catch (error: any) {
      console.error('Login error:', error);
      const errorMessage = error.response?.data?.error || error.message || 'Login failed';
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      });
      console.error('Error details:', {
        status: error.response?.status,
        data: error.response?.data,
        message: error.message
      });
      setError(errorMessage);
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="row justify-content-center">
      <div className="col-md-6">
        <div className="card bg-dark">
          <div className="card-body">
            <h2 className="card-title text-center mb-4">Login</h2>
            {error && (
              <div className="alert alert-danger" role="alert">
                {error}
              </div>
            )}
            <form onSubmit={handleSubmit}>
              <div className="mb-3">
                <label className="form-label">Email</label>
                <input
                  type="email"
                  className="form-control"
                  value={formData.email}
                  onChange={e => setFormData({...formData, email: e.target.value})}
                  required
                />
              </div>
              <div className="mb-3">
                <label className="form-label">Password</label>
                <input
                  type="password"
                  className="form-control"
                  value={formData.password}
                  onChange={e => setFormData({...formData, password: e.target.value})}
                  required
                />
              </div>
              <button 
                type="submit" 
                className="btn btn-primary w-100" 
                disabled={isLoading}
              >
                {isLoading ? 'Logging in...' : 'Login'}
              </button>
            </form>
            <div className="text-center mt-3">
              <p>Don't have an account? <Link to="/register" className="text-primary">Register here</Link></p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
