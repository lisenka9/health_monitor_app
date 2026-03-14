import React, { useState, useEffect } from 'react';
import { User } from '../types';
import { authService } from '../services/auth';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import api from '../services/api';

export const ProfilePage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    email: ''
  });
  const [passwordData, setPasswordData] = useState({
    currentPassword: '',
    newPassword: '',
    confirmPassword: ''
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const userData = await authService.getCurrentUser();
      setUser(userData);
      setFormData({
        full_name: userData.full_name,
        email: userData.email
      });
    } catch (error) {
      console.error('Error loading profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    
    try {
      // Для MVP просто обновляем локально
      setUser(prev => prev ? {...prev, ...formData} : null);
      setMessage('Профиль успешно обновлен');
      setEditMode(false);
    } catch (error) {
      setMessage('Ошибка обновления профиля');
    }
  };

  const handlePasswordChange = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage('');
    
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage('Пароли не совпадают');
      return;
    }
    
    try {
      // TODO: В будущем добавить API для смены пароля
      setMessage('Функция смены пароля будет реализована позже');
      setPasswordData({ currentPassword: '', newPassword: '', confirmPassword: '' });
    } catch (error) {
      setMessage('Ошибка смены пароля');
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>Мой профиль</h1>
      
      {message && (
        <div style={{
          backgroundColor: message.includes('успешно') ? '#d4edda' : '#f8d7da',
          color: message.includes('успешно') ? '#155724' : '#721c24',
          padding: '10px',
          borderRadius: '4px',
          marginBottom: '20px'
        }}>
          {message}
        </div>
      )}
      
      <div style={{ display: 'grid', gap: '30px' }}>
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
            <h2 style={{ margin: 0 }}>Личная информация</h2>
            <button
              onClick={() => setEditMode(!editMode)}
              style={{
                backgroundColor: editMode ? '#6c757d' : '#007bff',
                color: 'white',
                padding: '5px 15px',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              {editMode ? 'Отмена' : 'Редактировать'}
            </button>
          </div>
          
          {editMode ? (
            <form onSubmit={handleProfileUpdate}>
              <div style={{ marginBottom: '15px' }}>
                <label htmlFor="full_name" style={{ display: 'block', marginBottom: '5px' }}>Имя</label>
                <input
                  type="text"
                  id="full_name"
                  value={formData.full_name}
                  onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                  style={{ 
                    width: '100%', 
                    padding: '8px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              <div style={{ marginBottom: '15px' }}>
                <label htmlFor="email" style={{ display: 'block', marginBottom: '5px' }}>Email</label>
                <input
                  type="email"
                  id="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  style={{ 
                    width: '100%', 
                    padding: '8px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              <button type="submit" style={{
                backgroundColor: '#28a745',
                color: 'white',
                padding: '10px 20px',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}>
                Сохранить изменения
              </button>
            </form>
          ) : (
            <div>
              <p><strong>Имя:</strong> {user?.full_name}</p>
              <p><strong>Email:</strong> {user?.email}</p>
              <p><strong>Дата регистрации:</strong> {user?.created_at ? new Date(user.created_at).toLocaleDateString('ru-RU') : ''}</p>
              <p><strong>Статус:</strong> {user?.is_active ? 'Активен' : 'Неактивен'}</p>
            </div>
          )}
        </div>
        
      </div>
    </div>
  );
};