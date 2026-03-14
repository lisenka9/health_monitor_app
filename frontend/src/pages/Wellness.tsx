import React, { useState, useEffect } from 'react';
import { WellnessEntry, WellnessEntryCreate } from '../types';
import { measurementsService } from '../services/measurements';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const WellnessPage: React.FC = () => {
  const [formData, setFormData] = useState<WellnessEntryCreate>({
    description: '',
    mood: '',
    symptoms: ''
  });
  const [entries, setEntries] = useState<WellnessEntry[]>([]);
  const [loading, setLoading] = useState(false);
  const [entriesLoading, setEntriesLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);

  useEffect(() => {
    loadEntries();
  }, []);

  const loadEntries = async () => {
    setEntriesLoading(true);
    try {
      const data = await measurementsService.getWellnessHistory();
      setEntries(data);
    } catch (error) {
      console.error('Error loading wellness entries:', error);
    } finally {
      setEntriesLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      if (editingId) {
        await measurementsService.updateWellnessEntry(editingId, formData);
        setSuccess('Запись успешно обновлена!');
        setEditingId(null);
      } else {
        await measurementsService.createWellnessEntry(formData);
        setSuccess('Запись успешно сохранена!');
      }
      setFormData({ description: '', mood: '', symptoms: '' });
      
      await loadEntries();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (entry: WellnessEntry) => {
    setFormData({
      description: entry.description || '',
      mood: entry.mood || '',
      symptoms: entry.symptoms || ''
    });
    setEditingId(entry.id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить эту запись?')) {
      try {
        await measurementsService.deleteWellnessEntry(id);
        await loadEntries();
        setSuccess('Запись успешно удалена!');
      } catch (error) {
        console.error('Error deleting entry:', error);
        setError('Ошибка при удалении записи');
      }
    }
  };

  const handleCancelEdit = () => {
    setFormData({ description: '', mood: '', symptoms: '' });
    setEditingId(null);
  };

  const moodOptions = [
    { value: '', label: 'Выберите настроение' },
    { value: 'good', label: '😊 Хорошее' },
    { value: 'normal', label: '😐 Нормальное' },
    { value: 'bad', label: '😔 Плохое' }
  ];

  const getMoodDisplay = (mood: string | undefined) => {
    switch (mood) {
      case 'good': return '😊 Хорошее';
      case 'normal': return '😐 Нормальное';
      case 'bad': return '😔 Плохое';
      default: return 'Не указано';
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>Дневник самочувствия</h1>
      
      {error && (
        <div style={{ 
          backgroundColor: '#f8d7da', 
          color: '#721c24', 
          padding: '10px', 
          borderRadius: '4px', 
          marginBottom: '15px' 
        }}>
          {error}
        </div>
      )}
      
      {success && (
        <div style={{ 
          backgroundColor: '#d4edda', 
          color: '#155724', 
          padding: '10px', 
          borderRadius: '4px', 
          marginBottom: '15px' 
        }}>
          {success}
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h2 style={{ marginBottom: '20px' }}>
            {editingId ? 'Редактировать запись' : 'Добавить запись'}
          </h2>

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="mood" style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
                Настроение
              </label>
              <select
                id="mood"
                name="mood"
                value={formData.mood}
                onChange={handleChange}
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: '1px solid #ddd', 
                  borderRadius: '4px', 
                  fontSize: '14px' 
                }}
              >
                {moodOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="symptoms" style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
                Симптомы
              </label>
              <textarea
                id="symptoms"
                name="symptoms"
                value={formData.symptoms}
                onChange={handleChange}
                placeholder="Головная боль, усталость, тошнота..."
                rows={3}
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: '1px solid #ddd', 
                  borderRadius: '4px', 
                  fontSize: '14px', 
                  resize: 'vertical' 
                }}
              />
            </div>
            
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="description" style={{ display: 'block', marginBottom: '5px', fontWeight: '500' }}>
                Описание
              </label>
              <textarea
                id="description"
                name="description"
                value={formData.description}
                onChange={handleChange}
                placeholder="Опишите свое самочувствие..."
                rows={4}
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: '1px solid #ddd', 
                  borderRadius: '4px', 
                  fontSize: '14px', 
                  resize: 'vertical' 
                }}
              />
            </div>
            
            <button 
              type="submit" 
              disabled={loading} 
              style={{
                backgroundColor: editingId ? '#ffc107' : '#28a745',
                color: 'white',
                padding: '10px 20px',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                fontSize: '16px',
                width: '100%',
                marginBottom: editingId ? '10px' : '0'
              }}
            >
              {loading ? 'Сохранение...' : (editingId ? 'Обновить запись' : 'Сохранить запись')}
            </button>
            
            {editingId && (
              <button
                type="button"
                onClick={handleCancelEdit}
                style={{
                  backgroundColor: '#6c757d',
                  color: 'white',
                  padding: '10px 20px',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer',
                  fontSize: '16px',
                  width: '100%'
                }}
              >
                Отмена редактирования
              </button>
            )}
          </form>
        </div>

        <div style={{ background: 'white', padding: '20px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <h2 style={{ marginBottom: '20px' }}>История записей</h2>

          {entriesLoading ? (
            <LoadingSpinner />
          ) : entries.length > 0 ? (
            <div style={{ maxHeight: '600px', overflowY: 'auto' }}>
              {entries.map((entry) => (
                <div key={entry.id} style={{
                  borderBottom: '1px solid #eee',
                  padding: '15px 0',
                  position: 'relative'
                }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '10px' }}>
                    <div>
                      <strong style={{ fontSize: '18px' }}>
                        {getMoodDisplay(entry.mood)}
                      </strong>
                      <div style={{ fontSize: '12px', color: '#666', marginTop: '5px' }}>
                        {new Date(entry.date).toLocaleDateString('ru-RU')} в{' '}
                        {new Date(entry.date).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })}
                      </div>
                    </div>
                    <div>
                      <button
                        onClick={() => handleEdit(entry)}
                        style={{
                          background: 'none',
                          border: '1px solid #007bff',
                          color: '#007bff',
                          padding: '5px 10px',
                          borderRadius: '4px',
                          cursor: 'pointer',
                          marginRight: '5px'
                        }}
                      >
                        Редактировать
                      </button>
                      <button
                        onClick={() => handleDelete(entry.id)}
                        style={{
                          background: 'none',
                          border: '1px solid #dc3545',
                          color: '#dc3545',
                          padding: '5px 10px',
                          borderRadius: '4px',
                          cursor: 'pointer'
                        }}
                      >
                        Удалить
                      </button>
                    </div>
                  </div>

                  {entry.symptoms && (
                    <div style={{ marginBottom: '10px' }}>
                      <strong>Симптомы:</strong> {entry.symptoms}
                    </div>
                  )}

                  {entry.description && (
                    <div>
                      <strong>Описание:</strong>
                      <p style={{ margin: '5px 0 0 0', color: '#333' }}>{entry.description}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <p style={{ color: '#666', fontStyle: 'italic' }}>
              Нет записей о самочувствии
            </p>
          )}
        </div>
      </div>
    </div>
  );
};