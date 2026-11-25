import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable } from 'rxjs';

import { environment } from '../../environments/environment';
import { PredictRequest, PredictionItem, PredictionResult } from './models/prediction.models';

@Injectable({ providedIn: 'root' })
export class PredictionService {
  private http = inject(HttpClient);
  private base = `${environment.apiUrl}/predictions`;

  /** Score une absence pour un employé existant et l'archive côté backend. */
  predict(payload: PredictRequest): Observable<PredictionResult> {
    return this.http.post<PredictionResult>(`${this.base}/predict`, payload);
  }

  /** Historique des prédictions, plus récentes d'abord. */
  list(limit = 20): Observable<PredictionItem[]> {
    const params = new HttpParams().set('limit', limit);
    return this.http.get<PredictionItem[]>(this.base, { params });
  }
}