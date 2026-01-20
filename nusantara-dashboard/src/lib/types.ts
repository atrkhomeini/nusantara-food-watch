export interface OverviewMetrics {
  foodInflation: number;
  inflationChange: number;
  highestVolatility: { name: string; value: number };
  stabilityScore: number;
  regionalGap: number;
}

export interface CommodityWatchlist {
  commodity_name: string;
  subcategory_name: string;
  current_price: number;
  change_7d_pct: number;
  volatility: number;
  volatility_level: string;
  status: 'alert' | 'watch' | 'normal';
}

export interface SupplyChainMargin {
  commodity_name: string;
  subcategory_name: string;
  producer_price: number;
  wholesale_price: number;
  retail_traditional_price: number;
  retail_modern_price: number;
  wholesale_margin_pct: number;
  retail_traditional_margin_pct: number;
  retail_modern_margin_pct: number;
}

export interface MarketComparison {
  commodity_name: string;
  subcategory_name: string;
  traditional_price: number;
  modern_price: number;
  price_difference: number;
  price_diff_pct: number;
  cheaper_market: string;
}