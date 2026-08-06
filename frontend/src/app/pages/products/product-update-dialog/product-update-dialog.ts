import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { Product, ProductCreate, ProductUpdate } from '../../../models/products';

@Component({
  selector: 'app-product-update-dialog',
  imports: [
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatInputModule,
    MatSelectModule,
    ReactiveFormsModule,
  ],
  templateUrl: './product-update-dialog.html',
  styleUrl: './product-update-dialog.scss',
})
export class ProductUpdateDialog {
  private readonly dialogRef = inject(MatDialogRef<ProductUpdateDialog>);
  private readonly fb = inject(FormBuilder);
  readonly product = inject<Product | null>(MAT_DIALOG_DATA);
  readonly isCreateMode = this.product === null;

  readonly form = this.fb.nonNullable.group({
    name: [this.product?.name ?? '', [Validators.required, Validators.maxLength(120)]],
    sku: [this.product?.sku ?? '', [Validators.required, Validators.maxLength(50)]],
    price: [this.product?.price ?? '', [Validators.required]],
    category: [this.product?.category ?? '', [Validators.required, Validators.maxLength(50)]],
    stock_quantity: [this.product?.stock_quantity ?? 0, [Validators.required, Validators.min(0)]],
    status: [this.product?.status ?? 'active', [Validators.required]],
    description: [this.product?.description ?? null],
  });

  save(): void {
    if (this.form.invalid) return;
    const productData: ProductCreate | ProductUpdate = this.form.getRawValue();
    this.dialogRef.close(productData);
  }

  cancel(): void {
    this.dialogRef.close();
  }
}
