import React from 'react';
import { Link } from 'react-router-dom';
import { LoginForm } from '../components/forms/LoginForm';

export const Login: React.FC = () => {
  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: '#f5f5f5'
    }}>
      <div style={{
        width: '100%',
        maxWidth: '500px',
        padding: '20px'
      }}>
        <LoginForm />
        <p style={{ textAlign: 'center', marginTop: '20px' }}>
          Нет аккаунта? <Link to="/register">Зарегистрируйтесь</Link>
        </p>
      </div>
    </div>
  );
};