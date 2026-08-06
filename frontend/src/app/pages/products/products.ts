import { Component, inject, OnInit, signal } from '@angular/core';
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
import { RouterLink } from '@angular/router';
import { finalize } from 'rxjs';
import { ProductsService } from '../../core/services/products';
import { Product, ProductCreate, ProductUpdate } from '../../models/products';
import { ProductUpdateDialog } from './product-update-dialog/product-update-dialog';

@Component({
  selector: 'app-products',
  imports: [
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    MatTableModule,
    MatIconModule,
    MatMenuModule,
    MatDialogModule,
    RouterLink,
  ],
  templateUrl: './products.html',
  styleUrl: './products.scss',
})
export class Products implements OnInit {
  private readonly productsService = inject(ProductsService);
  private readonly dialog = inject(MatDialog);
  readonly displayColumns = ['name', 'sku', 'category', 'price', 'stock', 'status', 'actions'];

  readonly isLoading = signal(false);
  readonly errorMsg = signal<string | null>(null);

  readonly products = signal<Product[]>([]);
  readonly total = signal(0);

  readonly search = signal('');
  readonly category = signal('');
  readonly statusFilter = signal('');
  readonly page = signal(1);
  readonly pageSize = signal(10);

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.isLoading.set(true);
    this.errorMsg.set(null);

    this.productsService
      .getProducts({
        search: this.search(),
        category: this.category(),
        status: this.statusFilter(),
        page: this.page(),
        pageSize: this.pageSize(),
      })
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (response) => {
          this.products.set(response.items);
          this.total.set(response.total);
        },
        error: () => {
          this.errorMsg.set('Products could not be loaded.');
        },
      });
  }

  onSearchInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.search.set(input.value);
  }

  // TODO: change for selector; use enums
  onCategoryInput(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.category.set(input.value);
  }

  onStatusChange(status: string): void {
    this.statusFilter.set(status);
  }

  applyFilters(): void {
    this.page.set(1);
    this.loadProducts();
  }

  clearFilters(): void {
    this.search.set('');
    this.category.set('');
    this.statusFilter.set('');
    this.page.set(1);
    this.loadProducts();
  }

  onPageChange(event: PageEvent): void {
    this.page.set(event.pageIndex + 1);
    this.pageSize.set(event.pageSize);
    this.loadProducts();
  }

  createProduct(): void {
    const dialogRef = this.dialog.open(ProductUpdateDialog, {
      data: null,
      width: '520px',
    });
    dialogRef.afterClosed().subscribe((productCreate: ProductCreate | undefined) => {
      if (!productCreate) return;
      this.productsService.createProduct(productCreate).subscribe({
        next: () => {
          this.page.set(1);
          this.loadProducts();
        },
        error: () => {
          this.errorMsg.set('Product could not be created.');
        },
      });
    });
  }

  updateProduct(product: Product): void {
    const dialogRef = this.dialog.open(ProductUpdateDialog, { data: product, width: '520px' });
    dialogRef.afterClosed().subscribe((productUpdate: ProductUpdate | undefined) => {
      if (!productUpdate) return;
      this.productsService.updateProduct(product.id, productUpdate).subscribe({
        next: (updatedProduct) => {
          this.products.update((products) =>
            products.map((currentProduct) =>
              currentProduct.id === updatedProduct.id ? updatedProduct : currentProduct,
            ),
          );
        },
        error: () => {
          this.errorMsg.set('Product could not be updated.');
        },
      });
    });
  }

  deleteProduct(product: Product): void {
    const confirmed = window.confirm(`Delete product "${product.name}"`);
    if (!confirmed) return;

    this.productsService.deleteProduct(product.id).subscribe({
      next: () => {
        this.products.update((products) =>
          products.filter((currentProduct) => currentProduct.id !== product.id),
        );
        this.total.update((total) => total - 1);
      },
      error: () => {
        this.errorMsg.set('Product could not be deleted.');
      },
    });
  }
}
