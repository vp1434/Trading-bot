import logging
import os
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger(__name__)

class BinanceFuturesClient:
    """Wrapper for Binance Futures API client."""
    
    TESTNET_URL = 'https://testnet.binancefuture.com'
    
    def __init__(self, api_key: str, api_secret: str):
        """Initialize Binance Futures client for testnet."""
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required")
        
        logger.info("Initializing Binance Futures Testnet client...")
        
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.API_URL = self.TESTNET_URL
        
        logger.info("Client initialized successfully")
    
    def test_connectivity(self) -> bool:
        """Test API connectivity."""
        try:
            logger.info("Testing API connectivity...")
            self.client.futures_ping()
            logger.info("API connectivity test successful")
            return True
        except Exception as e:
            logger.error(f"API connectivity test failed: {e}")
            return False
    
    def place_order(self, symbol: str, side: str, order_type: str, 
                   quantity: float, price: float = None) -> dict:
        """
        Place an order on Binance Futures.
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT orders)
        
        Returns:
            Order response from Binance API
        
        Raises:
            BinanceAPIException: If API returns an error
            BinanceRequestException: If request fails
        """
        try:
            params = {
                'symbol': symbol,
                'side': side,
                'type': order_type,
                'quantity': quantity
            }
            
            if order_type == 'LIMIT':
                params['price'] = price
                params['timeInForce'] = 'GTC'  # Good Till Cancel
            
            logger.info(f"Placing {order_type} {side} order: {params}")
            
            response = self.client.futures_create_order(**params)
            
            logger.info(f"Order placed successfully: {response}")
            return response
            
        except BinanceAPIException as e:
            logger.error(f"Binance API error: {e.status_code} - {e.message}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance request error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error placing order: {e}")
            raise
    
    def get_account_info(self) -> dict:
        """Get futures account information."""
        try:
            logger.info("Fetching account information...")
            return self.client.futures_account()
        except Exception as e:
            logger.error(f"Error fetching account info: {e}")
            raise
