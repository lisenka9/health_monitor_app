import React from 'react';
import { Link } from 'react-router-dom';
import { RegisterForm } from '../components/forms/RegisterForm';

export const Register: React.FC = () => {
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
        <RegisterForm />
        <p style={{ textAlign: 'center', marginTop: '20px' }}>
          Уже есть аккаунт? <Link to="/login">Войдите</Link>
        </p>
      </div>
    </div>
  );
};