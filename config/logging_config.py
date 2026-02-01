import logging
import os
from datetime import datetime

def setup_logging():
    """Configure logging for the trading bot."""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt=date_format,
        handlers=[
            logging.FileHandler('logs/trading_bot.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)
