import { useState, useEffect } from 'react';
import { fetchNationalOverview, fetchCommodityWatchlist } from '../lib/api';
import type { OverviewMetrics, CommodityWatchlist } from '../lib/types';

export function useNationalOverview() {
  const [data, setData] = useState<OverviewMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchNationalOverview()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}

export function useCommodityWatchlist() {
  const [data, setData] = useState<CommodityWatchlist[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    fetchCommodityWatchlist()
      .then(setData)
      .catch(setError)
      .finally(() => setLoading(false));
  }, []);

  return { data, loading, error };
}