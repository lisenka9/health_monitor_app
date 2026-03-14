import api from './api';
import {
  BloodPressure,
  BloodPressureCreate,
  BloodGlucose,
  BloodGlucoseCreate,
  Weight,
  WeightCreate,
  WellnessEntry,
  WellnessEntryCreate,
  MeasurementFilter,
  DashboardData
} from '../types';

export const measurementsService = {
  async createBloodPressure(data: BloodPressureCreate): Promise<BloodPressure> {
    const response = await api.post<BloodPressure>('/api/blood-pressure', data);
    return response.data;
  },

  async getBloodPressureHistory(skip: number = 0, limit: number = 100): Promise<BloodPressure[]> {
    const response = await api.get<BloodPressure[]>(`/api/blood-pressure?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  async createBloodGlucose(data: BloodGlucoseCreate): Promise<BloodGlucose> {
    const response = await api.post<BloodGlucose>('/api/blood-glucose', data);
    return response.data;
  },

  async getBloodGlucoseHistory(skip: number = 0, limit: number = 100): Promise<BloodGlucose[]> {
    const response = await api.get<BloodGlucose[]>(`/api/blood-glucose?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  async createWeight(data: WeightCreate): Promise<Weight> {
    const response = await api.post<Weight>('/api/weight', data);
    return response.data;
  },

  async getWeightHistory(skip: number = 0, limit: number = 100): Promise<Weight[]> {
    const response = await api.get<Weight[]>(`/api/weight?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  async createWellnessEntry(data: WellnessEntryCreate): Promise<WellnessEntry> {
    const response = await api.post<WellnessEntry>('/api/wellness', data);
    return response.data;
  },

  async getWellnessHistory(skip: number = 0, limit: number = 100): Promise<WellnessEntry[]> {
    const response = await api.get<WellnessEntry[]>(`/api/wellness?skip=${skip}&limit=${limit}`);
    return response.data;
  },
  async getMeasurementsForPeriod(filters: MeasurementFilter): Promise<any> {
    const params = new URLSearchParams();
    if (filters.start_date) params.append('start_date', filters.start_date);
    if (filters.end_date) params.append('end_date', filters.end_date);
    if (filters.type) params.append('measurement_type', filters.type);

    const response = await api.get(`/api/analytics/measurements?${params}`);
    return response.data;
  },

  async getMeasurementsStats(days: number = 30): Promise<any> {
    const response = await api.get(`/api/analytics/stats?days=${days}`);
    return response.data;
  },

  async getDashboardData(): Promise<DashboardData> {
    const response = await api.get<DashboardData>('/api/analytics/dashboard');
    return response.data;
  },

  async updateWellnessEntry(id: number, data: WellnessEntryCreate): Promise<WellnessEntry> {
    const response = await api.put<WellnessEntry>(`/api/wellness/${id}`, data);
    return response.data;
  },

  async deleteWellnessEntry(id: number): Promise<void> {
    await api.delete(`/api/wellness/${id}`);
  },
  async updateBloodPressure(id: number, data: BloodPressureCreate): Promise<BloodPressure> {
    const response = await api.put<BloodPressure>(`/api/blood-pressure/${id}`, data);
    return response.data;
  },

  async deleteBloodPressure(id: number): Promise<void> {
    await api.delete(`/api/blood-pressure/${id}`);
  },

  async updateBloodGlucose(id: number, data: BloodGlucoseCreate): Promise<BloodGlucose> {
    const response = await api.put<BloodGlucose>(`/api/blood-glucose/${id}`, data);
    return response.data;
  },

  async deleteBloodGlucose(id: number): Promise<void> {
    await api.delete(`/api/blood-glucose/${id}`);
  },

  async updateWeight(id: number, data: WeightCreate): Promise<Weight> {
    const response = await api.put<Weight>(`/api/weight/${id}`, data);
    return response.data;
  },

  async deleteWeight(id: number): Promise<void> {
    await api.delete(`/api/weight/${id}`);
  }
};