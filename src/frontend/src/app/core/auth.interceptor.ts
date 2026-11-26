import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { catchError, throwError } from 'rxjs';

/**
 * Attache le JWT à chaque requête sortante s'il est présent, et gère
 * l'expiration : si le backend répond 401, le token est effacé et
 * l'utilisateur est renvoyé vers l'écran de login (évite de rester
 * bloqué sur des pages qui échouent en silence).
 */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const router = inject(Router);
  const token = localStorage.getItem('access_token');
  if (token) {
    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }
  return next(req).pipe(
    catchError((err: HttpErrorResponse) => {
      if (err.status === 401) {
        localStorage.removeItem('access_token');
        router.navigate(['/login']);
      }
      return throwError(() => err);
    }),
  );
};
