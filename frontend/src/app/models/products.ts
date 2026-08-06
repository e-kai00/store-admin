export interface Product {
  id: number;
  name: string;
  sku: string;
  category: string;
  price: string;
  stock_quantity: number;
  status: string;
  description: string | null;
  created_at: string;
}

export interface ProductCreate {
  name: string;
  sku: string;
  category: string;
  price: string;
  stock_quantity: number;
  status: string;
  description: string | null;
}

export type ProductUpdate = Partial<ProductCreate>;

export interface ProductFilters {
  search?: string;
  category?: string;
  status?: string;
  page: number;
  pageSize: number;
}

export interface ProductListResponse {
  items: Product[];
  total: number;
  page: number;
  pageSize: number;
}
