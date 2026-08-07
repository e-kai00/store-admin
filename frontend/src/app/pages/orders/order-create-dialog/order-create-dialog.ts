import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { finalize, single } from 'rxjs';
import { ProductsService } from '../../../core/services/products';
import { OrderCreate } from '../../../models/order';
import { Product } from '../../../models/products';

@Component({
  selector: 'app-order-create-dialog',
  imports: [
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatIconModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatSelectModule,
    ReactiveFormsModule,
  ],
  templateUrl: './order-create-dialog.html',
  styleUrl: './order-create-dialog.scss',
})
export class OrderCreateDialog implements OnInit {
  private readonly dialogRef = inject(MatDialogRef<OrderCreateDialog>);
  private readonly fb = inject(FormBuilder);
  private readonly productsService = inject(ProductsService);

  readonly products = signal<Product[]>([]);
  readonly isLoading = signal(false);
  readonly productErrorMsg = signal<string | null>(null);

  readonly form = this.fb.nonNullable.group({
    customer_name: ['', [Validators.required, Validators.maxLength(120)]],
    customer_email: ['', [Validators.required, Validators.email, Validators.maxLength(255)]],
    items: this.fb.array([this.createItemGroup()]),
  });

  ngOnInit(): void {
    this.loadProducts();
  }

  get items() {
    return this.form.controls.items;
  }

  addItem(): void {
    this.items.push(this.createItemGroup());
  }

  removeItem(idx: number): void {
    this.items.removeAt(idx);
  }

  private createItemGroup() {
    return this.fb.nonNullable.group({
      product_id: [0, [Validators.required, Validators.min(1)]],
      quantity: [1, [Validators.required, Validators.min(1)]],
    });
  }

  save(): void {
    if (this.form.invalid) return;
    const orderCreate: OrderCreate = {
      customer_name: this.form.controls.customer_name.value,
      customer_email: this.form.controls.customer_email.value,
      items: this.items.getRawValue(),
    };
    this.dialogRef.close(orderCreate);
  }

  cancel(): void {
    this.dialogRef.close();
  }

  private loadProducts(): void {
    this.isLoading.set(true);
    this.productErrorMsg.set(null);

    this.productsService
      .getProducts({
        page: 1,
        pageSize: 100,
        status: 'active',
      })
      .pipe(finalize(() => this.isLoading.set(false)))
      .subscribe({
        next: (response) => {
          this.products.set(response.items);
        },
        error: () => {
          this.productErrorMsg.set('Products could not be loaded.');
        },
      });
  }
}
