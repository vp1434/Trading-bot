# Binance Futures Testnet Trading Bot

A simplified Python trading bot for placing orders on Binance Futures Testnet (USDT-M).

## Features

- Support for MARKET and LIMIT orders
- BUY and SELL sides
- Clean code structure with separation of concerns
- Comprehensive input validation
- Logging of all operations
- Error handling for API and network issues

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Credentials

Create a `.env` file in the project root:

```
BINANCE_API_KEY=your_api_key_here
BINANCE_API_SECRET=your_api_secret_here
```

**Important:** Get your API credentials from [Binance Futures Testnet](https://testnet.binancefuture.com)

### 3. Run the Bot

#### Market Order Example

```bash
python main.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.001
```

#### Limit Order Example

```bash
python main.py --symbol BTCUSDT --side SELL --order-type LIMIT --quantity 0.001 --price 45000
```

## Command Line Arguments

- `--symbol`: Trading pair (e.g., BTCUSDT)
- `--side`: Order side (BUY or SELL)
- `--order-type`: Order type (MARKET or LIMIT)
- `--quantity`: Order quantity
- `--price`: Order price (required for LIMIT orders only)

## Project Structure

```
.
├── main.py                 # CLI entry point
├── src/
│   ├── __init__.py
│   ├── client.py          # Binance API client
│   ├── order_service.py   # Order logic layer
│   └── validators.py      # Input validation
├── config/
│   └── logging_config.py  # Logging configuration
├── logs/                  # Log files directory
├── .env                   # API credentials (create this)
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Logging

All operations are logged to `logs/trading_bot.log` with timestamps, including:
- API requests and responses
- Validation errors
- Network errors
- Order execution results

## Error Handling

The bot handles:
- Invalid input parameters
- Missing required fields
- Binance API errors
- Network and timeout issues
- Authentication failures

## Assumptions

- Python 3.8 or higher
- Active Binance Futures Testnet account
- Valid API key with trading permissions
- Sufficient testnet balance for orders
