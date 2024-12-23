import React, { useEffect, useState } from 'react';
import { User } from '@core/users/types/user';
import api from '@services/api';

const Home: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [stats, setStats] = useState<any>(null);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        return;
      }
      
      try {
        const [usersResponse, statsResponse] = await Promise.all([
          api.get('/api/users'),
          api.get('/api/stats')
        ]);
        setUsers(usersResponse.data);
        
        if (statsResponse.data.task_id) {
          // Poll for task completion
          const pollInterval = setInterval(async () => {
            try {
              const taskResponse = await api.get(`/api/stats/task/${statsResponse.data.task_id}`);
              if (taskResponse.data.status === 'completed') {
                clearInterval(pollInterval);
                setStats(taskResponse.data.result);
              }
            } catch (error) {
              console.error('Error polling task:', error);
              clearInterval(pollInterval);
            }
          }, 2000); // Poll every 2 seconds
          
          // Cleanup interval on unmount
          return () => clearInterval(pollInterval);
        } else {
          setStats(statsResponse.data);
        }
      } catch (error: any) {
        console.error('Error fetching data:', error);
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
        }
      }
    };

    fetchData();
    
    // Refresh data every minute
    const refreshInterval = setInterval(fetchData, 60000);
    return () => clearInterval(refreshInterval);
  }, []);

  return (
    <div>
      <h1>Welcome</h1>
      
      {stats && (
        <div className="card bg-dark mb-4">
          <div className="card-body">
            <h5 className="card-title">System Statistics</h5>
            <div className="row">
              <div className="col-md-4">
                <p className="mb-1">Total Users:</p>
                <h3>{stats.total_users || stats.message}</h3>
              </div>
              <div className="col-md-4">
                <p className="mb-1">Active Users:</p>
                <h3>{stats.active_users || 'Computing...'}</h3>
              </div>
              <div className="col-md-4">
                <p className="mb-1">Recent Users:</p>
                <h3>{stats.recent_users || 'Computing...'}</h3>
              </div>
            </div>
          </div>
        </div>
      )}

      <div className="row mt-4">
        {users.map(user => (
          <div key={user.id} className="col-md-4 mb-3">
            <div className="card bg-dark">
              <div className="card-body">
                <h5 className="card-title">{user.username}</h5>
                <p className="card-text">{user.email}</p>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Home;
