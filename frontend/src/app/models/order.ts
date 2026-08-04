export type OrderStatus =
  | 'pending'
  | 'processing'
  | 'shipped'
  | 'delivered'
  | 'cancelled';

export interface OrderItem {
  id: number;
  productId: number | null;
  productName: string;
  quantity: number;
  unitPrice: string;
  lineTotal: string;
}

export interface Order {
  id: number;
  orderNumber: string;
  customerName: string;
  customerEmail: string;
  status: OrderStatus;
  total: string;
  createdAt: string;
  items: OrderItem[];
}

export interface OrderItemCreate {
  productId: number;
  quantity: number;
}

export interface OrderCreate {
  customerName: string;
  customerEmail: string;
  items: OrderItemCreate[];
}

export interface OrderFilters {
  search?: string;
  status?: OrderStatus;
  page: number;
  pageSize: number;
}

export interface OrderListResponse {
  items: Order[];
  total: number;
  page: number;
  pageSize: number;
}
