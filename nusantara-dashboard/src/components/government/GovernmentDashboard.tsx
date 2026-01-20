'use client';

import React, { useState } from 'react';
import { Card, Title, Text, Metric, BadgeDelta, AreaChart, Select, SelectItem, Badge, Grid, Flex, ProgressBar } from '@tremor/react';
import { AlertCircle, TrendingUp, Activity, MapPin, ChevronRight, X } from 'lucide-react';
import { useNationalOverview, useCommodityWatchlist } from '../../hooks/useData';
import IndonesiaMap from './IndonesiaMap';

const GovernmentDashboard = () => {
  // 1. FETCH REAL DATA
  const { data: overview, loading: overviewLoading } = useNationalOverview();
  const { data: watchlist, loading: watchlistLoading } = useCommodityWatchlist();
  
  // 2. LOCAL STATE
  const [showAlert, setShowAlert] = useState(true);
  const [selectedCommodity, setSelectedCommodity] = useState('all');
  const [dateRange, setDateRange] = useState('30d');

  // 3. SHOW LOADING
  if (overviewLoading || watchlistLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading dashboard data...</p>
        </div>
      </div>
    );
  }

  // 4. HELPER FUNCTION
  const getStatusBadge = (status: string) => {
    const config = {
      alert: { color: 'red' as const, icon: '🚨', text: 'Alert' },
      watch: { color: 'yellow' as const, icon: '⚠️', text: 'Watch' },
      normal: { color: 'green' as const, icon: '✅', text: 'Normal' }
    };
    const { color, icon, text } = config[status as keyof typeof config];
    return <Badge color={color}>{icon} {text}</Badge>;
  };

  // 5. RENDER COMPONENT
  return (
    <div className="min-h-screen bg-gray-50 p-6">
      {/* Alert Banner */}
      {showAlert && (
        <Card className="mb-6 bg-red-50 border-red-200">
          <Flex>
            <div className="flex items-start gap-3 flex-1">
              <AlertCircle className="text-red-500 mt-1" size={20} />
              <div>
                <Text className="font-semibold text-red-900">🚨 HIGH PRIORITY ALERT</Text>
                <Text className="text-red-800">
                  {overview?.highestVolatility.name}: Volatilitas tinggi
                </Text>
              </div>
            </div>
            <button onClick={() => setShowAlert(false)} className="text-red-500 hover:text-red-700">
              <X size={20} />
            </button>
          </Flex>
        </Card>
      )}

      {/* National Overview Cards - USING REAL DATA */}
      <Grid numItemsMd={2} numItemsLg={4} className="gap-6 mb-6">
        <Card>
          <Text>📈 Inflasi Pangan</Text>
          <Metric>+{overview?.foodInflation.toFixed(1)}%</Metric>
          <Text className="text-sm">YoY</Text>
          <BadgeDelta deltaType="moderateIncrease" className="mt-2">
            vs {overview?.inflationChange}% general
          </BadgeDelta>
        </Card>

        <Card>
          <Text>🔥 Highest Volatility</Text>
          <Metric className="text-red-600">{overview?.highestVolatility.name}</Metric>
          <Text className="text-sm">σ = {overview?.highestVolatility.value.toFixed(0)}</Text>
          <Badge color="red" className="mt-2">Action needed!</Badge>
        </Card>

        <Card>
          <Text>📊 Price Stability</Text>
          <Metric>{overview?.stabilityScore}/10</Metric>
          <Text className="text-sm">Score</Text>
          <ProgressBar value={(overview?.stabilityScore || 0) * 10} color="green" className="mt-2" />
        </Card>

        <Card>
          <Text>🗺️ Regional Inequality</Text>
          <Metric className="text-orange-600">{overview?.regionalGap.toFixed(1)}%</Metric>
          <Text className="text-sm">Gap</Text>
        </Card>
      </Grid>

      {/* Main Content - Map and Insights */}
      <Grid numItemsLg={3} className="gap-6 mb-6">
        <div className="lg:col-span-2">
          <Card>
            <Title>🗺️ Price Heatmap</Title>
            <IndonesiaMap />
            
            <div className="mt-4 flex gap-4">
              <Select value={selectedCommodity} onValueChange={setSelectedCommodity}>
                <SelectItem value="all">Komoditas: All</SelectItem>
                <SelectItem value="beras">Beras</SelectItem>
                <SelectItem value="cabai">Cabai</SelectItem>
              </Select>
              
              <Select value={dateRange} onValueChange={setDateRange}>
                <SelectItem value="7d">Last 7 days</SelectItem>
                <SelectItem value="30d">Last 30 days</SelectItem>
              </Select>
            </div>
          </Card>
        </div>

        <Card>
          <Title>💡 Policy Insights</Title>
          <div className="mt-4 space-y-4">
            <div className="border-l-4 border-blue-500 pl-4 py-2">
              <Text className="font-semibold">1. Stabilisasi {overview?.highestVolatility.name}</Text>
              <ul className="mt-2 space-y-1">
                <li className="text-sm text-gray-600">• Volatilitas tinggi</li>
                <li className="text-sm text-gray-600">• Action: Impor atau subsidi</li>
              </ul>
            </div>
          </div>
        </Card>
      </Grid>

      {/* Commodity Watchlist - USING REAL DATA */}
      <Card>
        <Flex>
          <Title>📊 Komoditas Prioritas</Title>
        </Flex>
        
        <div className="mt-4 overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-gray-200">
                <th className="text-left py-3 px-2 text-sm font-medium text-gray-600">Commodity</th>
                <th className="text-right py-3 px-2 text-sm font-medium text-gray-600">Current</th>
                <th className="text-right py-3 px-2 text-sm font-medium text-gray-600">7d Change</th>
                <th className="text-right py-3 px-2 text-sm font-medium text-gray-600">Volatility</th>
                <th className="text-right py-3 px-2 text-sm font-medium text-gray-600">Status</th>
              </tr>
            </thead>
            <tbody>
              {watchlist.map((item, idx) => (
                <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50">
                  <td className="py-3 px-2">
                    <Text>{item.commodity_name} - {item.subcategory_name}</Text>
                  </td>
                  <td className="text-right py-3 px-2">
                    <Text>Rp {item.current_price.toLocaleString('id-ID')}</Text>
                  </td>
                  <td className="text-right py-3 px-2">
                    <BadgeDelta deltaType={item.change_7d_pct > 0 ? 'increase' : 'decrease'}>
                      {item.change_7d_pct > 0 ? '+' : ''}{item.change_7d_pct}%
                    </BadgeDelta>
                  </td>
                  <td className="text-right py-3 px-2">
                    <Badge color={
                      item.volatility_level === 'Very High' ? 'red' :
                      item.volatility_level === 'High' ? 'orange' :
                      item.volatility_level === 'Medium' ? 'yellow' : 'green'
                    }>
                      {item.volatility_level}
                    </Badge>
                  </td>
                  <td className="text-right py-3 px-2">
                    {getStatusBadge(item.status)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};

export default GovernmentDashboard;