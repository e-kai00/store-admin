import { Component, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { Order, OrderStatus } from '../../../models/order';


@Component({
  selector: 'app-order-status-dialog',
  imports: [
    MatButtonModule,
    MatDialogModule,
    MatFormFieldModule,
    MatSelectModule,
    ReactiveFormsModule,
  ],
  templateUrl: './order-status-dialog.html',
  styleUrl: './order-status-dialog.scss',
})
export class OrderStatusDialog {
  private readonly dialogRef = inject(MatDialogRef<OrderStatusDialog>);
  private readonly fb = inject(FormBuilder);
  readonly order = inject<Order>(MAT_DIALOG_DATA);
  readonly statuses: OrderStatus[] = ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];

  readonly form = this.fb.nonNullable.group({
    status: [this.order.status, [Validators.required]],
  });

  save(): void {
    if (this.form.invalid) return;
    this.dialogRef.close(this.form.getRawValue())
  }

  cancel(): void {
    this.dialogRef.close()
  }
}
