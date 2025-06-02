import React from 'react';
import { LineChart, Wallet, TrendingUp } from 'lucide-react';

function StakingDashboard() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Staking Dashboard</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <Wallet className="w-5 h-5 text-indigo-600 mr-2" />
              <h3 className="text-sm font-medium text-gray-500">Your Stake</h3>
            </div>
            <p className="text-2xl font-semibold text-gray-900">0.00 DMARKET</p>
            <p className="text-sm text-gray-500">≈ $0.00 USDT</p>
          </div>
          
          <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <TrendingUp className="w-5 h-5 text-purple-600 mr-2" />
              <h3 className="text-sm font-medium text-gray-500">APR</h3>
            </div>
            <p className="text-2xl font-semibold text-gray-900">5.00%</p>
            <p className="text-sm text-gray-500">Paid in ALGO</p>
          </div>
          
          <div className="bg-gradient-to-br from-pink-50 to-red-50 rounded-lg p-4">
            <div className="flex items-center mb-2">
              <LineChart className="w-5 h-5 text-pink-600 mr-2" />
              <h3 className="text-sm font-medium text-gray-500">Rewards</h3>
            </div>
            <p className="text-2xl font-semibold text-gray-900">0.00 ALGO</p>
            <p className="text-sm text-gray-500">Available to claim</p>
          </div>
        </div>
        
        <div className="bg-yellow-50 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-yellow-600 mt-0.5 mr-2" />
            <div>
              <h4 className="text-sm font-medium text-yellow-900">Staking Requirements</h4>
              <p className="text-sm text-yellow-700 mt-1">
                Minimum stake: 10,000 USDT worth of DMARKET tokens
                <br />
                Rewards are distributed daily in ALGO
              </p>
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button
            className="w-full px-4 py-3 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2"
          >
            Stake Tokens
          </button>
          <button
            className="w-full px-4 py-3 text-indigo-600 bg-indigo-100 rounded-lg hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2"
          >
            Claim Rewards
          </button>
        </div>
      </div>
    </div>
  );
}

export default StakingDashboard;