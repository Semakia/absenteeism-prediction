import { HttpClient, HttpParams } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, tap } from 'rxjs';

import { environment } from '../../environments/environment';

interface LoginResponse {
  access_token: string;
  token_type: string;
}

const TOKEN_KEY = 'access_token';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);

  /** Authentifie l'utilisateur et stocke le JWT renvoyé par le backend. */
  login(email: string, password: string): Observable<LoginResponse> {
    // OAuth2PasswordRequestForm => corps form-urlencoded, champs username/password.
    const body = new HttpParams()
      .set('username', email)
      .set('password', password)
      .toString();

    return this.http
      .post<LoginResponse>(`${environment.apiUrl}/auth/login`, body, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      .pipe(tap((res) => localStorage.setItem(TOKEN_KEY, res.access_token)));
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  isLoggedIn(): boolean {
    return this.getToken() !== null;
  }
}
