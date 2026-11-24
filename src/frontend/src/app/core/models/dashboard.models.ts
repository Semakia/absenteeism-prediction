export interface ReasonGroupBreakdown {
  reason_group: number;
  count: number;
}

export interface MonthlyAverage {
  month: number;
  average_hours: number;
}

export interface ModelInfo {
  version: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  trained_at: string;
}

export interface DashboardStats {
  total_employees: number;
  total_predictions: number;
  total_absence_records: number;
  excessive_rate: number;
  reason_breakdown: ReasonGroupBreakdown[];
  monthly_average_hours: MonthlyAverage[];
  active_model: ModelInfo | null;
}