import React from 'react';

export const LoadingSpinner: React.FC = () => {
  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', padding: '20px' }}>
      <div>Загрузка...</div>
    </div>
  );
};