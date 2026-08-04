import { Service, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Order,
  OrderCreate,
  OrderFilters,
  OrderListResponse,
  OrderStatus,
} from '../../models/order';

@Service()
export class OrdersService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/orders';

  getOrders(filters: OrderFilters): Observable<OrderListResponse> {
    let params = new HttpParams()
      .set('page', filters.page.toString())
      .set('page_size', filters.pageSize.toString());
    if (filters.search?.trim()) {
      params = params.set('search', filters.search.trim());
    }
    if (filters.status) {
      params = params.set('status', filters.status);
    }
    return this.http.get<OrderListResponse>(this.apiUrl, { params });
  }

  getOrder(orderId: number): Observable<Order> {
	return this.http.get<Order>(`${this.apiUrl}/${orderId}`)
  }

  createOrder(orderData: OrderCreate): Observable<Order> {
	return this.http.post<Order>(this.apiUrl, orderData)
  }

  updateOrderStatus(orderId: number, status: OrderStatus): Observable<Order> {
    return this.http.patch<Order>(`${this.apiUrl}/${orderId}/status`, { status });
  }
}
