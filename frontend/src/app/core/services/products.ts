import { inject, Service } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
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

  getProducts() {}

  createProduct() {}

  updateProduct() {}

  deleteProduct() {}
}
