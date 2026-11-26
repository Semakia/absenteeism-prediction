import { Component, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { AuthService } from '../core/auth.service';

/**
 * Coquille applicative (shell) : barre latérale de navigation fixe +
 * zone de contenu scrollable qui accueille les pages via <router-outlet>.
 * Enveloppe toutes les routes authentifiées (dashboard, employés, prédictions).
 * L'écran de login reste en dehors de ce shell.
 */
@Component({
  selector: 'app-shell',
  standalone: true,
  imports: [RouterOutlet, RouterLink, RouterLinkActive],
  templateUrl: './shell.component.html',
  styleUrl: './shell.component.css',
})
export class ShellComponent {
  private auth = inject(AuthService);
  private router = inject(Router);

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
