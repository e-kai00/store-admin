import { CurrencyPipe, DatePipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatPaginatorModule, PageEvent } from '@angular/material/paginator';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { finalize } from 'rxjs';
import { OrdersService } from '../../core/services/orders';
import { Order, OrderCreate, OrderStatus } from '../../models/order';
import { OrderStatusDialog } from './order-status-dialog/order-status-dialog';
import { OrderCreateDialog } from './order-create-dialog/order-create-dialog';

@Component({
  selector: 'app-orders',
  imports: [
    CurrencyPipe,
    DatePipe,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatTableModule,
    MatIconModule,
    MatMenuModule,
    RouterLink,
    MatDialogModule,
  ],
  templateUrl: './orders.html',
  styleUrl: './orders.scss',
})
export class Orders implements OnInit {
  private readonly ordersService = inject(OrdersService);

  readonly displayedColumns = [
    'orderNumber',
    'customer',
    'createdAt',
    'items',
    'total',
    'status',
    'actions',
  ];
  readonly statuses: OrderStatus[] = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];

  readonly isLoading = signal(false);
  readonly updatingOrderId = signal<number | null>(null);
  readonly errorMsg = signal<string | null>(null);
  private readonly dialog = inject(MatDialog);

  readonly orders = signal<Order[]>([]);
  readonly total = signal(0);
  readonly search = signal('');
  readonly statusFilter = signal<OrderStatus | ''>('');
  readonly page = signal(1);
  readonly pageSize = signal(10);

  ngOnInit(): void {
    this.loadOrders();
  }

  loadOrders(): void {
    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.ordersService
      .getOrders({
        search: this.search(),
        status: this.statusFilter() || undefined,
        page: this.page(),
        pageSize: this.pageSize(),
      })
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (response) => {
          this.orders.set(response.items);
          this.total.set(response.total);
        },
        error: () => {
          this.errorMsg.set('Orders could not be loaded.');
        },
      });
  }

  onSearchInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.search.set(input.value);
  }

  onStatusFilterChange(status: OrderStatus | ''): void {
    this.statusFilter.set(status);
  }

  applyFilters(): void {
    this.page.set(1);
    this.loadOrders();
  }

  clearFilters(): void {
    this.search.set('');
    this.statusFilter.set('');
    this.page.set(1);
    this.loadOrders();
  }

  onPageChange(event: PageEvent): void {
    this.page.set(event.pageIndex + 1);
    this.pageSize.set(event.pageSize);
    this.loadOrders();
  }

  createOrder(): void {
    const dialogRef = this.dialog.open(OrderCreateDialog, {
      width: '720px',
    });
    dialogRef.afterClosed().subscribe((orderCreate: OrderCreate | undefined) => {
      if (!orderCreate) return;
      this.ordersService.createOrder(orderCreate).subscribe({
        next: () => {
          (this.page.set(1), this.loadOrders());
        },
        error: () => {
          this.errorMsg.set('Order could not be created.');
        },
      });
    });
  }

  updateStatus(order: Order, status: OrderStatus): void {
    if (status === order.status) return;
    this.updatingOrderId.set(order.id);
    this.ordersService
      .updateOrderStatus(order.id, status)
      .pipe(finalize(() => this.updatingOrderId.set(null)))
      .subscribe({
        next: (updatedOrder) => {
          this.orders.update((orders) =>
            orders.map((currentOrder) =>
              currentOrder.id === updatedOrder.id ? updatedOrder : currentOrder,
            ),
          );
        },
        error: () => {
          this.errorMsg.set('The order status could not be updated.');
        },
      });
  }

  openStatusDialog(order: Order): void {
    const dialogRef = this.dialog.open(OrderStatusDialog, {
      data: order,
      width: '420px',
    });
    dialogRef.afterClosed().subscribe((result: { status: OrderStatus } | undefined) => {
      if (!result) return;
      this.updateStatus(order, result.status);
    });
  }
}
