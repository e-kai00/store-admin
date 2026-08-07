import { Routes } from '@angular/router';
import { Layout } from './layout/layout';
import { Dashboard } from './pages/dashboard/dashboard';
import { Orders } from './pages/orders/orders';
import { OrderDetail } from './pages/orders/order-detail/order-detail';
import { Products } from './pages/products/products';
import { ProductDetail } from './pages/products/product-detail/product-detail';

export const routes: Routes = [
  {
    path: '',
    component: Layout,
    children: [
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
      { path: 'dashboard', component: Dashboard },
      { path: 'products', component: Products },
      { path: 'products/:productId', component: ProductDetail },
      { path: 'orders', component: Orders },
      { path: 'orders/:orderId', component: OrderDetail },
    ],
  },
  { path: '**', redirectTo: 'dashboard' },
];
