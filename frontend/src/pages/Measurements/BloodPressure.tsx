import React, { useState, useEffect } from 'react';
import { BloodPressure as BloodPressureType, BloodPressureCreate } from '../../types';
import { measurementsService } from '../../services/measurements';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';

export const BloodPressurePage: React.FC = () => {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [formData, setFormData] = useState<BloodPressureCreate>({
    systolic: 120,
    diastolic: 80,
    pulse: 70,
    notes: ''
  });
  const [history, setHistory] = useState<BloodPressureType[]>([]);
  const [loading, setLoading] = useState(false);
  const [historyLoading, setHistoryLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    setHistoryLoading(true);
    try {
      const data = await measurementsService.getBloodPressureHistory();
      let filtered = data;

      if (startDate) {
        filtered = filtered.filter(item =>
          new Date(item.date) >= new Date(startDate)
        );
      }
      if (endDate) {
        filtered = filtered.filter(item =>
          new Date(item.date) <= new Date(endDate + 'T23:59:59')
        );
      }
      setHistory(filtered);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setHistoryLoading(false);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'systolic' || name === 'diastolic' || name === 'pulse'
        ? parseInt(value) || 0
        : value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      if (editingId) {
        await measurementsService.updateBloodPressure(editingId, formData);
        setSuccess('Измерение успешно обновлено!');
        setEditingId(null);
      } else {
        await measurementsService.createBloodPressure(formData);
        setSuccess('Измерение успешно сохранено!');
      }
      
      setFormData({
        systolic: 120,
        diastolic: 80,
        pulse: 70,
        notes: ''
      });
      
      await loadHistory();
      
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = (item: BloodPressureType) => {
    setFormData({
      systolic: item.systolic,
      diastolic: item.diastolic,
      pulse: item.pulse,
      notes: item.notes || ''
    });
    setEditingId(item.id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить это измерение?')) {
      try {
        await measurementsService.deleteBloodPressure(id);
        await loadHistory();
        setSuccess('Измерение успешно удалено!');
      } catch (error) {
        console.error('Error deleting measurement:', error);
        setError('Ошибка при удалении измерения');
      }
    }
  };

  const handleCancelEdit = () => {
    setFormData({
      systolic: 120,
      diastolic: 80,
      pulse: 70,
      notes: ''
    });
    setEditingId(null);
  };

  const applyFilter = () => {
    loadHistory();
  };

  const resetFilter = () => {
    setStartDate('');
    setEndDate('');
    loadHistory();
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>Артериальное давление</h1>
      
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

      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '20px'
      }}>
        <div style={{
          background: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '20px' }}>
            {editingId ? 'Редактировать измерение' : 'Добавить измерение'}
          </h2>

          <form onSubmit={handleSubmit}>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr 1fr',
              gap: '15px',
              marginBottom: '15px'
            }}>
              <div>
                <label htmlFor="systolic" style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '500'
                }}>Систолическое</label>
                <input
                  type="number"
                  id="systolic"
                  name="systolic"
                  value={formData.systolic}
                  onChange={handleChange}
                  min="50"
                  max="250"
                  required
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              <div>
                <label htmlFor="diastolic" style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '500'
                }}>Диастолическое</label>
                <input
                  type="number"
                  id="diastolic"
                  name="diastolic"
                  value={formData.diastolic}
                  onChange={handleChange}
                  min="30"
                  max="150"
                  required
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
              <div>
                <label htmlFor="pulse" style={{
                  display: 'block',
                  marginBottom: '5px',
                  fontWeight: '500'
                }}>Пульс</label>
                <input
                  type="number"
                  id="pulse"
                  name="pulse"
                  value={formData.pulse}
                  onChange={handleChange}
                  min="30"
                  max="200"
                  style={{
                    width: '100%',
                    padding: '8px 12px',
                    border: '1px solid #ddd',
                    borderRadius: '4px',
                    fontSize: '14px'
                  }}
                />
              </div>
            </div>
            
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="notes" style={{
                display: 'block',
                marginBottom: '5px',
                fontWeight: '500'
              }}>Примечания</label>
              <textarea
                id="notes"
                name="notes"
                value={formData.notes}
                onChange={handleChange}
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
            
            <button 
              type="submit" 
              disabled={loading} 
              style={{
                backgroundColor: editingId ? '#ffc107' : '#007bff',
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
              {loading ? 'Сохранение...' : (editingId ? 'Обновить измерение' : 'Сохранить измерение')}
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

        <div style={{
          background: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '20px' }}>История измерений</h2>
          
          <div style={{ 
            marginBottom: '20px', 
            display: 'flex', 
            gap: '10px', 
            alignItems: 'flex-end',
            flexWrap: 'wrap'
          }}>
            <div>
              <label htmlFor="startDate">С</label>
              <input
                type="date"
                id="startDate"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                style={{ marginLeft: '5px', padding: '4px' }}
              />
            </div>
            <div>
              <label htmlFor="endDate">По</label>
              <input
                type="date"
                id="endDate"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
                style={{ marginLeft: '5px', padding: '4px' }}
              />
            </div>
            <button 
              onClick={applyFilter}
              style={{
                padding: '4px 12px',
                background: '#007bff',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Применить
            </button>
            <button 
              onClick={resetFilter}
              style={{
                padding: '4px 12px',
                background: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Сбросить
            </button>
          </div>

          {historyLoading ? (
            <LoadingSpinner />
          ) : history.length > 0 ? (
            <div style={{ maxHeight: '500px', overflowY: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead style={{ position: 'sticky', top: 0, background: 'white' }}>
                  <tr style={{ borderBottom: '2px solid #dee2e6' }}>
                    <th style={{ padding: '10px', textAlign: 'left' }}>Дата</th>
                    <th style={{ padding: '10px', textAlign: 'left' }}>Давление</th>
                    <th style={{ padding: '10px', textAlign: 'left' }}>Пульс</th>
                    <th style={{ padding: '10px', textAlign: 'left' }}>Примечания</th>
                    <th style={{ padding: '10px', textAlign: 'left' }}>Действия</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((item) => (
                    <tr key={item.id} style={{ borderBottom: '1px solid #dee2e6' }}>
                      <td style={{ padding: '10px' }}>
                        {new Date(item.date).toLocaleDateString('ru-RU')}
                        <br />
                        <small>
                          {new Date(item.date).toLocaleTimeString('ru-RU', { 
                            hour: '2-digit', 
                            minute: '2-digit' 
                          })}
                        </small>
                      </td>
                      <td style={{ padding: '10px', fontWeight: 'bold' }}>
                        {item.systolic}/{item.diastolic}
                      </td>
                      <td style={{ padding: '10px' }}>
                        {item.pulse || '-'}
                      </td>
                      <td style={{ padding: '10px', fontSize: '14px', color: '#666' }}>
                        {item.notes || '-'}
                      </td>
                      <td style={{ padding: '10px' }}>
                        <button
                          onClick={() => handleEdit(item)}
                          style={{
                            background: 'none',
                            border: '1px solid #ffc107',
                            color: '#ffc107',
                            padding: '4px 8px',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            marginRight: '5px',
                            fontSize: '12px'
                          }}
                        >
                          ✏️
                        </button>
                        <button
                          onClick={() => handleDelete(item.id)}
                          style={{
                            background: 'none',
                            border: '1px solid #dc3545',
                            color: '#dc3545',
                            padding: '4px 8px',
                            borderRadius: '4px',
                            cursor: 'pointer',
                            fontSize: '12px'
                          }}
                        >
                          🗑️
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p style={{ color: '#666', fontStyle: 'italic' }}>
              Нет сохраненных измерений
            </p>
          )}
        </div>
      </div>
    </div>
  );
};