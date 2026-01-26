# 🗄️ MongoDB Atlas Integration Guide

## 📚 คู่มือการใช้งาน MongoDB Atlas สำหรับ Stock Analyzer

---

## 🚀 Quick Start (5 นาที)

### 1. ติดตั้ง Dependencies
```bash
pip install pymongo dnspython python-dotenv
```

### 2. ตั้งค่า MongoDB Atlas
1. ไปที่ https://www.mongodb.com/cloud/atlas/register
2. สมัครบัญชีฟรี
3. สร้าง Cluster (M0 Free Tier)
4. สร้าง Database User (username/password)
5. ตั้งค่า Network Access (Allow 0.0.0.0/0)
6. คัดลอก Connection String

### 3. สร้างไฟล์ .env
```bash
# คัดลอกจาก .env.example
cp .env.example .env

# แก้ไข .env และใส่ connection string
MONGODB_URI=mongodb+srv://stock_user:YOUR_PASSWORD@stock-analyzer-cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority
```

### 4. ทดสอบการเชื่อมต่อ
```bash
python test_mongodb.py
```

---

## 📖 การใช้งาน MongoDBManager

### Basic Usage

```python
from src.database.mongodb_manager import MongoDBManager

# เชื่อมต่อ MongoDB
db = MongoDBManager()

# หรือระบุ connection string เอง
db = MongoDBManager(connection_string="mongodb+srv://...")
```

---

## 🔧 API Reference

### 1. Stock Data Operations

#### บันทึกข้อมูลหุ้น
```python
stock_data = {
    'name': 'Apple Inc.',
    'sector': 'Technology',
    'market_cap': 2800000000000,
    'pe_ratio': 28.5,
    'dividend_yield': 0.5
}
db.save_stock_info('AAPL', stock_data)
```

#### ดึงข้อมูลหุ้น
```python
stock = db.get_stock_info('AAPL')
print(stock['name'])  # Apple Inc.
```

---

### 2. Price Data Operations (Time Series)

#### บันทึกข้อมูลราคา
```python
import pandas as pd

# DataFrame จาก yfinance หรือ CSV
prices_df = yf.download('AAPL', period='1mo')
db.save_price_data('AAPL', prices_df)
```

#### ดึงข้อมูลราคา
```python
from datetime import datetime, timedelta

# ดึงข้อมูล 30 วันล่าสุด
start_date = datetime.now() - timedelta(days=30)
prices = db.get_price_data('AAPL', start_date=start_date)

print(prices.head())
#              Open    High     Low   Close    Volume
# 2024-01-01  150.0   151.0   149.0  150.5   1000000
```

---

### 3. Signal Operations

#### บันทึกสัญญาณซื้อขาย
```python
from datetime import datetime

signal_data = {
    'signal_type': 'buy',  # 'buy' หรือ 'sell'
    'confidence': 0.85,
    'reasons': ['RSI oversold', 'MACD crossover'],
    'price': 150.5,
    'date': datetime.now(),
    'entry_price': 150.5,
    'target_price': 157.5,
    'stop_loss': 147.0
}

db.save_signal('AAPL', signal_data)
```

#### ดึงสัญญาณ
```python
# ดึงสัญญาณทั้งหมด 7 วันล่าสุด
signals = db.get_signals(days=7)

# ดึงเฉพาะหุ้น AAPL
signals = db.get_signals(symbol='AAPL', days=30)

# ดึงเฉพาะสัญญาณซื้อ
buy_signals = db.get_signals(signal_type='buy', days=7)

# แสดงผล
for signal in signals:
    print(f"{signal['symbol']} - {signal['signal_type'].upper()} @ ${signal['price']} - {signal['confidence']:.0%}")
```

---

### 4. Backtesting Operations

#### บันทึกผลลัพธ์ Backtest
```python
backtest_data = {
    'symbols': ['AAPL', 'MSFT', 'GOOGL'],
    'period': '2023-01-01 to 2024-12-31',
    'initial_capital': 10000,
    'final_capital': 11500,
    'total_return': 15.0,
    'win_rate': 65.0,
    'total_trades': 25,
    'winning_trades': 16,
    'losing_trades': 9,
    'sharpe_ratio': 1.25,
    'max_drawdown': -8.5,
    'trades': [
        {'symbol': 'AAPL', 'action': 'BUY', 'price': 150.0, 'date': '2023-01-15'},
        # ... more trades
    ]
}

backtest_id = db.save_backtest_result(backtest_data)
print(f"Saved backtest: {backtest_id}")
```

#### ดึงผลลัพธ์ Backtest
```python
# ดึง 10 ผลลัพธ์ล่าสุด
backtests = db.get_backtest_results(limit=10)

for bt in backtests:
    print(f"Return: {bt['total_return']:.2f}% - Win Rate: {bt['win_rate']:.1f}%")
```

---

### 5. Portfolio Operations

#### บันทึก Portfolio
```python
portfolio_data = {
    'stocks': [
        {'symbol': 'AAPL', 'quantity': 10, 'avg_price': 150.0, 'current_price': 155.0},
        {'symbol': 'MSFT', 'quantity': 5, 'avg_price': 300.0, 'current_price': 310.0}
    ],
    'total_value': 3100.0,
    'total_cost': 3000.0,
    'profit_loss': 100.0,
    'profit_loss_pct': 3.33
}

db.save_portfolio('user123', portfolio_data)
```

#### ดึง Portfolio
```python
portfolio = db.get_portfolio('user123')

if portfolio:
    print(f"Total Value: ${portfolio['total_value']:,.2f}")
    print(f"P/L: ${portfolio['profit_loss']:+,.2f} ({portfolio['profit_loss_pct']:+.2f}%)")
    
    for stock in portfolio['stocks']:
        print(f"  {stock['symbol']}: {stock['quantity']} shares @ ${stock['avg_price']:.2f}")
```

---

### 6. Utility Functions

#### ดูสถิติ Database
```python
stats = db.get_database_stats()

print("Database Statistics:")
for collection, count in stats.items():
    print(f"  {collection}: {count} documents")

# Output:
# stocks: 150
# prices: 25000
# signals: 1200
# backtests: 50
# portfolio: 1
```

#### ปิดการเชื่อมต่อ
```python
db.close()
```

---

## 🏗️ Database Schema

### Collections

#### 1. `stocks` Collection
```javascript
{
  "_id": ObjectId("..."),
  "symbol": "AAPL",
  "name": "Apple Inc.",
  "sector": "Technology",
  "market_cap": 2800000000000,
  "pe_ratio": 28.5,
  "dividend_yield": 0.5,
  "updated_at": ISODate("2024-01-26T10:30:00Z")
}
```

#### 2. `prices` Collection (Time Series)
```javascript
{
  "_id": ObjectId("..."),
  "symbol": "AAPL",
  "date": ISODate("2024-01-26T00:00:00Z"),
  "open": 150.0,
  "high": 151.0,
  "low": 149.0,
  "close": 150.5,
  "volume": 1000000,
  "updated_at": ISODate("2024-01-26T10:30:00Z")
}
```

#### 3. `signals` Collection
```javascript
{
  "_id": ObjectId("..."),
  "symbol": "AAPL",
  "signal_type": "buy",  // "buy" or "sell"
  "confidence": 0.85,
  "reasons": ["RSI oversold", "MACD crossover"],
  "price": 150.5,
  "date": ISODate("2024-01-26T10:30:00Z"),
  "entry_price": 150.5,
  "target_price": 157.5,
  "stop_loss": 147.0,
  "created_at": ISODate("2024-01-26T10:30:00Z")
}
```

#### 4. `backtests` Collection
```javascript
{
  "_id": ObjectId("..."),
  "symbols": ["AAPL", "MSFT"],
  "period": "2023-01-01 to 2024-12-31",
  "initial_capital": 10000,
  "final_capital": 11500,
  "total_return": 15.0,
  "win_rate": 65.0,
  "total_trades": 25,
  "sharpe_ratio": 1.25,
  "max_drawdown": -8.5,
  "trades": [...],
  "created_at": ISODate("2024-01-26T10:30:00Z")
}
```

#### 5. `portfolio` Collection
```javascript
{
  "_id": ObjectId("..."),
  "user_id": "user123",
  "stocks": [
    {"symbol": "AAPL", "quantity": 10, "avg_price": 150.0}
  ],
  "total_value": 3100.0,
  "updated_at": ISODate("2024-01-26T10:30:00Z")
}
```

---

## 🔍 Indexes

MongoDBManager สร้าง indexes อัตโนมัติ:

- `stocks`: `symbol` (unique)
- `prices`: `(symbol, date)`
- `signals`: `(symbol, date, signal_type)`
- `backtests`: `created_at`

---

## ⚡ Performance Tips

### 1. Bulk Operations
```python
# ❌ Slow - Insert ทีละ record
for date, row in df.iterrows():
    db.prices_collection.insert_one({...})

# ✅ Fast - Bulk insert
db.save_price_data('AAPL', df)  # ใช้ insert_many
```

### 2. Query Optimization
```python
# ❌ ดึงข้อมูลทั้งหมดแล้ว filter ใน Python
all_signals = db.get_signals(days=365)
aapl_signals = [s for s in all_signals if s['symbol'] == 'AAPL']

# ✅ Filter ที่ Database
aapl_signals = db.get_signals(symbol='AAPL', days=365)
```

### 3. Caching
```python
# Cache ข้อมูลที่ไม่เปลี่ยนบ่อย
stock_info_cache = {}

def get_cached_stock_info(symbol):
    if symbol not in stock_info_cache:
        stock_info_cache[symbol] = db.get_stock_info(symbol)
    return stock_info_cache[symbol]
```

---

## 🔒 Security Best Practices

### 1. Environment Variables
```python
# ❌ ไม่ควร hardcode
db = MongoDBManager("mongodb+srv://user:pass123@...")

# ✅ ใช้ environment variables
db = MongoDBManager()  # อ่านจาก .env
```

### 2. Credential Management
```bash
# .env file (ห้าม commit ใน Git!)
MONGODB_URI=mongodb+srv://...

# .gitignore
.env
*.env
```

### 3. Network Access
- ใช้ IP Whitelist แทน 0.0.0.0/0 (ถ้าทำได้)
- ใช้ VPN หรือ Private Peering สำหรับ production

---

## 🐛 Troubleshooting

### ปัญหา: "ServerSelectionTimeoutError"
```
สาเหตุ: ไม่สามารถเชื่อมต่อ MongoDB Atlas
แก้ไข:
1. ตรวจสอบ connection string ใน .env
2. ตรวจสอบ Network Access อนุญาต IP ของคุณ
3. ตรวจสอบ username/password ถูกต้อง
4. ติดตั้ง dnspython: pip install dnspython
```

### ปัญหา: "Authentication failed"
```
สาเหตุ: Username/Password ผิด
แก้ไข:
1. ตรวจสอบ Database User ใน MongoDB Atlas
2. Reset password ถ้าจำเป็น
3. อัพเดท connection string ใน .env
```

### ปัญหา: "DuplicateKeyError"
```
สาเหตุ: พยายาม insert ข้อมูล symbol ซ้ำ
แก้ไข:
- ใช้ save_stock_info() แทน insert_one() (มี upsert=True)
```

---

## 📊 Monitoring

### ดูการใช้งาน Database
1. ไปที่ MongoDB Atlas Dashboard
2. เลือก Cluster
3. ดู Metrics → Connections, Operations, Data Size

### Alerts
- ตั้งค่า Alerts สำหรับ:
  - Storage > 80%
  - Connections > 90%
  - Slow queries

---

## 🚀 Next Steps

1. **Integration**: รวม MongoDBManager เข้ากับ StockAnalyzerApp
2. **Caching**: เพิ่ม caching layer ด้วย Redis
3. **Backup**: ตั้งค่า automated backups
4. **Monitoring**: ใช้ MongoDB Charts สำหรับ visualization
5. **Scaling**: อัพเกรด cluster เมื่อข้อมูลเยอะขึ้น

---

## 📚 Resources

- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [PyMongo Documentation](https://pymongo.readthedocs.io/)
- [MongoDB Best Practices](https://www.mongodb.com/docs/manual/administration/production-notes/)

---

**Created**: January 26, 2026  
**Version**: 1.0  
**Author**: Stock Analyzer Team
