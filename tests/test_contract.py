"""
Tests for the DigitalMarketplace contract.
"""
import unittest
from unittest.mock import MagicMock, patch

from digital_marketplace.contract import DigitalMarketplace
from digital_marketplace.config import (
    TOTAL_SUPPLY, 
    DECIMALS,
    FIXED_FEE_USDT,
    STAKING_THRESHOLD_USDT,
    STAKING_REWARD_PERCENTAGE
)

class TestDigitalMarketplace(unittest.TestCase):
    """Test cases for the DigitalMarketplace contract."""
    
    def setUp(self):
        """Set up test environment before each test."""
        # Create mock AlgodClient
        self.mock_client = MagicMock()
        self.mock_client.suggested_params.return_value = MagicMock()
        
        # Set up transaction confirmation mock
        self.mock_wait_for_confirmation = MagicMock()
        self.mock_wait_for_confirmation.return_value = {"asset-index": 12345, "confirmed-round": 1}
        
        # Create test addresses
        self.creator_address = "CREATOR_ADDRESS"
        self.creator_private_key = "CREATOR_PRIVATE_KEY"
        self.user_address = "USER_ADDRESS"
        self.user_private_key = "USER_PRIVATE_KEY"
        
        # Initialize contract
        self.contract = DigitalMarketplace(
            self.mock_client,
            self.creator_address,
            self.creator_private_key
        )
    
    @patch("algosdk.future.transaction.wait_for_confirmation")
    def test_create_token(self, mock_wait_for_confirmation):
        """Test token creation."""
        # Set up mocks
        mock_wait_for_confirmation.return_value = {"asset-index": 12345, "confirmed-round": 1}
        self.mock_client.send_transaction.return_value = "TX_ID"
        
        # Create token
        asset_id = self.contract.create_token()
        
        # Verify results
        self.assertEqual(asset_id, 12345)
        self.assertEqual(self.contract.asset_id, 12345)
        self.assertEqual(self.contract.token_holders[self.creator_address], TOTAL_SUPPLY * (10 ** DECIMALS))
        
        # Verify that the client was called with correct parameters
        self.mock_client.send_transaction.assert_called_once()
    
    @patch("algosdk.future.transaction.wait_for_confirmation")
    def test_deposit(self, mock_wait_for_confirmation):
        """Test token deposit."""
        # Set up contract state
        self.contract.asset_id = 12345
        self.contract.token_holders = {self.creator_address: TOTAL_SUPPLY * (10 ** DECIMALS)}
        
        # Set up mocks
        mock_wait_for_confirmation.return_value = {"confirmed-round": 1}
        self.mock_client.send_transactions.return_value = "TX_ID"
        
        # Mock ALGO to USDT conversion
        with patch("digital_marketplace.contract.algo_to_usdt") as mock_algo_to_usdt, \
             patch("digital_marketplace.contract.usdt_to_algo") as mock_usdt_to_algo:
            
            # Set up conversion mocks
            mock_algo_to_usdt.return_value = 1.0  # 1 ALGO = 1 USDT for testing
            mock_usdt_to_algo.return_value = 1000  # 1 USDT = 1000 microALGO for testing
            
            # Deposit 1 ALGO
            tx_id, tokens_received = self.contract.deposit(
                self.user_address, 
                self.user_private_key, 
                1_000_000  # 1 ALGO
            )
            
            # Verify results
            self.assertEqual(tx_id, "TX_ID")
            expected_tokens = int((1.0 - FIXED_FEE_USDT) * (10 ** DECIMALS))
            self.assertEqual(tokens_received, expected_tokens)
            self.assertEqual(self.contract.token_holders[self.user_address], expected_tokens)
    
    @patch("algosdk.future.transaction.wait_for_confirmation")
    def test_withdraw(self, mock_wait_for_confirmation):
        """Test token withdrawal."""
        # Set up contract state
        self.contract.asset_id = 12345
        token_amount = 100_000_000  # 1 token with 8 decimals
        self.contract.token_holders = {
            self.creator_address: TOTAL_SUPPLY * (10 ** DECIMALS) - token_amount,
            self.user_address: token_amount
        }
        
        # Set up mocks
        mock_wait_for_confirmation.return_value = {"confirmed-round": 1}
        self.mock_client.send_transactions.return_value = "TX_ID"
        
        # Mock USDT to ALGO conversion
        with patch("digital_marketplace.contract.usdt_to_algo") as mock_usdt_to_algo:
            
            # Set up conversion mocks - 1 USDT = 1000 microALGO for testing
            mock_usdt_to_algo.return_value = 1000
            
            # Withdraw all tokens
            tx_id, algo_received = self.contract.withdraw(
                self.user_address, 
                self.user_private_key, 
                token_amount
            )
            
            # Verify results
            self.assertEqual(tx_id, "TX_ID")
            expected_algo = 1000  # From our mock conversion
            self.assertEqual(algo_received, expected_algo)
            self.assertEqual(self.contract.token_holders[self.user_address], 0)
            self.assertEqual(
                self.contract.token_holders[self.creator_address], 
                TOTAL_SUPPLY * (10 ** DECIMALS)
            )
    
    def test_calculate_staking_rewards(self):
        """Test staking rewards calculation."""
        # Set up contract state
        self.contract.token_holders = {
            self.user_address: int(STAKING_THRESHOLD_USDT * (10 ** DECIMALS))
        }
        self.contract.last_staking_calculation = 0  # Force calculation
        
        # Mock current timestamp to ensure reward calculation
        with patch("digital_marketplace.contract.get_current_timestamp") as mock_timestamp, \
             patch("digital_marketplace.utils.usdt_to_algo") as mock_usdt_to_algo:
            
            mock_timestamp.return_value = 100000  # Arbitrary future timestamp
            mock_usdt_to_algo.return_value = 10000  # 10000 microALGO per USDT
            
            # Calculate rewards
            self.contract.calculate_staking_rewards()
            
            # Expected daily reward in USDT: 10000 * 0.05 / 365 ≈ 1.3699 USDT
            # Convert to ALGO using our mock: 1.3699 * 10000 ≈ 13699 microALGO
            expected_reward = int((STAKING_THRESHOLD_USDT * STAKING_REWARD_PERCENTAGE / 100 / 365) * 10000)
            
            # Verify rewards were calculated correctly
            self.assertAlmostEqual(
                self.contract.staking_rewards[self.user_address], 
                expected_reward,
                delta=2  # Allow small rounding differences
            )
    
    @patch("algosdk.future.transaction.wait_for_confirmation")
    def test_claim_staking_rewards(self, mock_wait_for_confirmation):
        """Test claiming staking rewards."""
        # Set up contract state
        rewards_amount = 100000  # 0.1 ALGO
        self.contract.staking_rewards = {self.user_address: rewards_amount}
        
        # Set up mocks
        mock_wait_for_confirmation.return_value = {"confirmed-round": 1}
        self.mock_client.send_transaction.return_value = "TX_ID"
        
        # Claim rewards
        tx_id, claimed_amount = self.contract.claim_staking_rewards(self.user_address)
        
        # Verify results
        self.assertEqual(tx_id, "TX_ID")
        self.assertEqual(claimed_amount, rewards_amount)
        self.assertEqual(self.contract.staking_rewards[self.user_address], 0)

if __name__ == "__main__":
    unittest.main()