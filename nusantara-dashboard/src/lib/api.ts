import { supabase } from './supabase';
import type { OverviewMetrics, CommodityWatchlist, SupplyChainMargin, MarketComparison } from './types';

export async function fetchNationalOverview(): Promise<OverviewMetrics> {
  try {
    const [inflation, volatility, gap, stability] = await Promise.all([
      supabase.rpc('get_food_inflation_yoy'),
      supabase.rpc('get_highest_volatility'),
      supabase.rpc('get_regional_price_gap'),
      supabase.rpc('get_price_stability_score')
    ]);

    return {
      foodInflation: inflation.data?.[0]?.inflation_yoy || 0,
      inflationChange: 3.2,
      highestVolatility: {
        name: volatility.data?.[0]?.commodity_name || 'N/A',
        value: volatility.data?.[0]?.volatility || 0
      },
      stabilityScore: stability.data?.[0]?.stability_score || 0,
      regionalGap: gap.data?.[0]?.regional_gap_pct || 0
    };
  } catch (error) {
    console.error('Error fetching overview:', error);
    throw error;
  }
}

export async function fetchCommodityWatchlist(): Promise<CommodityWatchlist[]> {
  const { data, error } = await supabase.rpc('get_commodity_watchlist');
  if (error) throw error;
  return data || [];
}

export async function fetchSupplyChainMargins(): Promise<SupplyChainMargin[]> {
  const { data, error } = await supabase.rpc('get_supply_chain_margins');
  if (error) throw error;
  return data || [];
}

export async function fetchMarketComparison(): Promise<MarketComparison[]> {
  const { data, error } = await supabase.rpc('get_market_type_comparison');
  if (error) throw error;
  return data || [];
}