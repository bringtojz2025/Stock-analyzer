# Stock Analyzer - USA Stock Analysis Tool

แอปพลิเคชันสำหรับวิเคราะห์หุ้น USA เพื่อหาจุดซื้อ (Buy Signals) และจุดขาย (Sell Signals) โดยใช้ AI และข้อมูลจากหลายแหล่ง

## ✨ คุณสมบัติ

### 1. **Data Fetcher** 📊
- ดึงข้อมูลราคาหุ้นจาก Yahoo Finance
- ดึงข้อมูลพื้นฐานของบริษัท (P/E, Dividend, Market Cap เป็นต้น)
- รองรับหุ้นหลายตัวพร้อมกัน
- Caching ข้อมูลเพื่อประหยัด API calls

### 2. **Technical Analysis** 📈
ใช้ Indicators ต่อไปนี้:
- **SMA (Simple Moving Average)**: MA20, MA50, MA200
- **EMA (Exponential Moving Average)**: เพื่อ trend tracking
- **RSI (Relative Strength Index)**: วัด Momentum
- **MACD**: ติดตามการเปลี่ยนแปลง Trend
- **Bollinger Bands**: วัดความผันผวน
- **ATR (Average True Range)**: วัด volatility
- **Stochastic Oscillator**: ติดตาม Momentum

### 3. **Fundamental Analysis** 💼
วิเคราะห์คุณภาพบริษัท:
- **Valuation**: P/E, Forward P/E, PEG, Price-to-Book
- **Financial Health**: Debt/Equity, Current Ratio, Profit Margin
- **Growth Metrics**: Revenue Growth, ROE, ROA
- **Dividend Analysis**: Dividend Yield

### 4. **Signal Generation** 🎯
สร้าง Buy/Sell signals จาก:
- **Rule-based Engine**: ใช้ Technical Indicators
- **AI Model**: Machine Learning (Random Forest)
- **Confidence Scoring**: ระดับความมั่นใจ 0-100%

### 5. **Entry/Exit Points** 🎲
คำนวณ:
- Entry Price: ราคาเข้าสุดปัจจุบัน
- Target Price: 5% profit target
- Stop Loss: 3% stop loss

### 6. **Notifications** 🔔
รองรับหลายช่องทาง:
- 📧 **Email**: ส่งรายงาน HTML
- 📱 **Telegram**: ส่ง Message ทันที
- 🔗 **Webhook**: Integration กับระบบอื่น

## 🚀 Installation

### ข้อกำหนด
- Python 3.8+
- pip

### ขั้นตอนการติดตั้ง

1. Clone repository:
```bash
git clone <repository>
cd stock_analyzer
```

2. สร้าง Virtual Environment:
```bash
python -m venv venv
source venv/bin/activate  # บน macOS/Linux
# หรือ
venv\Scripts\activate  # บน Windows
```

3. ติดตั้ง Dependencies:
```bash
pip install -r requirements.txt
```

4. สร้างไฟล์ Configuration:
```bash
cp .env.example .env
# แก้ไข .env เพื่อเพิ่ม API keys และ settings
```

## 📖 วิธีการใช้งาน

### Basic Usage

```python
from main import StockAnalyzerApp

# สร้าง App instance
app = StockAnalyzerApp()

# วิเคราะห์หุ้นตัวเดียว
result = app.analyze_single_stock('AAPL', period='1y')

# วิเคราะห์หุ้นหลายตัว
results = app.analyze_multiple_stocks(
    ['AAPL', 'MSFT', 'GOOGL'], 
    period='6mo'
)

# หาโอกาสซื้อ
buy_opps = app.find_buy_opportunities(['AAPL', 'MSFT', 'GOOGL'])

# หาโอกาสขาย
sell_opps = app.find_sell_opportunities(['AAPL', 'MSFT', 'GOOGL'])

# หาหุ้นโดดเด่น
hot_stocks = app.get_hot_stocks(['AAPL', 'MSFT', 'GOOGL'])

# บันทึกผลลัพธ์
app.save_results_to_json('results.json')

# พิมพ์สรุป
app.print_analysis_summary('AAPL')
```

### รัน Main Program

```bash
python main.py
```

## 📊 ผลลัพธ์ที่ได้

แต่ละการวิเคราะห์จะให้:

```json
{
  "symbol": "AAPL",
  "timestamp": "2024-01-06T15:30:00",
  "technical": {
    "latest_price": 189.50,
    "sma_20": 185.30,
    "sma_50": 182.10,
    "rsi": 65.5,
    "macd": 0.1234
  },
  "signals": {
    "buy": 1,
    "sell": 0,
    "confidence": 0.75,
    "reasons": ["Golden Cross (SMA 20 > 50 > 200)", "RSI Oversold"]
  },
  "entry_exit": {
    "entry_price": 189.50,
    "target_price": 198.98,
    "stop_loss": 183.82
  }
}
```

## 🛠️ โครงสร้างไฟล์

```
stock_analyzer/
├── main.py                 # ไฟล์ Main
├── requirements.txt        # Dependencies
├── .env.example           # Configuration template
├── config/
│   └── settings.py        # Settings
├── src/
│   ├── data/
│   │   └── fetcher.py     # Data fetching
│   ├── analysis/
│   │   └── technical.py   # Technical analysis
│   ├── signals/
│   │   └── generator.py   # Signal generation
│   ├── notifications/
│   │   └── notifier.py    # Notifications
│   └── ai/
│       └── models.py      # AI Models
├── tests/
│   └── test_*.py          # Unit tests
└── README.md              # This file
```

## ⚙️ Configuration

### settings.py

สำคัญ Settings:

```python
# Stock list
STOCKS_TO_MONITOR = ['AAPL', 'MSFT', 'GOOGL', ...]

# Technical parameters
TECHNICAL_CONFIG = {
    'sma_short': 20,
    'sma_medium': 50,
    'sma_long': 200,
    'rsi_period': 14,
    'rsi_overbought': 70,
    'rsi_oversold': 30,
}

# Signal settings
SIGNAL_CONFIG = {
    'min_confidence': 0.6,
    'buy_threshold': 0.65,
    'sell_threshold': 0.65,
}

# Trading settings
TRADING_CONFIG = {
    'profit_target_percent': 5,
    'stop_loss_percent': 3,
}
```

## 🔔 การตั้งค่า Notifications

### Email Notification

1. ใช้ Gmail:
   - Enable "2-Step Verification"
   - สร้าง "App Password"
   - ใส่ใน .env:
   ```
   EMAIL_NOTIFICATIONS_ENABLED=True
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   RECIPIENT_EMAIL=recipient@gmail.com
   ```

### Telegram Notification

1. สร้าง Telegram Bot:
   - Chat with @BotFather
   - Get Bot Token
   - Get Chat ID
   - ใส่ใน .env:
   ```
   TELEGRAM_NOTIFICATIONS_ENABLED=True
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

### Webhook Notification

```
WEBHOOK_NOTIFICATIONS_ENABLED=True
WEBHOOK_URL=https://your-service.com/webhook
```

## 📊 Signal Interpretation

### Buy Signal 🟢
- **Golden Cross**: SMA20 > SMA50 > SMA200 (Uptrend)
- **RSI Oversold**: RSI < 30 (ราคาอาจจะเด้งกลับ)
- **MACD Bullish**: MACD crossing above Signal line
- **Price Support**: Price above MA50 and MA200

### Sell Signal 🔴
- **Death Cross**: SMA20 < SMA50 < SMA200 (Downtrend)
- **RSI Overbought**: RSI > 70 (ราคาอาจจะปรับตัว)
- **MACD Bearish**: MACD crossing below Signal line
- **Price Resistance**: Price below MA50 and MA200

### Confidence Score
- **80-100%**: Very Strong Signal
- **60-80%**: Strong Signal
- **40-60%**: Moderate Signal
- **<40%**: Weak Signal

## 📈 Performance Metrics

โปรแกรมจะคำนวณ:
- Win Rate: % ของ signals ที่ถูกต้อง
- Risk/Reward Ratio: Potential profit vs risk
- Sharpe Ratio: Return per unit of risk

## 🔐 ข้อระวัง

⚠️ **สำคัญ**:
- โปรแกรมนี้ใช้สำหรับวิเคราะห์เท่านั้น ไม่ใช่คำแนะนำการลงทุน
- ผลลัพธ์ไม่รับประกัน
- ทำการศึกษาเพิ่มเติมก่อนตัดสินใจลงทุน
- เสี่ยงด้านข้อมูล APIs อาจมีความล่าช้า

## 🚦 Roadmap

- [ ] Sentiment Analysis (News/Social Media)
- [ ] Portfolio Management
- [ ] Backtesting Engine
- [ ] Real-time Trading Bot
- [ ] Mobile App
- [ ] Web Dashboard (Streamlit/Flask)

## 📝 License

MIT License

## 👨‍💻 Contributing

Contributions welcome! Please create a Pull Request.

## 📧 Support

สำหรับคำถามหรือปัญหา กรุณา open an issue.

---

**Happy Trading! 📈** 🚀

