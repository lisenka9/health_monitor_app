import React, { useState, useEffect } from 'react';
import { DashboardData, BloodPressure } from '../types';
import { measurementsService } from '../services/measurements';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { useNavigate } from 'react-router-dom';

export const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const loadDashboardData = async () => {
      try {
        const data = await measurementsService.getDashboardData();
        setDashboardData(data);
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    loadDashboardData();
  }, []);

  const handleAddMeasurement = (type: string) => {
    navigate(`/${type}`);
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>Дашборд</h1>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
        gap: '20px' 
      }}>
        <div style={{
          background: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '15px' }}>Быстрое добавление</h2>
          <button 
            onClick={() => handleAddMeasurement('blood-pressure')}
            style={{
              width: '100%',
              padding: '10px',
              marginBottom: '10px',
              background: '#007bff',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            📊 Добавить давление
          </button>
          <button 
            onClick={() => handleAddMeasurement('blood-glucose')}
            style={{
              width: '100%',
              padding: '10px',
              marginBottom: '10px',
              background: '#28a745',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            🩸 Добавить глюкозу
          </button>
          <button 
            onClick={() => handleAddMeasurement('weight')}
            style={{
              width: '100%',
              padding: '10px',
              marginBottom: '10px',
              background: '#ffc107',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            ⚖️ Добавить вес
          </button>
        </div>

        <div style={{
          background: 'white',
          padding: '20px',
          borderRadius: '8px',
          boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
        }}>
          <h2 style={{ marginBottom: '15px' }}>Последние измерения</h2>
          
          {dashboardData?.latest_blood_pressure && (
            <div style={{ 
              background: '#e8f4fd', 
              padding: '15px', 
              borderRadius: '4px',
              marginBottom: '10px'
            }}>
              <h3 style={{ margin: '0 0 5px 0' }}>Артериальное давление</h3>
              <p style={{ margin: '0', fontSize: '18px', fontWeight: 'bold' }}>
                {dashboardData.latest_blood_pressure.systolic}/
                {dashboardData.latest_blood_pressure.diastolic} mmHg
              </p>
              <small>
                {new Date(dashboardData.latest_blood_pressure.date).toLocaleDateString()}
              </small>
            </div>
          )}

          {dashboardData?.latest_blood_glucose && (
            <div style={{ 
              background: '#f0f9f0', 
              padding: '15px', 
              borderRadius: '4px',
              marginBottom: '10px'
            }}>
              <h3 style={{ margin: '0 0 5px 0' }}>Уровень глюкозы</h3>
              <p style={{ margin: '0', fontSize: '18px', fontWeight: 'bold' }}>
                {dashboardData.latest_blood_glucose.value} {dashboardData.latest_blood_glucose.unit}
              </p>
              <small>
                {new Date(dashboardData.latest_blood_glucose.date).toLocaleDateString()}
              </small>
            </div>
          )}

          {dashboardData?.latest_weight && (
            <div style={{ 
              background: '#fff3cd', 
              padding: '15px', 
              borderRadius: '4px',
              marginBottom: '10px'
            }}>
              <h3 style={{ margin: '0 0 5px 0' }}>Вес</h3>
              <p style={{ margin: '0', fontSize: '18px', fontWeight: 'bold' }}>
                {dashboardData.latest_weight.value} {dashboardData.latest_weight.unit}
              </p>
              <small>
                {new Date(dashboardData.latest_weight.date).toLocaleDateString()}
              </small>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};