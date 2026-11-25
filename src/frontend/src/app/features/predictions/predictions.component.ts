import { DecimalPipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { EmployeeService } from '../../core/employee.service';
import { PredictionService } from '../../core/prediction.service';
import { Employee } from '../../core/models/employee.models';
import { PredictionItem, PredictionResult } from '../../core/models/prediction.models';

@Component({
  selector: 'app-predictions',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink, DecimalPipe],
  templateUrl: './predictions.component.html',
  styleUrl: './predictions.component.css',
})
export class PredictionsComponent implements OnInit {
  private fb = inject(FormBuilder);
  private employeeService = inject(EmployeeService);
  private predictionService = inject(PredictionService);

  employees = signal<Employee[]>([]);
  recent = signal<PredictionItem[]>([]);
  result = signal<PredictionResult | null>(null);
  loading = signal(true);
  saving = signal(false);
  error = signal<string | null>(null);

  form = this.fb.nonNullable.group({
    employee_id: [null as number | null, Validators.required],
    reason_for_absence: [26, [Validators.required, Validators.min(0), Validators.max(28)]],
    absence_date: ['', Validators.required],
  });

  ngOnInit(): void {
    this.employeeService.list().subscribe({
      next: (list) => {
        this.employees.set(list);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Impossible de charger les employés.');
        this.loading.set(false);
      },
    });
    this.loadRecent();
  }

  /** Recharge l'historique (appelé au démarrage et après chaque prédiction). */
  loadRecent(): void {
    this.predictionService.list(20).subscribe({
      next: (list) => this.recent.set(list),
      error: () => {},
    });
  }

  submit(): void {
    if (this.form.invalid) {
      return;
    }
    this.saving.set(true);
    this.error.set(null);
    this.result.set(null);
    const v = this.form.getRawValue();
    this.predictionService
      .predict({
        employee_id: v.employee_id!,
        reason_for_absence: v.reason_for_absence,
        absence_date: v.absence_date,
      })
      .subscribe({
        next: (r) => {
          this.result.set(r);
          this.saving.set(false);
          this.loadRecent();
        },
        error: () => {
          this.error.set('La prédiction a échoué.');
          this.saving.set(false);
        },
      });
  }

  /** Nom lisible d'un employé à partir de son id (pour l'historique). */
  employeeName(id: number | null): string {
    if (id == null) {
      return '—';
    }
    const e = this.employees().find((x) => x.id === id);
    return e ? `${e.first_name} ${e.last_name}` : `#${id}`;
  }
}