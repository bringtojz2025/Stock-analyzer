# Stock Analyzer Architecture

## Project Structure

```
stock_analyzer/
├── main.py                 # Main application entry point
├── cli.py                  # Command-line interface
├── dashboard.py            # Web dashboard (Streamlit)
├── requirements.txt        # Python dependencies
├── .env.example           # Configuration template
├── setup.sh              # Setup script for Linux/Mac
├── setup.bat             # Setup script for Windows
│
├── config/
│   ├── __init__.py
│   └── settings.py       # Configuration settings
│
├── src/
│   ├── __init__.py
│   ├── data/
│   │   ├── __init__.py
│   │   └── fetcher.py    # Data fetching from APIs
│   │
│   ├── analysis/
│   │   ├── __init__.py
│   │   └── technical.py  # Technical indicators
│   │
│   ├── signals/
│   │   ├── __init__.py
│   │   └── generator.py  # Signal generation
│   │
│   ├── notifications/
│   │   ├── __init__.py
│   │   └── notifier.py   # Notification system
│   │
│   └── ai/
│       ├── __init__.py
│       └── models.py     # AI/ML models
│
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py  # Unit tests
│
└── README.md             # Documentation
```

---

## Data Flow Architecture

```
┌─────────────────────────────────────────┐
│     Data Sources                        │
│  (Yahoo Finance, Alpha Vantage, etc)   │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│     StockDataFetcher                    │
│  - Fetch historical data                │
│  - Fetch real-time prices               │
│  - Fetch fundamental data               │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌─────────────────┐ ┌──────────────────┐
│ TechnicalAnalyzer │ FundamentalAnalyzer│
│ - SMA, EMA       │ │ - P/E Ratio      │
│ - RSI, MACD      │ │ - Dividend Yield │
│ - Bollinger Bands │ │ - Financial Health
│ - ATR, Stochastic │ │ - Valuation     │
└────────┬────────┘ └────────┬─────────┘
         │                   │
         └──────────┬────────┘
                    ▼
         ┌──────────────────────────┐
         │  SignalGenerator         │
         │ ┌─────────────────────┐  │
         │ │ Rule-based Engine   │  │
         │ │ (Technical Signals) │  │
         │ └─────────────────────┘  │
         │ ┌─────────────────────┐  │
         │ │ AI Models (ML)      │  │
         │ │ (Classification)    │  │
         │ └─────────────────────┘  │
         └──────────┬───────────────┘
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
    ┌─────────┐          ┌──────────────┐
    │   BUY   │          │   SELL       │
    │ SIGNALS │          │ SIGNALS      │
    │ + Entry │          │ + Exit       │
    │ +Target │          │ + Reasons    │
    │ +SL     │          │ + Confidence │
    └────┬────┘          └────┬─────────┘
         │                    │
         └────────┬───────────┘
                  ▼
     ┌───────────────────────────┐
     │  NotificationManager      │
     │ ┌─────────────────────┐   │
     │ │ Email Notification  │   │
     │ ├─────────────────────┤   │
     │ │ Telegram Notification   │
     │ ├─────────────────────┤   │
     │ │ Webhook Notification    │
     │ └─────────────────────┘   │
     └───────────┬────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
    ┌────────┐        ┌─────────┐
    │ User's │        │External │
    │ Email  │        │Services │
    └────────┘        └─────────┘
```

---

## Module Responsibilities

### 1. **Data Fetcher** (`src/data/fetcher.py`)
- Retrieves stock data from Yahoo Finance
- Caches data for performance
- Handles multiple stocks simultaneously
- Provides historical and fundamental data

**Key Classes:**
- `StockDataFetcher`: Fetches price and volume data
- `FundamentalAnalyzer`: Analyzes company valuation and health

### 2. **Technical Analysis** (`src/analysis/technical.py`)
- Calculates technical indicators
- Supports 8+ different indicators
- Provides comprehensive technical summary

**Key Methods:**
- `calculate_sma()`: Simple Moving Average
- `calculate_rsi()`: Relative Strength Index
- `calculate_macd()`: MACD indicator
- `calculate_bollinger_bands()`: Bollinger Bands
- `get_technical_summary()`: All indicators at once

### 3. **Signal Generation** (`src/signals/generator.py`)
- Combines technical indicators for trading signals
- Implements rule-based logic for signal generation
- Includes ML-based signal prediction
- Calculates entry and exit points

**Key Classes:**
- `SignalGenerator`: Rule-based signal generation
- `AISignalGenerator`: ML-based signal prediction

### 4. **Notifications** (`src/notifications/notifier.py`)
- Sends alerts via multiple channels
- Supports Email, Telegram, Webhook
- Formats notifications with relevant data

**Key Classes:**
- `NotificationManager`: Central manager for all notifications
- `EmailNotification`: Email alerts
- `TelegramNotification`: Telegram alerts
- `WebhookNotification`: Webhook integration

### 5. **AI Models** (`src/ai/models.py`)
- Price prediction using ML
- Signal classification
- Anomaly detection
- Correlation analysis

**Key Classes:**
- `PricePredictor`: Predicts future prices
- `SignalClassifier`: Classifies buy/sell/hold signals
- `AnomalyDetector`: Detects unusual price movements
- `CorrelationAnalyzer`: Analyzes stock correlations

---

## Signal Generation Logic

### Rule-Based Signals
1. **Golden Cross**: SMA20 > SMA50 > SMA200 → BUY ✅
2. **Death Cross**: SMA20 < SMA50 < SMA200 → SELL ❌
3. **RSI Oversold**: RSI < 30 → BUY Signal 📊
4. **RSI Overbought**: RSI > 70 → SELL Signal 📊
5. **MACD Bullish**: MACD > Signal Line → BUY 📈
6. **MACD Bearish**: MACD < Signal Line → SELL 📉

### Confidence Scoring
- Combines multiple indicators
- Calculates percentage confidence (0-100%)
- Minimum threshold: 60% for action

### Entry/Exit Strategy
- **Entry**: Current price with analysis
- **Target**: 5% above entry
- **Stop Loss**: 3% below entry
- **Risk/Reward**: 1:1.67 ratio

---

## Configuration

### Key Settings (`config/settings.py`)

```python
# Stocks to monitor
STOCKS_TO_MONITOR = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', ...
]

# Technical parameters
TECHNICAL_CONFIG = {
    'sma_short': 20,
    'sma_medium': 50,
    'sma_long': 200,
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'bollinger_period': 20,
}

# Signal thresholds
SIGNAL_CONFIG = {
    'min_confidence': 0.6,
    'buy_threshold': 0.65,
    'sell_threshold': 0.65,
}

# Trading rules
TRADING_CONFIG = {
    'profit_target_percent': 5,
    'stop_loss_percent': 3,
}
```

---

## Usage Examples

### Command Line
```bash
# Analyze stocks
python cli.py analyze AAPL MSFT GOOGL -p 1y

# Find buy opportunities
python cli.py buy AAPL MSFT GOOGL -c 0.7

# Find hot stocks
python cli.py hot AAPL MSFT GOOGL TSLA AMZN
```

### Web Dashboard
```bash
streamlit run dashboard.py
```

### Python API
```python
from main import StockAnalyzerApp

app = StockAnalyzerApp()
result = app.analyze_single_stock('AAPL', period='1y')
app.print_analysis_summary('AAPL')
```

---

## Performance Considerations

1. **Caching**: Historical data is cached to reduce API calls
2. **Parallel Processing**: Multiple stocks analyzed simultaneously
3. **Vectorized Operations**: NumPy and Pandas for fast calculations
4. **Efficient ML**: Scikit-learn models for fast predictions

---

## Future Enhancements

1. ✅ Add more indicators (Ichimoku, Volume Profile)
2. ✅ Implement sentiment analysis
3. ✅ Add backtesting engine
4. ✅ Real-time trading bot
5. ✅ Portfolio management
6. ✅ Risk management features
7. ✅ Mobile app
8. ✅ Advanced ML models (LSTM, Transformer)

---

## Dependencies

### Core Libraries
- **yfinance**: Stock data
- **pandas**: Data manipulation
- **numpy**: Numerical computation
- **scikit-learn**: Machine learning

### Notification
- **requests**: HTTP requests
- **python-dotenv**: Environment variables

### Visualization
- **plotly**: Interactive charts
- **streamlit**: Web dashboard

### Testing
- **unittest**: Unit testing

---

**Architecture designed for scalability, maintainability, and extensibility** 🚀
