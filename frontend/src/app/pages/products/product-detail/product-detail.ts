import { CurrencyPipe, DatePipe } from '@angular/common';
import { Component, inject, OnInit, signal } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { finalize } from 'rxjs';
import { ProductsService } from '../../../core/services/products';
import { Product } from '../../../models/products';

@Component({
  selector: 'app-product-detail',
  imports: [CurrencyPipe, DatePipe, MatButtonModule, MatProgressSpinnerModule, RouterLink],
  templateUrl: './product-detail.html',
  styleUrl: './product-detail.scss',
})
export class ProductDetail implements OnInit {
  private readonly route = inject(ActivatedRoute);
  private readonly productService = inject(ProductsService);

  readonly product = signal<Product | null>(null);
  readonly isLoading = signal(false);
  readonly errorMsg = signal<string | null>(null);

  ngOnInit(): void {
    this.loadProduct();
  }

  loadProduct(): void {
    const productId = Number(this.route.snapshot.paramMap.get('productId'));
    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.productService
      .getProduct(productId)
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (product) => {
          this.product.set(product);
        },
        error: () => {
          this.errorMsg.set('Product could not be loaded.');
        },
      });
  }
}
