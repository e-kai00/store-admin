import { inject, Service } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { filter, Observable } from 'rxjs';
import {
  Product,
  ProductCreate,
  ProductFilters,
  ProductListResponse,
  ProductUpdate,
} from '../../models/products';

@Service()
export class ProductsService {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000/products';

  getProducts(filters: ProductFilters): Observable<ProductListResponse> {
    let params = new HttpParams()
      .set('page', filters.page.toString())
      .set('page_size', filters.pageSize.toString());
    if (filters.search?.trim()) {
      params = params.set('search', filters.search.trim());
    }
    if (filters.category) {
      params = params.set('category', filters.category);
    }
    if (filters.status) {
      params = params.set('status', filters.status);
    }
    return this.http.get<ProductListResponse>(this.apiUrl, { params });
  }

  getProduct(productId: number): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/${productId}`);
  }

  createProduct(productData: ProductCreate): Observable<Product> {
    return this.http.post<Product>(this.apiUrl, productData);
  }

  updateProduct(productId: number, product_data: ProductUpdate): Observable<Product> {
    return this.http.patch<Product>(`${this.apiUrl}/${productId}`, product_data);
  }

  deleteProduct(productId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${productId}`);
  }
}
