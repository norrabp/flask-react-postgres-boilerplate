import React, { useEffect, useState } from 'react';
import { User } from '@core/users/types/user';
import api from '@services/api';
import StatsCard from '@core/users/components/StatsCard';
import UserCard from '@core/users/components/UserCard';

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
        setUsers(usersResponse.data.users);
        
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
        <StatsCard stats={stats} />
      )}

      <div className="row mt-4">
        {users.map(user => (
          <UserCard user={user} />
        ))}
      </div>
    </div>
  );
};

export default Home;
