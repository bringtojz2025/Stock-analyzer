"""
Quick Start Guide
เริ่มต้นใช้งาน Stock Analyzer อย่างรวดเร็ว
"""

# ============================================================
# 1. INSTALLATION
# ============================================================

# Windows - ใช้ setup.bat
setup.bat

# หรือ Linux/Mac - ใช้ setup.sh
bash setup.sh

# หรือ Manual installation
python -m venv venv
source venv/bin/activate  # Linux/Mac
# หรือ
venv\Scripts\activate  # Windows

pip install -r requirements.txt

# ============================================================
# 2. CONFIGURATION
# ============================================================

# Copy configuration template
cp .env.example .env  # Linux/Mac
# หรือ
copy .env.example .env  # Windows

# Edit .env ด้วย text editor
# - เพิ่ม Email settings (optional)
# - เพิ่ม Telegram Bot Token และ Chat ID (optional)
# - เพิ่ม Webhook URL (optional)


# ============================================================
# 3. QUICK RUN
# ============================================================

# Option A: ใช้ CLI
python cli.py analyze AAPL MSFT GOOGL -p 6mo

# Option B: ใช้ Web Dashboard
pip install streamlit
streamlit run dashboard.py

# Option C: ใช้ Python Script
python main.py


# ============================================================
# 4. COMMON COMMANDS
# ============================================================

# วิเคราะห์หุ้นเดียว
python cli.py analyze AAPL

# วิเคราะห์หุ้นหลายตัว
python cli.py analyze AAPL MSFT GOOGL TSLA AMZN

# ระบุระยะเวลา
python cli.py analyze AAPL -p 1y  # 1 year
python cli.py analyze AAPL -p 6mo  # 6 months
python cli.py analyze AAPL -p 3mo  # 3 months

# หาโอกาสซื้อ (Confidence >= 60%)
python cli.py buy AAPL MSFT GOOGL

# หาโอกาสซื้อ (Confidence >= 70%)
python cli.py buy AAPL MSFT GOOGL -c 0.7

# หาโอกาสขาย
python cli.py sell AAPL MSFT GOOGL

# หาหุ้นโดดเด่น
python cli.py hot AAPL MSFT GOOGL TSLA AMZN NFLX


# ============================================================
# 5. WEB DASHBOARD
# ============================================================

# Install Streamlit (if not installed)
pip install streamlit

# Run dashboard
streamlit run dashboard.py

# Access at http://localhost:8501
# Features:
# - Real-time stock analysis
# - Buy/Sell signal detection
# - Hot stocks overview
# - Technical indicators visualization


# ============================================================
# 6. PYTHON USAGE EXAMPLES
# ============================================================

from main import StockAnalyzerApp

# Initialize
app = StockAnalyzerApp()

# Analyze single stock
result = app.analyze_single_stock('AAPL', period='1y')
app.print_analysis_summary('AAPL')

# Analyze multiple stocks
results = app.analyze_multiple_stocks(
    ['AAPL', 'MSFT', 'GOOGL'], 
    period='6mo'
)

# Find buy opportunities
buy_opps = app.find_buy_opportunities(
    ['AAPL', 'MSFT', 'GOOGL'],
    min_confidence=0.6
)

for opp in buy_opps:
    print(f"{opp['symbol']}: {opp['confidence']:.1%}")
    print(f"  Entry: ${opp['entry_price']:.2f}")
    print(f"  Target: ${opp['target_price']:.2f}")

# Find sell opportunities
sell_opps = app.find_sell_opportunities(['AAPL', 'MSFT', 'GOOGL'])

# Get hot stocks
hot = app.get_hot_stocks(['AAPL', 'MSFT', 'GOOGL'])
print(f"Strong Buys: {len(hot['strong_buys'])}")
print(f"Strong Sells: {len(hot['strong_sells'])}")

# Save results
app.save_results_to_json('results.json')


# ============================================================
# 7. WITH NOTIFICATIONS
# ============================================================

from src.notifications.notifier import NotificationManager

app = StockAnalyzerApp()
notifications = NotificationManager()

# Add Telegram notification
notifications.add_telegram_notification('YOUR_BOT_TOKEN', 'YOUR_CHAT_ID')

# Analyze and get signals
result = app.analyze_single_stock('AAPL')
signals = result['signals']

# Send notification if buy signal
if signals['buy']:
    notifications.notify_all(
        'AAPL',
        'BUY',
        result['technical']
    )


# ============================================================
# 8. UNDERSTANDING OUTPUT
# ============================================================

# Buy Signal Example:
# 💚 BUY OPPORTUNITIES
# 1. AAPL
#    Confidence: 75%
#    Entry: $189.50
#    Target: $198.98
#    Stop Loss: $183.82
#    Potential Profit: 5.0%
#    Reasons:
#      • Golden Cross (SMA 20 > 50 > 200)
#      • RSI Oversold (25.50)
#      • MACD Bullish

# Signal Levels:
# 🟢 Green = BUY (confidence 60-80%)
# 🟢🟢 Strong Buy (confidence > 80%)
# 🔴 Red = SELL (confidence 60-80%)
# 🔴🔴 Strong Sell (confidence > 80%)
# 🟡 Yellow = HOLD


# ============================================================
# 9. STOCK LIST (PRE-CONFIGURED)
# ============================================================

STOCKS = [
    # Tech
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NFLX', 'NVDA',
    
    # Banks
    'JPM', 'BAC', 'WFC', 'GS', 'MS',
    
    # Healthcare
    'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK'
]

# You can add your own stocks!
python cli.py analyze TSLA NVDA AMD INTC


# ============================================================
# 10. TIPS & BEST PRACTICES
# ============================================================

# 1. Use multiple timeframes for confirmation
python cli.py analyze AAPL -p 1mo
python cli.py analyze AAPL -p 3mo
python cli.py analyze AAPL -p 1y

# 2. Always check fundamentals before investing
# Look at P/E, Dividend Yield, Debt/Equity in output

# 3. Use appropriate confidence threshold
# 0.6 = Moderate (60% confidence)
# 0.7 = Strong (70% confidence)
# 0.8 = Very Strong (80% confidence)

# 4. Never trade based on single signal alone
# Always confirm with multiple indicators

# 5. Always use stop loss (3% default)
# Always set profit target (5% default)

# 6. Diversify - don't put all money in one stock

# 7. Remember: Past performance ≠ Future results!


# ============================================================
# 11. TROUBLESHOOTING
# ============================================================

# Error: "yfinance not installed"
# Solution: pip install yfinance

# Error: "No data found for symbol"
# Solution: Check if symbol is valid (e.g., AAPL not AA)

# Error: "Connection timeout"
# Solution: Yahoo Finance server may be down, try again later

# Dashboard not loading?
# Solution: pip install streamlit

# Check logs:
# tail -f logs/stock_analyzer.log  # Linux/Mac
# type logs\stock_analyzer.log  # Windows


# ============================================================
# 12. NEXT STEPS
# ============================================================

# 1. Read README.md for detailed documentation
# 2. Check ARCHITECTURE.md for system design
# 3. Read USAGE.md for advanced features
# 4. Customize config/settings.py for your needs
# 5. Set up notifications in .env
# 6. Backtest strategies with historical data
# 7. Monitor signals regularly


# ============================================================
# 13. IMPORTANT DISCLAIMER
# ============================================================

# ⚠️  This tool is for educational and analysis purposes only
# ⚠️  NOT investment advice or financial recommendation
# ⚠️  Past performance doesn't guarantee future results
# ⚠️  Always do your own research before investing
# ⚠️  Trading carries risk of financial loss
# ⚠️  Consult with a financial advisor if needed
# ⚠️  Use at your own risk!


print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🚀 Stock Analyzer Ready to Use! 🚀                  ║
║                                                              ║
║   Next step: python cli.py analyze AAPL MSFT GOOGL          ║
║                                                              ║
║   or                                                         ║
║                                                              ║
║   Next step: streamlit run dashboard.py                     ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")
