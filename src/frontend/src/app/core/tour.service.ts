import { Injectable } from '@angular/core';
import { driver } from 'driver.js';
import 'driver.js/dist/driver.css';

/**
 * Visite guidée interactive (basée sur driver.js).
 * Met en surbrillance les éléments réels de l'interface, étape par étape.
 * Se lance automatiquement au tout premier passage sur le dashboard
 * (mémorisé dans localStorage), ou manuellement via le bouton « Visite guidée ».
 *
 * Les cibles sont désignées par des attributs `data-tour="..."` posés sur
 * les éléments (sidebar dans le shell, sections du dashboard).
 */
@Injectable({ providedIn: 'root' })
export class TourService {
  private readonly SEEN_KEY = 'tour_seen';

  /** Lance la visite immédiatement. */
  start(): void {
    const tour = driver({
      showProgress: true,
      allowClose: true,
      popoverClass: 'app-tour',
      nextBtnText: 'Suivant →',
      prevBtnText: '← Précédent',
      doneBtnText: 'Terminer',
      progressText: 'Étape {{current}} / {{total}}',
      steps: [
        {
          element: '[data-tour="brand"]',
          popover: {
            title: 'Bienvenue 👋',
            description: "Cet outil prédit si une absence risque d'être « excessive ». Voici une visite rapide des écrans.",
          },
        },
        {
          element: '[data-tour="nav"]',
          popover: {
            title: 'Navigation',
            description: 'Passe d\'un écran à l\'autre ici : Dashboard, Employés, Prédictions et le Guide.',
          },
        },
        {
          element: '[data-tour="tiles"]',
          popover: {
            title: 'Chiffres clés',
            description: 'Les totaux d\'employés, d\'absences, de prédictions et le taux d\'absences « excessives ».',
          },
        },
        {
          element: '[data-tour="model"]',
          popover: {
            title: 'Modèle actif',
            description: 'La performance du modèle entraîné (accuracy, precision, recall, F1, ROC AUC). Détails dans le Guide.',
          },
        },
        {
          element: '[data-tour="reasons"]',
          popover: {
            title: 'Groupes de motifs',
            description: 'Les absences réparties par groupe de motif. Le lien « Que signifient les groupes ? » ouvre le Guide.',
          },
        },
        {
          element: '[data-tour="nav-predictions"]',
          popover: {
            title: 'À toi de jouer',
            description: 'Ouvre « Prédictions » pour scorer une absence : choisis un employé, un motif, une date, puis « Prédire ».',
          },
        },
      ],
    });
    tour.drive();
    this.markSeen();
  }

  /** Lance la visite seulement si l'utilisateur ne l'a jamais vue. */
  maybeAutoStart(): void {
    if (this.hasSeen()) {
      return;
    }
    // Petit délai : laisse Angular peindre les éléments du dashboard.
    setTimeout(() => this.start(), 450);
  }

  private hasSeen(): boolean {
    try {
      return localStorage.getItem(this.SEEN_KEY) === '1';
    } catch {
      return false;
    }
  }

  private markSeen(): void {
    try {
      localStorage.setItem(this.SEEN_KEY, '1');
    } catch {
      /* localStorage indisponible : on ignore. */
    }
  }
}
