import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterLink } from '@angular/router';

import { EmployeeService } from '../../core/employee.service';
import { Employee } from '../../core/models/employee.models';

@Component({
  selector: 'app-employees',
  standalone: true,
  imports: [ReactiveFormsModule, RouterLink],
  templateUrl: './employees.component.html',
  styleUrl: './employees.component.css',
})
export class EmployeesComponent implements OnInit {
  private fb = inject(FormBuilder);
  private employees = inject(EmployeeService);

  rows = signal<Employee[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);
  saving = signal(false);
  showForm = signal(false);
  search = signal('');

  form = this.fb.nonNullable.group({
    first_name: ['', [Validators.required, Validators.maxLength(120)]],
    last_name: ['', [Validators.required, Validators.maxLength(120)]],
    age: [30, [Validators.required, Validators.min(16), Validators.max(100)]],
    transportation_expense: [0, [Validators.required, Validators.min(0)]],
    distance_to_work: [0, [Validators.required, Validators.min(0)]],
    daily_work_load_average: [0, [Validators.required, Validators.min(0)]],
    body_mass_index: [25, [Validators.required, Validators.min(0)]],
    education: [1, [Validators.required, Validators.min(0)]],
    pets: [0, [Validators.required, Validators.min(0)]],
  });

  ngOnInit(): void {
    this.load();
  }

  load(): void {
    this.loading.set(true);
    this.error.set(null);
    this.employees.list(this.search() || undefined).subscribe({
      next: (rows) => {
        this.rows.set(rows);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Impossible de charger les employés.');
        this.loading.set(false);
      },
    });
  }

  onSearch(value: string): void {
    this.search.set(value.trim());
    this.load();
  }

  toggleForm(): void {
    this.showForm.update((v) => !v);
  }

  submit(): void {
    if (this.form.invalid) {
      return;
    }
    this.saving.set(true);
    this.error.set(null);
    this.employees.create(this.form.getRawValue()).subscribe({
      next: () => {
        this.saving.set(false);
        this.showForm.set(false);
        this.form.reset({
          first_name: '', last_name: '', age: 30, transportation_expense: 0,
          distance_to_work: 0, daily_work_load_average: 0, body_mass_index: 25,
          education: 1, pets: 0,
        });
        this.load();
      },
      error: () => {
        this.saving.set(false);
        this.error.set('Création impossible (vérifie les champs).');
      },
    });
  }

  remove(emp: Employee): void {
    if (!confirm(`Supprimer ${emp.first_name} ${emp.last_name} ?`)) {
      return;
    }
    this.employees.delete(emp.id).subscribe({
      next: () => this.load(),
      error: () => this.error.set('Suppression impossible.'),
    });
  }
}