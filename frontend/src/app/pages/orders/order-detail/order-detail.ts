import { CurrencyPipe, DatePipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatTableModule } from '@angular/material/table';
import { finalize } from 'rxjs';
import { OrdersService } from '../../../core/services/orders';
import { Order } from '../../../models/order';
import { N } from '@angular/cdk/keycodes';

@Component({
  selector: 'app-order-detail',
  imports: [
    CurrencyPipe,
    DatePipe,
    MatButtonModule,
    MatProgressSpinnerModule,
    MatTableModule,
    RouterLink,
  ],
  templateUrl: './order-detail.html',
  styleUrl: './order-detail.scss',
})
export class OrderDetail implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly ordersService = inject(OrdersService);

  readonly displayedColumns = ['product', 'quantity', 'unitPrice', 'lineTotal'];
  readonly order = signal<Order | null>(null);
  readonly isLoading = signal(false);
  readonly errorMsg = signal<string | null>(null);

  ngOnInit(): void {
    this.loadOrder();
  }

  loadOrder(): void {
    const orderId = Number(this.route.snapshot.paramMap.get('orderId'));
    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.ordersService
      .getOrder(orderId)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (order) => {
          this.order.set(order);
        },
        error: () => {
          this.errorMsg.set('Order could not be loaded.');
        },
      });
  }
}
