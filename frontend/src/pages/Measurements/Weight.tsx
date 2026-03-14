import React, { useState, useEffect } from 'react';
import { Weight as WeightType, WeightCreate } from '../../types';
import { measurementsService } from '../../services/measurements';
import { LoadingSpinner } from '../../components/common/LoadingSpinner';

export const WeightPage: React.FC = () => {
  const [startDate, setStartDate] = useState<string>('');
  const [endDate, setEndDate] = useState<string>('');
  const [formData, setFormData] = useState<WeightCreate>({
    value: 50,
    unit: 'kg',
    notes: ''
  });
  const [history, setHistory] = useState<WeightType[]>([]);
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
      const data = await measurementsService.getWeightHistory();
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

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'value' ? parseFloat(value) || 0 : value
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    try {
      if (editingId) {
        await measurementsService.updateWeight(editingId, formData);
        setSuccess('Вес успешно обновлен!');
        setEditingId(null);
      } else {
        await measurementsService.createWeight(formData);
        setSuccess('Вес успешно сохранен!');
      }
      
      setFormData({
        value: 50,
        unit: 'kg',
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

  const handleEdit = (item: WeightType) => {
    setFormData({
      value: item.value,
      unit: item.unit,
      notes: item.notes || ''
    });
    setEditingId(item.id);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Вы уверены, что хотите удалить это измерение?')) {
      try {
        await measurementsService.deleteWeight(id);
        await loadHistory();
        setSuccess('Вес успешно удален!');
      } catch (error) {
        console.error('Error deleting measurement:', error);
        setError('Ошибка при удалении измерения');
      }
    }
  };

  const handleCancelEdit = () => {
    setFormData({
      value: 50,
      unit: 'kg',
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

  const formatValue = (value: number, unit: string) => {
    return `${value} ${unit === 'kg' ? 'кг' : 'фунтов'}`;
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>Вес</h1>
      
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
        <div style={{ 
          background: 'white', 
          padding: '20px', 
          borderRadius: '8px', 
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)' 
        }}>
          <h2 style={{ marginBottom: '20px' }}>
            {editingId ? 'Редактировать вес' : 'Добавить вес'}
          </h2>

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="value" style={{ 
                display: 'block', 
                marginBottom: '5px', 
                fontWeight: '500' 
              }}>
                Вес
              </label>
              <input
                type="number"
                id="value"
                name="value"
                value={formData.value}
                onChange={handleChange}
                step="0.1"
                min="20"
                max="300"
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
            
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="unit" style={{ 
                display: 'block', 
                marginBottom: '5px', 
                fontWeight: '500' 
              }}>
                Единица измерения
              </label>
              <select
                id="unit"
                name="unit"
                value={formData.unit}
                onChange={handleChange}
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: '1px solid #ddd', 
                  borderRadius: '4px', 
                  fontSize: '14px' 
                }}
              >
                <option value="kg">Килограммы (кг)</option>
                <option value="lb">Фунты (lb)</option>
              </select>
            </div>
            
            <div style={{ marginBottom: '15px' }}>
              <label htmlFor="notes" style={{ 
                display: 'block', 
                marginBottom: '5px', 
                fontWeight: '500' 
              }}>
                Примечания
              </label>
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
                backgroundColor: editingId ? '#ffc107' : '#ffc107',
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
              {loading ? 'Сохранение...' : (editingId ? 'Обновить вес' : 'Сохранить вес')}
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
                background: '#ffc107',
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
                    <th style={{ padding: '10px', textAlign: 'left' }}>Вес</th>
                    <th style={{ padding: '10px', textAlign: 'left' }}>Единица</th>
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
                        {item.value}
                      </td>
                      <td style={{ padding: '10px' }}>
                        {item.unit === 'kg' ? 'кг' : 'фунты'}
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