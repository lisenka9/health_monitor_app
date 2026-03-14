export interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  created_at: string;
}

export interface BloodPressure {
  id: number;
  user_id: number;
  systolic: number;
  diastolic: number;
  pulse?: number;
  date: string;
  notes?: string;
}

export interface BloodPressureCreate {
  systolic: number;
  diastolic: number;
  pulse?: number;
  notes?: string;
}

export interface BloodGlucose {
  id: number;
  user_id: number;
  value: number;
  unit: string;
  date: string;
  notes?: string;
}

export interface BloodGlucoseCreate {
  value: number;
  unit: string;
  notes?: string;
}

export interface Weight {
  id: number;
  user_id: number;
  value: number;
  unit: string;
  date: string;
  notes?: string;
}

export interface WeightCreate {
  value: number;
  unit: string;
  notes?: string;
}

export interface WellnessEntry {
  id: number;
  user_id: number;
  description?: string;
  mood?: string;
  symptoms?: string;
  date: string;
}

export interface WellnessEntryCreate {
  description?: string;
  mood?: string;
  symptoms?: string;
}

export interface MeasurementFilter {
  start_date?: string;
  end_date?: string;
  type?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  password: string;
  full_name: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
}

export interface DashboardData {
  latest_blood_pressure?: BloodPressure;
  latest_blood_glucose?: BloodGlucose;
  latest_weight?: Weight;
  weekly_stats: any;
}