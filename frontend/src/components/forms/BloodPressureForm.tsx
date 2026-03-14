import React, { useState } from 'react';
import { BloodPressureCreate } from '../../types';
import { measurementsService } from '../../services/measurements';
import './Forms.css';

interface BloodPressureFormProps {
  onSuccess: () => void;
}

export const BloodPressureForm: React.FC<BloodPressureFormProps> = ({ onSuccess }) => {
  const [formData, setFormData] = useState<BloodPressureCreate>({
    systolic: 120,
    diastolic: 80,
    pulse: 70,
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

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

    try {
      await measurementsService.createBloodPressure(formData);
      onSuccess();
      setFormData({
        systolic: 120,
        diastolic: 80,
        pulse: 70,
        notes: ''
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Ошибка сохранения');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form">
      <h3>Добавить измерение давления</h3>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="form-row">
        <div className="form-group">
          <label htmlFor="systolic">Систолическое (верхнее)</label>
          <input
            type="number"
            id="systolic"
            name="systolic"
            value={formData.systolic}
            onChange={handleChange}
            min="50"
            max="250"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="diastolic">Диастолическое (нижнее)</label>
          <input
            type="number"
            id="diastolic"
            name="diastolic"
            value={formData.diastolic}
            onChange={handleChange}
            min="30"
            max="150"
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="pulse">Пульс</label>
          <input
            type="number"
            id="pulse"
            name="pulse"
            value={formData.pulse}
            onChange={handleChange}
            min="30"
            max="200"
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="notes">Примечания</label>
        <textarea
          id="notes"
          name="notes"
          value={formData.notes}
          onChange={handleChange}
          rows={3}
        />
      </div>

      <button type="submit" disabled={loading} className="submit-btn">
        {loading ? 'Сохранение...' : 'Сохранить'}
      </button>
    </form>
  );
};