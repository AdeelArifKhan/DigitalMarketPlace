import React, { useState } from 'react';
import { Coins, ArrowDownUp, Wallet, LineChart } from 'lucide-react';
import TokenInfo from './components/TokenInfo';
import DepositWithdraw from './components/DepositWithdraw';
import StakingDashboard from './components/StakingDashboard';
import Navbar from './components/Navbar';

function App() {
  const [activeTab, setActiveTab] = useState('token');

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-white to-purple-100">
      <Navbar />
      
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <nav className="flex space-x-4 justify-center">
            <button
              onClick={() => setActiveTab('token')}
              className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'token'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-indigo-50'
              }`}
            >
              <Coins className="w-5 h-5 mr-2" />
              Token Info
            </button>
            <button
              onClick={() => setActiveTab('transfer')}
              className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'transfer'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-indigo-50'
              }`}
            >
              <ArrowDownUp className="w-5 h-5 mr-2" />
              Deposit/Withdraw
            </button>
            <button
              onClick={() => setActiveTab('staking')}
              className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                activeTab === 'staking'
                  ? 'bg-indigo-600 text-white'
                  : 'bg-white text-gray-600 hover:bg-indigo-50'
              }`}
            >
              <LineChart className="w-5 h-5 mr-2" />
              Staking
            </button>
          </nav>
        </div>

        <div className="max-w-4xl mx-auto">
          {activeTab === 'token' && <TokenInfo />}
          {activeTab === 'transfer' && <DepositWithdraw />}
          {activeTab === 'staking' && <StakingDashboard />}
        </div>
      </main>
    </div>
  );
}

export default App;