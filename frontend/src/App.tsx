import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { Header } from './components/common/Header';
import { ProtectedRoute } from './components/common/ProtectedRoute';
import { Login } from './pages/Login';
import { Register } from './pages/Register';
import { Dashboard } from './pages/Dashboard';
import { WellnessPage } from './pages/Wellness';
import { Analytics } from './pages/Analytics';
import { BloodPressurePage } from './pages/Measurements/BloodPressure';
import { BloodGlucosePage } from './pages/Measurements/BloodGlucose';
import { WeightPage } from './pages/Measurements/Weight';
import { ProfilePage } from './pages/Profile';

function App() {
  return (
    <Router>
      <AuthProvider> {/* AuthProvider теперь внутри Router */}
        <div className="App" style={{ minHeight: '100vh' }}>
          <Header />
          <main style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              
              <Route path="/" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              
              <Route path="/dashboard" element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              } />
              
              <Route path="/blood-pressure" element={
                <ProtectedRoute>
                  <BloodPressurePage />
                </ProtectedRoute>
              } />
              
              <Route path="/blood-glucose" element={
                <ProtectedRoute>
                  <BloodGlucosePage />
                </ProtectedRoute>
              } />
              
              <Route path="/weight" element={
                <ProtectedRoute>
                  <WeightPage />
                </ProtectedRoute>
              } />
              
              <Route path="/wellness" element={
                <ProtectedRoute>
                  <WellnessPage />
                </ProtectedRoute>
              } />
              
              <Route path="/analytics" element={
                <ProtectedRoute>
                  <Analytics />
                </ProtectedRoute>
              } />
              
              <Route path="/profile" element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } />
            </Routes>
          </main>
        </div>
      </AuthProvider>
    </Router>
  );
}

export default App;