import { DecimalPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../../core/auth.service';
import { DashboardService } from '../../core/dashboard.service';
import { DashboardStats } from '../../core/models/dashboard.models';
import { RouterLink } from '@angular/router';
import { TourService } from '../../core/tour.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [DecimalPipe, RouterLink],
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css',
})
export class DashboardComponent implements OnInit {
  private auth = inject(AuthService);
  private router = inject(Router);
  private dashboard = inject(DashboardService);
  private tour = inject(TourService);

  stats = signal<DashboardStats | null>(null);
  error = signal<string | null>(null);
  loading = signal(true);

  ngOnInit(): void {
    this.dashboard.getStats().subscribe({
      next: (s) => {
        this.stats.set(s);
        this.loading.set(false);
        // Lance la visite guidée au tout premier passage (une seule fois).
        this.tour.maybeAutoStart();
      },
      error: () => {
        this.error.set('Impossible de charger les statistiques.');
        this.loading.set(false);
      },
    });
  }

  /** Valeur max des motifs, pour dimensionner les barres (évite /0). */
  maxReason(): number {
    const s = this.stats();
    return s && s.reason_breakdown.length
      ? Math.max(...s.reason_breakdown.map((r) => r.count))
      : 1;
  }

  maxMonthly(): number {
    const s = this.stats();
    return s && s.monthly_average_hours.length
      ? Math.max(...s.monthly_average_hours.map((m) => m.average_hours))
      : 1;
  }

  monthLabel(month: number): string {
    const names = ['', 'Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin', 'Juil', 'Août', 'Sep', 'Oct', 'Nov', 'Déc'];
    return names[month] ?? String(month);
  }

  /** Relance la visite guidée à la demande (bouton de l'en-tête). */
  startTour(): void {
    this.tour.start();
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}