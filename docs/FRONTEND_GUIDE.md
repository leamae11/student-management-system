# Frontend Integration Guide

## Frontend Setup

This guide helps you set up a React/Vue frontend to work with the Django backend.

## React Setup

### 1. Create React App

```bash
npx create-react-app frontend
cd frontend
```

### 2. Install Dependencies

```bash
npm install axios react-router-dom redux react-redux
npm install --save-dev tailwindcss postcss autoprefixer
```

### 3. Create API Service

**src/services/api.js**
```javascript
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default api;
```

### 4. Authentication Service

**src/services/auth.js**
```javascript
import api from './api';

export const authService = {
  register: (userData) => api.post('/users/register/', userData),
  
  login: (credentials) => {
    return api.post('/users/login/', credentials).then((response) => {
      localStorage.setItem('access_token', response.data.access);
      localStorage.setItem('refresh_token', response.data.refresh);
      return response.data;
    });
  },
  
  logout: () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },
  
  getProfile: () => api.get('/users/profile/'),
};
```

### 5. Task Service

**src/services/tasks.js**
```javascript
import api from './api';

export const taskService = {
  getAll: () => api.get('/tasks/'),
  
  getPending: () => api.get('/tasks/pending/'),
  
  getCompleted: () => api.get('/tasks/completed/'),
  
  getOverdue: () => api.get('/tasks/overdue/'),
  
  create: (taskData) => api.post('/tasks/', taskData),
  
  update: (id, taskData) => api.put(`/tasks/${id}/`, taskData),
  
  delete: (id) => api.delete(`/tasks/${id}/`),
  
  markComplete: (id) => api.post(`/tasks/${id}/mark_complete/`),
};
```

### 6. Grades Service

**src/services/grades.js**
```javascript
import api from './api';

export const gradeService = {
  getAll: () => api.get('/grades/'),
  
  getGPA: () => api.get('/grades/gpa/'),
  
  getBySemester: (semester) => 
    api.get(`/grades/by_semester/?semester=${semester}`),
  
  create: (gradeData) => api.post('/grades/', gradeData),
  
  update: (id, gradeData) => api.put(`/grades/${id}/`, gradeData),
};
```

### 7. Login Component

**src/components/Login.js**
```javascript
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { authService } from '../services/auth';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await authService.login({ username, password });
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
    }
  };

  return (
    <div className="flex justify-center items-center h-screen">
      <form onSubmit={handleSubmit} className="w-96 p-8 border rounded-lg">
        <h1 className="text-2xl font-bold mb-6">Student Dashboard</h1>
        
        {error && <div className="text-red-500 mb-4">{error}</div>}
        
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          className="w-full p-2 mb-4 border rounded"
        />
        
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="w-full p-2 mb-6 border rounded"
        />
        
        <button
          type="submit"
          className="w-full p-2 bg-blue-500 text-white rounded font-bold"
        >
          Login
        </button>
      </form>
    </div>
  );
}

export default Login;
```

### 8. Dashboard Component

**src/components/Dashboard.js**
```javascript
import React, { useEffect, useState } from 'react';
import { taskService } from '../services/tasks';
import { gradeService } from '../services/grades';

function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [gpa, setGPA] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const tasksRes = await taskService.getPending();
        const gpaRes = await gradeService.getGPA();
        
        setTasks(tasksRes.data);
        setGPA(gpaRes.data.gpa);
      } catch (err) {
        console.error('Error loading data:', err);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, []);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-8">Dashboard</h1>
      
      {/* GPA Card */}
      <div className="bg-blue-100 p-4 rounded-lg mb-8">
        <h2 className="text-xl font-bold">Current GPA</h2>
        <p className="text-3xl font-bold text-blue-600">{gpa.toFixed(2)}</p>
      </div>
      
      {/* Tasks List */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Pending Tasks</h2>
        {tasks.length === 0 ? (
          <p>No pending tasks</p>
        ) : (
          <div className="space-y-4">
            {tasks.map(task => (
              <div key={task.id} className="p-4 border rounded-lg">
                <h3 className="font-bold">{task.title}</h3>
                <p className="text-gray-600">{task.description}</p>
                <p className="text-sm mt-2">Priority: {task.priority}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
```

### 9. CORS Configuration

Ensure Django settings allow your frontend:

**.env**
```env
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8080
```

### 10. Run Frontend

```bash
npm start
```

Frontend will run at: http://localhost:3000

## Vue Setup

For Vue.js, follow similar patterns with:
- Vue Router for navigation
- Vuex for state management
- Axios for API calls

## Environment Variables

**.env.local**
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENV=development
```

## Production Build

```bash
npm run build
```

## Common Issues

### CORS Errors
- Ensure CORS_ALLOWED_ORIGINS includes your frontend URL
- Check backend is running on correct port

### 401 Unauthorized
- Check if token is being sent in headers
- Verify token is stored in localStorage
- Token may have expired

### 404 Not Found
- Check API endpoint URLs
- Verify backend is running
- Check API base URL in services

## Next Steps

1. Create more components (Notes, OJT, Requirements)
2. Implement state management
3. Add form validation
4. Setup error handling
5. Add loading states
6. Style with Tailwind/Material UI
7. Deploy to production
