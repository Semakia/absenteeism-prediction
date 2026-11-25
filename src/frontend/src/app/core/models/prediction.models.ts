export interface PredictionResult {
  probability: number;
  is_excessive: boolean;
  model_version: string;
}

export interface PredictionItem {
  id: number;
  employee_id: number | null;
  reason_for_absence: number;
  absence_date: string;
  input_features: Record<string, number>;
  probability: number;
  is_excessive: boolean;
  model_version: string;
  created_at: string;
}

export interface PredictRequest {
  employee_id: number;
  reason_for_absence: number;
  absence_date: string;
}