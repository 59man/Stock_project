export interface Lot {
  id: number;
  asset_id: number;
  quantity: number;
  price: number;
  currency: string | null;
  bought_at: string;
}

export interface LotCreate {
  asset_id: number;
  quantity: number;
  price: number;
  currency?: string;
  bought_at?: string | null; // 👈 MUST EXIST
}

export interface LotResponse {
  id: number;
  asset_id: number;
  quantity: number;
  price: number;
  currency?: string | null;
  bought_at: string; // ISO datetime string
}


