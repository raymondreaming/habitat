const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export type AuctionResult = {
  unit_result_id: string;
  auction_unit: string;
  service_type: string;
  auction_product: string;
  executed_quantity: number;
  clearing_price: number;
  delivery_start: string;
  delivery_end: string;
  technology_type: string | null;
  post_code: string | null;
};

export type Summary = {
  date: string;
  total_records: number;
  total_executed_quantity: number;
  average_clearing_price: number;
  estimated_gross_revenue: number;
  active_units: number;
  top_service_by_volume: { service_type: string; executed_quantity: number } | null;
  top_unit_by_volume: { auction_unit: string; executed_quantity: number } | null;
  by_service_type: Array<{ service_type: string; executed_quantity: number }>;
  by_auction_unit: Array<{ auction_unit: string; executed_quantity: number }>;
};

export type MarketShare = {
  service_type: string;
  habitat_records: number;
  market_records: number;
  habitat_executed_quantity: number;
  market_executed_quantity: number;
  habitat_market_share_percent: number;
  habitat_average_clearing_price: number;
  market_average_clearing_price: number;
};

export type TimeSeriesPoint = {
  delivery_start: string;
  delivery_end: string;
  service_type: string;
  auction_product: string;
  total_records: number;
  executed_quantity: number;
  average_clearing_price: number;
  estimated_gross_revenue: number;
};

export type UnitPerformance = {
  auction_unit: string;
  total_records: number;
  executed_quantity: number;
  average_clearing_price: number;
  estimated_gross_revenue: number;
  service_types: string[];
  auction_products: string[];
};

export type ProductPerformance = {
  service_type: string;
  auction_product: string;
  total_records: number;
  executed_quantity: number;
  average_clearing_price: number;
  estimated_gross_revenue: number;
};

export type Options = {
  date: string;
  service_types: string[];
  auction_units: string[];
  auction_products: string[];
};

export type IngestionRun = {
  id: number;
  target_date: string;
  records_fetched: number;
  records_upserted: number;
  status: string;
  error_message: string | null;
  started_at: string;
  finished_at: string | null;
};

export async function ingest(date: string): Promise<IngestionRun> {
  return request<IngestionRun>(`/api/ingest?date=${encodeURIComponent(date)}`, { method: "POST" });
}

export async function getResults(params: {
  date: string;
  serviceType?: string;
  auctionUnit?: string;
  auctionProduct?: string;
}): Promise<{ date: string; results: AuctionResult[] }> {
  const search = new URLSearchParams({ date: params.date });
  if (params.serviceType) search.set("service_type", params.serviceType);
  if (params.auctionUnit) search.set("auction_unit", params.auctionUnit);
  if (params.auctionProduct) search.set("auction_product", params.auctionProduct);
  return request(`/api/results?${search.toString()}`);
}

export async function getSummary(date: string): Promise<Summary> {
  return request<Summary>(`/api/summary?date=${encodeURIComponent(date)}`);
}

export async function getOptions(date: string): Promise<Options> {
  return request<Options>(`/api/options?date=${encodeURIComponent(date)}`);
}

export async function getMarketShare(date: string): Promise<{ date: string; market_share: MarketShare[] }> {
  return request(`/api/market-share?date=${encodeURIComponent(date)}`);
}

export async function getTimeseries(date: string): Promise<{ date: string; timeseries: TimeSeriesPoint[] }> {
  return request(`/api/timeseries?date=${encodeURIComponent(date)}`);
}

export async function getUnits(date: string): Promise<{ date: string; units: UnitPerformance[] }> {
  return request(`/api/units?date=${encodeURIComponent(date)}`);
}

export async function getProducts(date: string): Promise<{ date: string; products: ProductPerformance[] }> {
  return request(`/api/products?date=${encodeURIComponent(date)}`);
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, init);
  const payload = await response.json().catch(() => null);

  if (!response.ok) {
    const detail = payload?.detail ?? response.statusText;
    throw new Error(detail);
  }

  return payload as T;
}
