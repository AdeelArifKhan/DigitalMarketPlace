import React, { useState } from 'react';
import { ArrowDownUp, AlertCircle } from 'lucide-react';

function DepositWithdraw() {
  const [isDeposit, setIsDeposit] = useState(true);
  const [amount, setAmount] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Handle deposit/withdraw logic here
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-semibold text-gray-900">
          {isDeposit ? 'Deposit ALGO' : 'Withdraw DMARKET'}
        </h2>
        <button
          onClick={() => setIsDeposit(!isDeposit)}
          className="flex items-center px-4 py-2 rounded-lg bg-gray-100 text-gray-600 hover:bg-gray-200 transition-colors"
        >
          <ArrowDownUp className="w-5 h-5 mr-2" />
          Switch
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            {isDeposit ? 'ALGO Amount' : 'DMARKET Amount'}
          </label>
          <div className="relative">
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              className="block w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-indigo-600 focus:border-transparent"
              placeholder="0.00"
              min="0"
              step="0.00000001"
            />
            <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none">
              <span className="text-gray-500">{isDeposit ? 'ALGO' : 'DMARKET'}</span>
            </div>
          </div>
        </div>

        <div className="bg-indigo-50 rounded-lg p-4">
          <div className="flex items-start">
            <AlertCircle className="w-5 h-5 text-indigo-600 mt-0.5 mr-2" />
            <div>
              <h4 className="text-sm font-medium text-indigo-900">Transaction Details</h4>
              <p className="text-sm text-indigo-700 mt-1">
                Fee: 0.0001945 USDT
                <br />
                You will receive: {amount ? `${(Number(amount) * 0.99).toFixed(8)} ${isDeposit ? 'DMARKET' : 'ALGO'}` : '0.00'}
              </p>
            </div>
          </div>
        </div>

        <button
          type="submit"
          className="w-full px-4 py-3 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2"
        >
          {isDeposit ? 'Deposit' : 'Withdraw'}
        </button>
      </form>
    </div>
  );
}

export default DepositWithdraw;