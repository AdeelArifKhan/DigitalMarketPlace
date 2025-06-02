"""
Utility functions for the Digital Marketplace contract.
"""
import time
from typing import Union, Dict
import requests

# Cache for ALGO price
_algo_price_cache: Dict[int, float] = {}
_algo_price_last_update = 0
_CACHE_DURATION = 300  # 5 minutes in seconds

def get_current_timestamp() -> int:
    """
    Get the current UNIX timestamp.
    
    Returns:
        int: Current timestamp in seconds
    """
    return int(time.time())

def get_algo_price_usdt() -> float:
    """
    Get the current price of ALGO in USDT.
    
    Uses caching to reduce API calls. Price is updated every 5 minutes.
    
    Returns:
        float: Current ALGO price in USDT
    """
    global _algo_price_last_update
    
    current_time = get_current_timestamp()
    
    # Check if we need to update the cache
    if current_time - _algo_price_last_update > _CACHE_DURATION:
        try:
            # In a real implementation, you'd use a reliable price oracle or API
            # This is a simplified example using a public API
            response = requests.get(
                "https://api.coingecko.com/api/v3/simple/price",
                params={"ids": "algorand", "vs_currencies": "usd"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                price = data.get("algorand", {}).get("usd", 0.1945)  # Default to 0.1945 if API fails
                
                # Update cache
                _algo_price_cache[current_time] = price
                _algo_price_last_update = current_time
                
                return price
            else:
                # If API call fails, use the last known price or default
                print(f"Failed to get ALGO price: {response.status_code}")
        
        except Exception as e:
            print(f"Error getting ALGO price: {e}")
    
    # Use the most recent cached price, or default to 0.1945 if no cache exists
    if _algo_price_cache:
        latest_time = max(_algo_price_cache.keys())
        return _algo_price_cache[latest_time]
    
    return 0.1945  # Default ALGO price in USDT

def algo_to_usdt(algo_amount: int) -> float:
    """
    Convert ALGO amount (in microALGO) to USDT.
    
    Args:
        algo_amount: Amount in microALGO (1 ALGO = 1,000,000 microALGO)
        
    Returns:
        float: Equivalent amount in USDT
    """
    algo_price = get_algo_price_usdt()
    algo_value = algo_amount / 1_000_000  # Convert microALGO to ALGO
    return algo_value * algo_price

def usdt_to_algo(usdt_amount: float) -> int:
    """
    Convert USDT amount to ALGO (in microALGO).
    
    Args:
        usdt_amount: Amount in USDT
        
    Returns:
        int: Equivalent amount in microALGO
    """
    algo_price = get_algo_price_usdt()
    
    # Prevent division by zero
    if algo_price <= 0:
        algo_price = 0.1945  # Default to 0.1945 if price is invalid
    
    algo_value = usdt_amount / algo_price
    return int(algo_value * 1_000_000)  # Convert ALGO to microALGO and return as integer

def format_amount(amount: Union[int, float], decimals: int = 8) -> str:
    """
    Format an amount with the specified number of decimals.
    
    Args:
        amount: The amount to format
        decimals: Number of decimal places
        
    Returns:
        str: Formatted amount as a string
    """
    if isinstance(amount, int) and decimals > 0:
        return f"{amount / (10 ** decimals):.{decimals}f}"
    
    if isinstance(amount, float):
        return f"{amount:.{decimals}f}"
    
    return str(amount)