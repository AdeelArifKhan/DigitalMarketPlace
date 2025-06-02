import React from 'react';
import { Coins, Users, Lock, Banknote as Banknotes } from 'lucide-react';

function TokenInfo() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Token Information</h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-indigo-100 rounded-lg">
              <Coins className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Total Supply</h3>
              <p className="text-2xl font-semibold text-indigo-600">100,000,000 DMARKET</p>
              <p className="text-sm text-gray-500">Fixed supply, no inflation</p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-purple-100 rounded-lg">
              <Users className="w-6 h-6 text-purple-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Holders</h3>
              <p className="text-2xl font-semibold text-purple-600">0</p>
              <p className="text-sm text-gray-500">Current token holders</p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-blue-100 rounded-lg">
              <Lock className="w-6 h-6 text-blue-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Decimals</h3>
              <p className="text-2xl font-semibold text-blue-600">8</p>
              <p className="text-sm text-gray-500">Token decimal precision</p>
            </div>
          </div>
          
          <div className="flex items-start space-x-4">
            <div className="p-3 bg-green-100 rounded-lg">
              <Banknotes className="w-6 h-6 text-green-600" />
            </div>
            <div>
              <h3 className="font-medium text-gray-900">Transaction Fee</h3>
              <p className="text-2xl font-semibold text-green-600">0.0001945 USDT</p>
              <p className="text-sm text-gray-500">Fixed fee per transaction</p>
            </div>
          </div>
        </div>
      </div>
      
      <div className="bg-white rounded-xl shadow-md p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">Market Statistics</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-4 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Current Price</h3>
            <p className="text-2xl font-semibold text-gray-900">$1.00 USDT</p>
          </div>
          
          <div className="p-4 bg-gradient-to-br from-purple-50 to-pink-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">Market Cap</h3>
            <p className="text-2xl font-semibold text-gray-900">$100,000,000</p>
          </div>
          
          <div className="p-4 bg-gradient-to-br from-pink-50 to-red-50 rounded-lg">
            <h3 className="text-sm font-medium text-gray-500">24h Volume</h3>
            <p className="text-2xl font-semibold text-gray-900">$0</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default TokenInfo;