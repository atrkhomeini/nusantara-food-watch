'use client';

import { Flex, Title, TabGroup, TabList, Tab } from '@tremor/react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export default function Navbar({ activeTab, setActiveTab }: NavbarProps) {
  const tabs = [
    { id: 'government', label: '🏛️ Government', icon: '🏛️' },
    { id: 'consumer', label: '🛒 Consumer', icon: '🛒' },
    { id: 'wholesaler', label: '📦 Wholesaler', icon: '📦' }
  ];

  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Flex className="py-4">
          <div className="flex items-center gap-3">
            <span className="text-3xl">🍚</span>
            <div>
              <Title>Nusantara Food Watch</Title>
              <p className="text-xs text-gray-500">Real-time Food Price Intelligence</p>
            </div>
          </div>
          
          <TabGroup
            index={tabs.findIndex(t => t.id === activeTab)}
            onIndexChange={(idx) => setActiveTab(tabs[idx].id)}
          >
            <TabList variant="solid" className="mt-0">
              {tabs.map(tab => (
                <Tab key={tab.id}>{tab.label}</Tab>
              ))}
            </TabList>
          </TabGroup>
        </Flex>
      </div>
    </nav>
  );
}