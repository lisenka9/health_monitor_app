import React, { useState, useEffect } from 'react';
import { measurementsService } from '../services/measurements';
import { LoadingSpinner } from '../components/common/LoadingSpinner';
import { MeasurementFilter } from '../types';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';

export const Analytics: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [stats, setStats] = useState<any>(null);
  const [measurements, setMeasurements] = useState<any[]>([]);
  const [chartType, setChartType] = useState<'pressure' | 'glucose' | 'weight'>('pressure');

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const statsData = await measurementsService.getMeasurementsStats(30);
      setStats(statsData);

      const measurementsData = await measurementsService.getMeasurementsForPeriod({
        start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString(),
        end_date: new Date().toISOString()
      });
      console.log('Measurements data:', measurementsData);

      setMeasurements(measurementsData.data || measurementsData || []);
    } catch (error) {
      console.error('Error loading data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPressureChartData = () => {
    const pressureData = measurements.filter(m => m.type === 'blood_pressure');
    return pressureData.slice(-15).map(item => ({
      date: new Date(item.date).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }),
      systolic: item.systolic,
      diastolic: item.diastolic,
      pulse: item.pulse
    }));
  };

  const getGlucoseChartData = () => {
    const glucoseData = measurements.filter(m => m.type === 'blood_glucose');
    return glucoseData.slice(-15).map(item => ({
      date: new Date(item.date).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }),
      glucose: item.value
    }));
  };

  const getWeightChartData = () => {
    const weightData = measurements.filter(m => m.type === 'weight');
    return weightData.slice(-15).map(item => ({
      date: new Date(item.date).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' }),
      weight: item.value
    }));
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '20px' }}>Аналитика и графики</h1>

      {loading ? (
        <LoadingSpinner />
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '30px' }}>
          <div style={{
            background: 'white',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
            display: 'flex',
            gap: '10px',
            flexWrap: 'wrap'
          }}>
            <button 
              onClick={() => setChartType('pressure')}
              style={{
                padding: '10px 20px',
                background: chartType === 'pressure' ? '#007bff' : '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              📈 Давление
            </button>
            <button 
              onClick={() => setChartType('glucose')}
              style={{
                padding: '10px 20px',
                background: chartType === 'glucose' ? '#28a745' : '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              🩸 Глюкоза
            </button>
            <button 
              onClick={() => setChartType('weight')}
              style={{
                padding: '10px 20px',
                background: chartType === 'weight' ? '#ffc107' : '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              ⚖️ Вес
            </button>
          </div>
          <div style={{
            background: 'white',
            padding: '20px',
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            <h2 style={{ marginBottom: '20px' }}>
              {chartType === 'pressure' && 'Динамика артериального давления'}
              {chartType === 'glucose' && 'Динамика уровня глюкозы'}
              {chartType === 'weight' && 'Динамика веса'}
            </h2>
            
            <div style={{ height: '300px' }}>
              {chartType === 'pressure' && getPressureChartData().length > 0 && (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={getPressureChartData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="systolic" stroke="#8884d8" name="Систолическое" />
                    <Line type="monotone" dataKey="diastolic" stroke="#82ca9d" name="Диастолическое" />
                  </LineChart>
                </ResponsiveContainer>
              )}
              
              {chartType === 'glucose' && getGlucoseChartData().length > 0 && (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={getGlucoseChartData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="glucose" stroke="#28a745" name="Глюкоза" />
                  </LineChart>
                </ResponsiveContainer>
              )}
              
              {chartType === 'weight' && getWeightChartData().length > 0 && (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={getWeightChartData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="weight" fill="#ffc107" name="Вес" />
                  </BarChart>
                </ResponsiveContainer>
              )}
              
              {(!getPressureChartData().length && !getGlucoseChartData().length && !getWeightChartData().length) && (
                <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
                  <p style={{ color: '#666', fontStyle: 'italic' }}>Нет данных для построения графика</p>
                </div>
              )}
            </div>
          </div>
          {stats && (
            <div style={{
              background: 'white',
              padding: '20px',
              borderRadius: '8px',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h2 style={{ marginBottom: '20px' }}>Статистика за {stats.period_days} дней</h2>
              
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
                gap: '20px'
              }}>
                {stats.stats.blood_pressure?.avg_systolic && (
                  <div style={{
                    background: '#e8f4fd',
                    padding: '15px',
                    borderRadius: '4px'
                  }}>
                    <h3 style={{ margin: '0 0 10px 0' }}>Артериальное давление</h3>
                    <p style={{ margin: '5px 0' }}>Среднее: <strong>{stats.stats.blood_pressure.avg_systolic?.toFixed(1)}/{stats.stats.blood_pressure.avg_diastolic?.toFixed(1)}</strong></p>
                    <p style={{ margin: '5px 0' }}>Пульс: <strong>{stats.stats.blood_pressure.avg_pulse?.toFixed(0) || '-'}</strong></p>
                  </div>
                )}

                {stats.stats.blood_glucose?.avg && (
                  <div style={{
                    background: '#f0f9f0',
                    padding: '15px',
                    borderRadius: '4px'
                  }}>
                    <h3 style={{ margin: '0 0 10px 0' }}>Уровень глюкозы</h3>
                    <p style={{ margin: '5px 0' }}>Среднее: <strong>{stats.stats.blood_glucose.avg.toFixed(1)}</strong></p>
                    <p style={{ margin: '5px 0' }}>Диапазон: <strong>{stats.stats.blood_glucose.min.toFixed(1)} - {stats.stats.blood_glucose.max.toFixed(1)}</strong></p>
                  </div>
                )}

                {stats.stats.weight?.avg && (
                  <div style={{
                    background: '#fff3cd',
                    padding: '15px',
                    borderRadius: '4px'
                  }}>
                    <h3 style={{ margin: '0 0 10px 0' }}>Вес</h3>
                    <p style={{ margin: '5px 0' }}>Среднее: <strong>{stats.stats.weight.avg.toFixed(1)}</strong></p>
                    <p style={{ margin: '5px 0' }}>Диапазон: <strong>{stats.stats.weight.min.toFixed(1)} - {stats.stats.weight.max.toFixed(1)}</strong></p>
                  </div>
                )}

                {stats.stats.wellness_entries > 0 && (
                  <div style={{
                    background: '#f8f9fa',
                    padding: '15px',
                    borderRadius: '4px'
                  }}>
                    <h3 style={{ margin: '0 0 10px 0' }}>Самочувствие</h3>
                    <p style={{ margin: '5px 0' }}>Записей: <strong>{stats.stats.wellness_entries}</strong></p>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};