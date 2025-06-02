"""
Example usage of the Digital Marketplace contract.
"""
import os
from algosdk import account, mnemonic
from algosdk.v2client import algod

from digital_marketplace.contract import DigitalMarketplace
from digital_marketplace.utils import format_amount, algo_to_usdt, usdt_to_algo

def main():
    """Run an example of the Digital Marketplace contract."""
    # In a real application, these would be securely stored
    # For this example, we'll create new accounts
    
    # Create creator account
    creator_private_key, creator_address = account.generate_account()
    creator_mnemonic = mnemonic.from_private_key(creator_private_key)
    
    print("=== Contract Creator Account ===")
    print(f"Address: {creator_address}")
    print(f"Mnemonic: {creator_mnemonic}")
    print()
    
    # Create user account
    user_private_key, user_address = account.generate_account()
    user_mnemonic = mnemonic.from_private_key(user_private_key)
    
    print("=== User Account ===")
    print(f"Address: {user_address}")
    print(f"Mnemonic: {user_mnemonic}")
    print()
    
    # In a real scenario, you would connect to an actual Algorand node
    # For demonstration, we'll assume we have a connection
    # You would need to replace this with actual connection parameters
    algod_address = "https://testnet-algorand.api.purestake.io/ps2"
    algod_token = "YOUR_API_KEY"
    headers = {"X-API-Key": algod_token}
    
    print("NOTE: This example requires a connection to an Algorand node.")
    print("You would need to fund these accounts with Algos before running this on a real network.")
    print("For demonstration purposes, we'll simulate the contract operations locally.")
    print()
    
    # For demonstration purposes, we'll create a simple mock of the AlgodClient
    # In a real application, you would use the actual client
    class MockAlgodClient:
        def suggested_params(self):
            class Params:
                def __init__(self):
                    self.fee = 1000
                    self.flat_fee = False
                    self.first = 1
                    self.last = 1000
                    self.gh = "dGVzdG5ldC12MS4w"
                    self.gen = "testnet-v1.0"
            return Params()
        
        def send_transaction(self, txn):
            return "MOCK_TX_ID"
        
        def send_transactions(self, txns):
            return "MOCK_TX_ID"
        
        def asset_info(self, asset_id):
            return {
                "index": asset_id,
                "params": {
                    "creator": creator_address,
                    "decimals": 8,
                    "default-frozen": False,
                    "name": "Digital Marketplace Token",
                    "total": 10000000000000000,
                    "unit-name": "DMARKET",
                    "url": "https://digitalmarketplace.example.com"
                }
            }
    
    def wait_for_confirmation(client, tx_id, wait_rounds):
        return {"asset-index": 12345, "confirmed-round": 1}
    
    # Monkey patch the transaction module for our simulation
    import algosdk.future.transaction as transaction
    transaction.wait_for_confirmation = wait_for_confirmation
    
    # Create mock client
    algod_client = MockAlgodClient()
    
    # Initialize the contract
    contract = DigitalMarketplace(algod_client, creator_address, creator_private_key)
    
    # Create the token
    try:
        print("=== Creating Digital Marketplace Token ===")
        asset_id = contract.create_token()
        print(f"Asset ID: {asset_id}")
        print(f"Total Supply: {format_amount(contract.token_holders[creator_address])}")
        print()
    except Exception as e:
        print(f"Error creating token: {e}")
        return
    
    # Simulate a deposit
    try:
        print("=== Simulating Deposit ===")
        algo_amount = 1_000_000  # 1 ALGO
        usdt_value = algo_to_usdt(algo_amount)
        print(f"Depositing {algo_amount/1_000_000} ALGO (≈{usdt_value:.4f} USDT)")
        
        tx_id, tokens_received = contract.deposit(user_address, user_private_key, algo_amount)
        
        print(f"Transaction ID: {tx_id}")
        print(f"Tokens Received: {format_amount(tokens_received)}")
        print(f"User Balance: {format_amount(contract.get_token_balance(user_address))}")
        print()
    except Exception as e:
        print(f"Error depositing: {e}")
    
    # Simulate a withdrawal
    try:
        print("=== Simulating Withdrawal ===")
        token_amount = contract.get_token_balance(user_address) // 2  # Withdraw half
        
        print(f"Withdrawing {format_amount(token_amount)} tokens")
        
        tx_id, algo_received = contract.withdraw(user_address, user_private_key, token_amount)
        
        print(f"Transaction ID: {tx_id}")
        print(f"ALGO Received: {algo_received/1_000_000}")
        print(f"User Balance: {format_amount(contract.get_token_balance(user_address))}")
        print()
    except Exception as e:
        print(f"Error withdrawing: {e}")
    
    # Simulate staking rewards
    try:
        print("=== Simulating Staking Rewards ===")
        
        # For demonstration, we'll give the user enough tokens to be eligible for staking
        staking_tokens = usdt_to_algo(10_000) * 10  # 10K USDT worth in tokens
        creator_balance = contract.get_token_balance(creator_address)
        
        print(f"Sending user {format_amount(staking_tokens)} tokens to simulate staking")
        
        # Update balances directly for simulation
        contract.token_holders[creator_address] = creator_balance - staking_tokens
        user_balance = contract.get_token_balance(user_address)
        contract.token_holders[user_address] = user_balance + staking_tokens
        
        print(f"User Balance: {format_amount(contract.get_token_balance(user_address))}")
        
        # Calculate staking rewards
        # We'll override the timestamp to simulate a day passing
        contract.last_staking_calculation = 0
        contract.calculate_staking_rewards()
        
        rewards = contract.get_staking_rewards(user_address)
        print(f"Daily Staking Rewards: {rewards/1_000_000} ALGO")
        
        # Claim rewards
        tx_id, claimed = contract.claim_staking_rewards(user_address)
        
        print(f"Transaction ID: {tx_id}")
        print(f"Claimed Rewards: {claimed/1_000_000} ALGO")
        print()
    except Exception as e:
        print(f"Error with staking rewards: {e}")
    
    # Show token info
    try:
        print("=== Token Information ===")
        token_info = contract.get_token_info()
        print(f"Asset ID: {token_info['index']}")
        print(f"Name: {token_info['params']['name']}")
        print(f"Unit Name: {token_info['params']['unit-name']}")
        print(f"Total Supply: {format_amount(token_info['params']['total'])}")
        print(f"Decimals: {token_info['params']['decimals']}")
        print(f"Creator: {token_info['params']['creator']}")
        print(f"URL: {token_info['params']['url']}")
        print()
    except Exception as e:
        print(f"Error getting token info: {e}")
    
    print("=== Example Completed ===")
    print("Note: This was a simulation. In a real environment, you would need:")
    print("1. Actual funded Algorand accounts")
    print("2. Connection to an Algorand node")
    print("3. Proper error handling and transaction confirmation")

if __name__ == "__main__":
    main()