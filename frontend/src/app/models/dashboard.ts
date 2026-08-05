export interface LowStockProduct {
  id: number;
  name: string;
  sku: string;
  stock_quantity: number;
  status: string;
}

export interface DashboardSummary {
  total_orders: number;
  total_revenue: string;
  open_orders: number;
  completed_orders: number;
  low_stock_products: LowStockProduct[];
}
