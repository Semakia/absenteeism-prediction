import { HttpInterceptorFn } from '@angular/common/http';

/** Attache le JWT a chaque requete sortante s'il est present. */
export const authInterceptor: HttpInterceptorFn = (req, next) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    req = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });
  }
  return next(req);
};