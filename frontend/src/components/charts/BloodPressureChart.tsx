import React from 'react';
import { BloodPressure } from '../../types';

interface BloodPressureChartProps {
  data: BloodPressure[];
}

export const BloodPressureChart: React.FC<BloodPressureChartProps> = ({ data }) => {
  if (data.length === 0) {
    return <div>Нет данных для построения графика</div>;
  }

  return (
    <div style={{ 
      background: 'white', 
      padding: '20px', 
      borderRadius: '8px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      marginTop: '20px'
    }}>
      <h3>Динамика артериального давления</h3>
      <div style={{
        display: 'flex',
        alignItems: 'flex-end',
        height: '200px',
        gap: '10px',
        padding: '20px',
        border: '1px solid #eee',
        borderRadius: '4px'
      }}>
        {data.slice(0, 10).map((item, index) => (
          <div key={index} style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            flex: 1
          }}>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              width: '100%'
            }}>
              <div style={{
                height: `${(item.systolic - 100) / 2}px`,
                width: '20px',
                background: '#8884d8',
                marginBottom: '2px'
              }} />
              <div style={{
                height: `${(item.diastolic - 60) / 2}px`,
                width: '20px',
                background: '#82ca9d'
              }} />
            </div>
            <div style={{
              fontSize: '12px',
              marginTop: '5px',
              transform: 'rotate(-45deg)',
              transformOrigin: 'top left'
            }}>
              {new Date(item.date).toLocaleDateString('ru-RU', { day: '2-digit', month: '2-digit' })}
            </div>
          </div>
        ))}
      </div>
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        marginTop: '20px',
        gap: '20px'
      }}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ 
            width: '20px', 
            height: '20px', 
            background: '#8884d8',
            marginRight: '5px'
          }} />
          <span>Систолическое</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ 
            width: '20px', 
            height: '20px', 
            background: '#82ca9d',
            marginRight: '5px'
          }} />
          <span>Диастолическое</span>
        </div>
      </div>
    </div>
  );
};