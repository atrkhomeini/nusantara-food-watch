'use client';

import { useState } from 'react';
import Navbar from '../components/layout/Navbar';
import GovernmentDashboard from '../components/government/GovernmentDashboard';

export default function Home() {
  const [activeTab, setActiveTab] = useState('government');

  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />
      
      <main className="max-w-7xl mx-auto">
        {activeTab === 'government' && <GovernmentDashboard />}
        {activeTab === 'consumer' && (
          <div className="p-12 text-center">
            <h2 className="text-2xl font-bold">🛒 Consumer Dashboard</h2>
            <p className="text-gray-600 mt-2">Coming soon...</p>
          </div>
        )}
        {activeTab === 'wholesaler' && (
          <div className="p-12 text-center">
            <h2 className="text-2xl font-bold">📦 Wholesaler Dashboard</h2>
            <p className="text-gray-600 mt-2">Coming soon...</p>
          </div>
        )}
      </main>
    </div>
  );
}