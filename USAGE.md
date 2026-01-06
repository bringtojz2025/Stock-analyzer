# Running the Stock Analyzer

## Option 1: Command Line Interface (CLI)

### Analyze single stock
```bash
python cli.py analyze AAPL
```

### Analyze multiple stocks
```bash
python cli.py analyze AAPL MSFT GOOGL -p 6mo
```

### Find buy opportunities
```bash
python cli.py buy AAPL MSFT GOOGL -c 0.7
```

### Find sell opportunities
```bash
python cli.py sell AAPL MSFT GOOGL
```

### Find hot stocks
```bash
python cli.py hot AAPL MSFT GOOGL TSLA AMZN
```

---

## Option 2: Web Dashboard (Streamlit)

### Install Streamlit
```bash
pip install streamlit
```

### Run Dashboard
```bash
streamlit run dashboard.py
```

Access at: http://localhost:8501

---

## Option 3: Direct Python Usage

### Basic Analysis
```python
from main import StockAnalyzerApp

app = StockAnalyzerApp()

# Analyze single stock
result = app.analyze_single_stock('AAPL', period='1y')
app.print_analysis_summary('AAPL')

# Find buy opportunities
buy_opps = app.find_buy_opportunities(['AAPL', 'MSFT', 'GOOGL'])
for opp in buy_opps:
    print(f"{opp['symbol']}: {opp['confidence']:.1%} confidence")

# Get hot stocks
hot = app.get_hot_stocks(['AAPL', 'MSFT', 'GOOGL'])
print(f"Strong Buys: {len(hot['strong_buys'])}")
print(f"Strong Sells: {len(hot['strong_sells'])}")
```

### With Notifications
```python
from main import StockAnalyzerApp
from src.notifications.notifier import NotificationManager

app = StockAnalyzerApp()

# Setup notifications
manager = NotificationManager()
manager.add_telegram_notification('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')

# Analyze and notify
result = app.analyze_single_stock('AAPL')
signals = result['signals']

if signals['buy']:
    manager.notify_all(
        'AAPL',
        'BUY',
        result['technical'],
        reasons=signals['reasons']
    )
```

---

## Sample Output

### Console Output
```
============================================================
STOCK ANALYSIS REPORT: AAPL
============================================================

📊 TECHNICAL INDICATORS:
  Current Price: $189.50
  SMA 20: $185.30
  SMA 50: $182.10
  SMA 200: $180.00
  RSI (14): 65.50
  MACD: 0.1234
  ATR: 1.5432

📈 SIGNALS:
  Signal: BUY
  Confidence: 75.00%
  Reasons:
    • Golden Cross (SMA 20 > 50 > 200)
    • RSI Oversold (65.50)
    • MACD Bullish

🎯 TRADING POINTS:
  Entry Price: $189.50
  Target Price: $198.98
  Stop Loss: $183.82

💰 VALUATION:
  P/E Ratio: 28.50
  Forward P/E: 24.30
  Dividend Yield: 0.45%

============================================================
```

---

## Tips for Best Results

1. **Use Multiple Timeframes**: Analyze with 1mo, 3mo, 6mo, 1y for better accuracy
2. **Combine Signals**: Don't rely on single signal, look for multiple confirmations
3. **Check Fundamentals**: Always check P/E, Debt/Equity before buying
4. **Risk Management**: Always use stop loss and profit targets
5. **Diversify**: Don't put all eggs in one basket

---

**Remember**: Past performance doesn't guarantee future results!
