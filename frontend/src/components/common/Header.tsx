import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

export const Header: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header style={{
      backgroundColor: '#343a40',
      color: 'white',
      padding: '1rem 0'
    }}>
      <div style={{
        maxWidth: '1200px',
        margin: '0 auto',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 20px'
      }}>
        <Link to="/" style={{
          fontSize: '1.5rem',
          fontWeight: 'bold',
          color: 'white',
          textDecoration: 'none'
        }}>
          Health Monitor
        </Link>
        
        <nav style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          {user ? (
            <>
              <Link to="/dashboard" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Дашборд
              </Link>
              <Link to="/blood-pressure" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Давление
              </Link>

              <Link to="/weight" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Вес
              </Link>

              <Link to="/blood-glucose" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Глюкоза
              </Link>

              <Link to="/wellness" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Самочувствие
              </Link>

              <Link to="/analytics" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Аналитика
              </Link>

              <Link to="/profile" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Профиль
              </Link>
              <button onClick={handleLogout} style={{
                background: 'none',
                border: '1px solid white',
                color: 'white',
                padding: '0.5rem 1rem',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to="/login" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Войти
              </Link>
              <Link to="/register" style={{ color: 'white', textDecoration: 'none', padding: '0.5rem 1rem' }}>
                Регистрация
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
};