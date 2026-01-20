import React, { useState } from 'react';
import { Card, Text } from '@tremor/react';

interface RegionData {
  name: string;
  price: number;
  priceIndex: number;
  color: string;
}

const regionData: Record<string, RegionData> = {
  sumatra: { name: 'Sumatra', price: 45000, priceIndex: 95, color: '#FCD34D' },
  java: { name: 'Java', price: 40000, priceIndex: 85, color: '#4ADE80' },
  kalimantan: { name: 'Kalimantan', price: 52000, priceIndex: 110, color: '#FB923C' },
  sulawesi: { name: 'Sulawesi', price: 48000, priceIndex: 102, color: '#FBBF24' },
  maluku: { name: 'Maluku', price: 58000, priceIndex: 125, color: '#F87171' },
  papua: { name: 'Papua', price: 65000, priceIndex: 140, color: '#DC2626' },
  bali: { name: 'Bali & Nusa Tenggara', price: 42000, priceIndex: 88, color: '#4ADE80' }
};

const IndonesiaMap = () => {
  const [hoveredRegion, setHoveredRegion] = useState<string | null>(null);
  const [tooltipPos, setTooltipPos] = useState({ x: 0, y: 0 });

  const handleMouseEnter = (region: string, event: React.MouseEvent) => {
    setHoveredRegion(region);
    setTooltipPos({ x: event.clientX, y: event.clientY });
  };

  const handleMouseMove = (event: React.MouseEvent) => {
    setTooltipPos({ x: event.clientX, y: event.clientY });
  };

  const handleMouseLeave = () => {
    setHoveredRegion(null);
  };

  return (
    <div className="relative">
      <svg
        viewBox="0 0 1000 400"
        className="w-full h-auto"
        style={{ maxHeight: '400px' }}
      >
        {/* Sumatra */}
        <path
          d="M 50 80 L 120 60 L 150 120 L 130 200 L 80 220 L 50 180 Z"
          fill={regionData.sumatra.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80 hover:stroke-4"
          onMouseEnter={(e) => handleMouseEnter('sumatra', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        
        {/* Java */}
        <path
          d="M 180 200 L 350 195 L 380 220 L 360 240 L 200 245 Z"
          fill={regionData.java.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80"
          onMouseEnter={(e) => handleMouseEnter('java', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        
        {/* Kalimantan */}
        <path
          d="M 250 80 L 400 70 L 420 140 L 400 190 L 300 180 L 260 140 Z"
          fill={regionData.kalimantan.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80"
          onMouseEnter={(e) => handleMouseEnter('kalimantan', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        
        {/* Sulawesi */}
        <path
          d="M 480 120 L 540 100 L 560 150 L 540 200 L 490 190 L 480 150 Z"
          fill={regionData.sulawesi.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80"
          onMouseEnter={(e) => handleMouseEnter('sulawesi', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        
        {/* Bali & Nusa Tenggara */}
        <path
          d="M 400 230 L 500 228 L 520 250 L 500 265 L 410 260 Z"
          fill={regionData.bali.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80"
          onMouseEnter={(e) => handleMouseEnter('bali', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        
        {/* Maluku */}
        <path
          d="M 620 140 L 680 130 L 700 170 L 680 200 L 630 190 Z"
          fill={regionData.maluku.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80"
          onMouseEnter={(e) => handleMouseEnter('maluku', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />
        
        {/* Papua */}
        <path
          d="M 750 120 L 900 110 L 950 160 L 920 220 L 800 210 L 760 180 Z"
          fill={regionData.papua.color}
          stroke="#1F2937"
          strokeWidth="2"
          className="cursor-pointer transition-all hover:opacity-80"
          onMouseEnter={(e) => handleMouseEnter('papua', e)}
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
        />

        {/* Region Labels */}
        <text x="90" y="145" className="text-xs font-semibold fill-gray-800">Sumatra</text>
        <text x="270" y="220" className="text-xs font-semibold fill-gray-800">Java</text>
        <text x="320" y="130" className="text-xs font-semibold fill-gray-800">Kalimantan</text>
        <text x="500" y="155" className="text-xs font-semibold fill-gray-800">Sulawesi</text>
        <text x="440" y="250" className="text-xs font-semibold fill-gray-800">Bali</text>
        <text x="640" y="170" className="text-xs font-semibold fill-gray-800">Maluku</text>
        <text x="820" y="170" className="text-xs font-semibold fill-gray-800">Papua</text>
      </svg>

      {/* Tooltip */}
      {hoveredRegion && (
        <div
          className="fixed z-50 pointer-events-none"
          style={{
            left: `${tooltipPos.x + 15}px`,
            top: `${tooltipPos.y + 15}px`,
          }}
        >
          <Card className="shadow-lg border-2 border-gray-300 max-w-xs">
            <Text className="font-bold text-lg mb-2">
              {regionData[hoveredRegion].name}
            </Text>
            <div className="space-y-1">
              <Text className="text-sm">
                <span className="font-semibold">Avg Price:</span>{' '}
                Rp {regionData[hoveredRegion].price.toLocaleString('id-ID')}
              </Text>
              <Text className="text-sm">
                <span className="font-semibold">Price Index:</span>{' '}
                {regionData[hoveredRegion].priceIndex}
              </Text>
              <div className="pt-2 border-t">
                <Text className="text-xs text-gray-600">
                  Click to view detailed statistics
                </Text>
              </div>
            </div>
          </Card>
        </div>
      )}

      {/* Legend */}
      <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-3">
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-green-400 rounded border border-gray-300"></div>
          <Text className="text-sm">85-95 (Low)</Text>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-yellow-300 rounded border border-gray-300"></div>
          <Text className="text-sm">95-110 (Medium)</Text>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-orange-400 rounded border border-gray-300"></div>
          <Text className="text-sm">110-125 (High)</Text>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-6 h-6 bg-red-500 rounded border border-gray-300"></div>
          <Text className="text-sm">125+ (Very High)</Text>
        </div>
      </div>
    </div>
  );
};

export default IndonesiaMap;