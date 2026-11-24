import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [],
  template: `
    <div style="padding:32px;font-family:system-ui">
      <h1>Dashboard</h1>
      <p>✅ Connecté. Le token JWT est stocké et envoyé sur chaque appel API.</p>
      <button (click)="logout()">Se déconnecter</button>
    </div>
  `,
})
export class DashboardComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}