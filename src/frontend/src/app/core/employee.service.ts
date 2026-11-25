import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { Employee, EmployeeCreate } from './models/employee.models';

@Injectable({ providedIn: 'root' })
export class EmployeeService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/employees`;

  /** Liste les employés, filtrée par nom si `search` est fourni. */
  list(search?: string): Observable<Employee[]> {
    let params = new HttpParams();
    if (search) {
      params = params.set('search', search);
    }
    return this.http.get<Employee[]>(this.base, { params });
  }

  create(payload: EmployeeCreate): Observable<Employee> {
    return this.http.post<Employee>(this.base, payload);
  }

  delete(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}