"""
Tests for the utility functions.
"""
import unittest
from unittest.mock import patch, MagicMock

from digital_marketplace.utils import (
    get_current_timestamp,
    get_algo_price_usdt,
    algo_to_usdt,
    usdt_to_algo,
    format_amount
)

class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    @patch("time.time")
    def test_get_current_timestamp(self, mock_time):
        """Test getting current timestamp."""
        mock_time.return_value = 1234567890.123
        
        timestamp = get_current_timestamp()
        
        self.assertEqual(timestamp, 1234567890)
    
    @patch("digital_marketplace.utils.requests.get")
    @patch("digital_marketplace.utils.get_current_timestamp")
    def test_get_algo_price_usdt(self, mock_timestamp, mock_get):
        """Test getting ALGO price in USDT."""
        # Set up mocks
        mock_timestamp.return_value = 1000
        
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "algorand": {
                "usd": 0.25
            }
        }
        mock_get.return_value = mock_response
        
        # Test price retrieval
        price = get_algo_price_usdt()
        
        self.assertEqual(price, 0.25)
        mock_get.assert_called_once()
        
        # Test caching
        mock_get.reset_mock()
        mock_timestamp.return_value = 1100  # Within cache duration
        
        price = get_algo_price_usdt()
        
        self.assertEqual(price, 0.25)
        mock_get.assert_not_called()  # API not called due to cache
        
        # Test cache expiration
        mock_get.reset_mock()
        mock_timestamp.return_value = 2000  # Outside cache duration
        
        mock_response.json.return_value = {
            "algorand": {
                "usd": 0.30
            }
        }
        
        price = get_algo_price_usdt()
        
        self.assertEqual(price, 0.30)
        mock_get.assert_called_once()  # API called again after cache expired
    
    @patch("digital_marketplace.utils.get_algo_price_usdt")
    def test_algo_to_usdt(self, mock_get_price):
        """Test converting ALGO to USDT."""
        mock_get_price.return_value = 0.20  # 1 ALGO = $0.20
        
        # Test converting 1 ALGO
        usdt_amount = algo_to_usdt(1_000_000)  # 1 ALGO in microALGO
        
        self.assertEqual(usdt_amount, 0.20)
        
        # Test converting 5 ALGO
        usdt_amount = algo_to_usdt(5_000_000)  # 5 ALGO in microALGO
        
        self.assertEqual(usdt_amount, 1.00)
    
    @patch("digital_marketplace.utils.get_algo_price_usdt")
    def test_usdt_to_algo(self, mock_get_price):
        """Test converting USDT to ALGO."""
        mock_get_price.return_value = 0.20  # 1 ALGO = $0.20
        
        # Test converting $1 USDT
        algo_amount = usdt_to_algo(1.0)
        
        self.assertEqual(algo_amount, 5_000_000)  # Should be 5 ALGO in microALGO
        
        # Test converting $0.10 USDT
        algo_amount = usdt_to_algo(0.10)
        
        self.assertEqual(algo_amount, 500_000)  # Should be 0.5 ALGO in microALGO
    
    def test_format_amount(self):
        """Test formatting amounts."""
        # Test formatting integer with decimals
        formatted = format_amount(1_000_000_000, 8)
        self.assertEqual(formatted, "10.00000000")
        
        # Test formatting float
        formatted = format_amount(10.5, 2)
        self.assertEqual(formatted, "10.50")
        
        # Test formatting integer without decimals
        formatted = format_amount(42, 0)
        self.assertEqual(formatted, "42")
        
        # Test default decimals
        formatted = format_amount(1_000_000_000)
        self.assertEqual(formatted, "10.00000000")

if __name__ == "__main__":
    unittest.main()