import React, { useState } from 'react';
import api from '../services/api';

function Auth() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    try {
      const response = await api.post('/auth/register', { email, password });
      setMessage(`Registration successful: ${response.data.email}`);
    } catch (error) {
      setMessage(`Registration failed: ${error.response?.data?.detail || error.message}`);
    }
  };

  const handleLogin = async () => {
    try {
      // FastAPI's OAuth2PasswordRequestForm expects x-www-form-urlencoded
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      const response = await api.post('/auth/token', formData.toString(), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      localStorage.setItem('accessToken', response.data.access_token);
      setMessage(`Login successful! Token stored.`);
      // Redirect or update UI to show logged-in state
    } catch (error) {
      setMessage(`Login failed: ${error.response?.data?.detail || error.message}`);
    }
  };

  return (
    <div>
      <h2>Authentication</h2>
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
      <input type="password" placeholder="Password" value={password} onChange={(e) => setPassword(e.target.value)} />
      <button onClick={handleRegister}>Register</button>
      <button onClick={handleLogin}>Login</button>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Auth;