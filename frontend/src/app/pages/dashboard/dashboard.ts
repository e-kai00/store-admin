import { CurrencyPipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';
import { finalize } from 'rxjs';
import { DashboardService } from '../../core/services/dashboard';
import { DashboardSummary } from '../../models/dashboard';

@Component({
  selector: 'app-dashboard',
  imports: [CurrencyPipe, MatButtonModule, MatProgressSpinnerModule, MatTableModule],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.scss',
})
export class Dashboard implements OnInit {
  private readonly dashboardService = inject(DashboardService);
  readonly displayedColumns = ['name', 'sku', 'stock', 'status'];

  readonly summary = signal<DashboardSummary | null>(null);

  readonly isLoading = signal(false);
  readonly errorMessage = signal<string | null>(null);

  ngOnInit(): void {
    this.loadSummary();
  }

  loadSummary(): void {
    this.isLoading.set(true);
    this.errorMessage.set(null);

    this.dashboardService
      .getSummary()
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (summary) => {
          this.summary.set(summary);
        },
        error: () => {
          this.errorMessage.set('Dashboard data could not be loaded.');
        },
      });
  }
}
