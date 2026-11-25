export interface Employee {
  id: number;
  first_name: string;
  last_name: string;
  transportation_expense: number;
  distance_to_work: number;
  age: number;
  daily_work_load_average: number;
  body_mass_index: number;
  education: number;
  pets: number;
  created_at: string;
  updated_at: string;
}

export type EmployeeCreate = Omit<Employee, 'id' | 'created_at' | 'updated_at'>;