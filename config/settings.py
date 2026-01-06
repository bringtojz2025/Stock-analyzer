"""
Configuration Settings
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Stock Analysis Settings
STOCKS_TO_MONITOR = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
    'META', 'NFLX', 'NVDA', 'AMD', 'INTEL',
    'JPM', 'BAC', 'WFC', 'GS', 'MS',
    'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK'
]

# Technical Analysis Parameters
TECHNICAL_CONFIG = {
    'sma_short': 20,      # Short-term SMA
    'sma_medium': 50,     # Medium-term SMA
    'sma_long': 200,      # Long-term SMA
    'rsi_period': 14,     # RSI period
    'rsi_overbought': 70, # RSI overbought threshold
    'rsi_oversold': 30,   # RSI oversold threshold
    'macd_fast': 12,      # MACD fast period
    'macd_slow': 26,      # MACD slow period
    'macd_signal': 9,     # MACD signal period
    'bollinger_period': 20,    # Bollinger Bands period
    'bollinger_std': 2,        # Bollinger Bands std dev
    'atr_period': 14,     # ATR period
}

# Signal Generation Settings
SIGNAL_CONFIG = {
    'min_confidence': 0.6,  # Minimum confidence for signals
    'buy_threshold': 0.65,  # Threshold for BUY signal
    'sell_threshold': 0.65, # Threshold for SELL signal
}

# Entry/Exit Settings
TRADING_CONFIG = {
    'profit_target_percent': 5,    # 5% profit target
    'stop_loss_percent': 3,        # 3% stop loss
    'position_size_percent': 2,    # 2% per position
}

# Notification Settings
NOTIFICATION_CONFIG = {
    'email': {
        'enabled': os.getenv('EMAIL_NOTIFICATIONS_ENABLED', 'False') == 'True',
        'smtp_server': os.getenv('SMTP_SERVER', 'smtp.gmail.com'),
        'smtp_port': int(os.getenv('SMTP_PORT', 587)),
        'sender_email': os.getenv('SENDER_EMAIL', ''),
        'sender_password': os.getenv('SENDER_PASSWORD', ''),
        'recipient_email': os.getenv('RECIPIENT_EMAIL', ''),
    },
    'telegram': {
        'enabled': os.getenv('TELEGRAM_NOTIFICATIONS_ENABLED', 'False') == 'True',
        'bot_token': os.getenv('TELEGRAM_BOT_TOKEN', ''),
        'chat_id': os.getenv('TELEGRAM_CHAT_ID', ''),
    },
    'webhook': {
        'enabled': os.getenv('WEBHOOK_NOTIFICATIONS_ENABLED', 'False') == 'True',
        'url': os.getenv('WEBHOOK_URL', ''),
    }
}

# Data Fetching Settings
DATA_CONFIG = {
    'period': '1y',         # Default period
    'interval': '1d',       # Default interval
    'cache_enabled': True,  # Cache historical data
    'cache_duration': 3600, # Cache duration in seconds
}

# Logging Settings
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/stock_analyzer.log'
}

# API Settings
API_CONFIG = {
    'yfinance': {
        'enabled': True,
        'timeout': 30
    },
    'alpha_vantage': {
        'enabled': False,
        'api_key': os.getenv('ALPHA_VANTAGE_API_KEY', ''),
        'timeout': 30
    },
    'finnhub': {
        'enabled': False,
        'api_key': os.getenv('FINNHUB_API_KEY', ''),
        'timeout': 30
    }
}
