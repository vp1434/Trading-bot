import logging
from typing import Optional
from src.client import BinanceFuturesClient
from src.validators import OrderValidator, ValidationError

logger = logging.getLogger(__name__)

class OrderService:
    """Service layer for order operations."""
    
    def __init__(self, client: BinanceFuturesClient):
        """Initialize order service with Binance client."""
        self.client = client
        self.validator = OrderValidator()
    
    def execute_order(self, symbol: str, side: str, order_type: str, 
                     quantity: float, price: Optional[float] = None) -> dict:
        """
        Execute a trading order with validation.
        
        Args:
            symbol: Trading pair
            side: BUY or SELL
            order_type: MARKET or LIMIT
            quantity: Order quantity
            price: Order price (required for LIMIT)
        
        Returns:
            Order execution result
        """
        try:
            # Validate inputs
            validated = self.validator.validate_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price
            )
            
            # Print order summary
            self._print_order_summary(validated)
            
            # Place order
            response = self.client.place_order(
                symbol=validated['symbol'],
                side=validated['side'],
                order_type=validated['order_type'],
                quantity=validated['quantity'],
                price=validated['price']
            )
            
            # Print response
            self._print_order_response(response)
            
            return {
                'success': True,
                'order': response
            }
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n❌ Validation Error: {e}\n")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'validation'
            }
        except Exception as e:
            logger.error(f"Order execution failed: {e}")
            print(f"\n❌ Order Failed: {e}\n")
            return {
                'success': False,
                'error': str(e),
                'error_type': 'execution'
            }
    
    def _print_order_summary(self, order_params: dict):
        """Print order request summary."""
        print("\n" + "="*50)
        print("📋 ORDER REQUEST SUMMARY")
        print("="*50)
        print(f"Symbol:      {order_params['symbol']}")
        print(f"Side:        {order_params['side']}")
        print(f"Type:        {order_params['order_type']}")
        print(f"Quantity:    {order_params['quantity']}")
        if order_params['price']:
            print(f"Price:       {order_params['price']}")
        print("="*50 + "\n")
    
    def _print_order_response(self, response: dict):
        """Print order response details."""
        print("\n" + "="*50)
        print("✅ ORDER RESPONSE")
        print("="*50)
        print(f"Order ID:    {response.get('orderId', 'N/A')}")
        print(f"Status:      {response.get('status', 'N/A')}")
        print(f"Symbol:      {response.get('symbol', 'N/A')}")
        print(f"Side:        {response.get('side', 'N/A')}")
        print(f"Type:        {response.get('type', 'N/A')}")
        print(f"Quantity:    {response.get('origQty', 'N/A')}")
        print(f"Executed:    {response.get('executedQty', 'N/A')}")
        
        if 'avgPrice' in response and response['avgPrice']:
            print(f"Avg Price:   {response['avgPrice']}")
        
        if 'price' in response and response['price']:
            print(f"Price:       {response['price']}")
        
        print("="*50)
        print("✅ Order placed successfully!")
        print("="*50 + "\n")
