#!/usr/bin/env python3
"""
Binance Futures Testnet Trading Bot
CLI entry point for placing orders
"""

import os
import sys
import click
from dotenv import load_dotenv
from config.logging_config import setup_logging
from src.client import BinanceFuturesClient
from src.order_service import OrderService

# Load environment variables
load_dotenv()

# Setup logging
logger = setup_logging()

@click.command()
@click.option('--symbol', required=True, help='Trading pair (e.g., BTCUSDT)')
@click.option('--side', required=True, type=click.Choice(['BUY', 'SELL'], case_sensitive=False), 
              help='Order side')
@click.option('--order-type', required=True, type=click.Choice(['MARKET', 'LIMIT'], case_sensitive=False),
              help='Order type')
@click.option('--quantity', required=True, type=float, help='Order quantity')
@click.option('--price', type=float, default=None, help='Order price (required for LIMIT orders)')
def main(symbol: str, side: str, order_type: str, quantity: float, price: float):
    """
    Binance Futures Testnet Trading Bot
    
    Place MARKET or LIMIT orders on Binance Futures Testnet (USDT-M).
    
    Examples:
    
        Market order:
        python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
        
        Limit order:
        python main.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 45000
    """
    logger.info("="*60)
    logger.info("Starting Binance Futures Trading Bot")
    logger.info("="*60)
    
    # Get API credentials
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        logger.error("API credentials not found in environment variables")
        print("\n❌ Error: API credentials not found!")
        print("Please create a .env file with BINANCE_API_KEY and BINANCE_API_SECRET\n")
        sys.exit(1)
    
    try:
        # Initialize client
        client = BinanceFuturesClient(api_key, api_secret)
        
        # Test connectivity
        if not client.test_connectivity():
            print("\n❌ Failed to connect to Binance API\n")
            sys.exit(1)
        
        # Initialize order service
        order_service = OrderService(client)
        
        # Execute order
        result = order_service.execute_order(
            symbol=symbol,
            side=side.upper(),
            order_type=order_type.upper(),
            quantity=quantity,
            price=price
        )
        
        # Exit with appropriate code
        if result['success']:
            logger.info("Order execution completed successfully")
            sys.exit(0)
        else:
            logger.error(f"Order execution failed: {result.get('error')}")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        print("\n\n⚠️  Operation cancelled by user\n")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        print(f"\n❌ Unexpected error: {e}\n")
        sys.exit(1)

if __name__ == '__main__':
    main()
