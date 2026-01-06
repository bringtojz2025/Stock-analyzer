# 📊 Stock Details Tab Documentation

## Overview

The new "📊 Stock Details" tab provides comprehensive information about individual stocks, including historical price charts, financial metrics, and business classification.

---

## 🎯 How to Use

### 1. Accessing the Stock Details Tab

1. Open Dashboard at `http://localhost:8504`
2. Click on the **"📊 Stock Details"** tab (Tab 6)
3. Select a stock from the dropdown **"Select Stock to View Details"**

### 2. Information Displayed

#### 📋 Basic Information
- **Company Name**: Full legal name
- **Symbol**: Ticker symbol (e.g., AAPL)
- **Market**: Stock exchange (NASDAQ, NYSE, etc.)
- **Country**: Company headquarters location
- **Website**: Official company website
- **Founded**: Year company was established

#### 🏢 Business Classification
- **Sector**: e.g., "Technology", "Finance", "Healthcare"
- **Industry**: e.g., "Electronics Manufacturer", "Software", "Financial Services"
- **Market Category**: Based on total market cap
  - 💎 **Micro-cap**: < $300M
  - 🔹 **Small-cap**: < $2B
  - 🔷 **Mid-cap**: < $10B
  - 🟦 **Large-cap**: < $100B
  - 🟩 **Mega-cap**: > $100B
- **Market Cap**: Total value of all shares (B = Billion, M = Million)

#### 📝 Business Description
- **Business Summary**: What the company does, products/services offered

#### 💰 Price & Performance
- **Current Price**: Latest stock price (Real-time)
- **Previous Close**: Previous trading day's closing price
- **1-Year Change**: Percentage price change over 1 year
- **Average Volume**: Daily trading volume

#### 📈 52-Week Range
- **52-Week High**: Highest price in past 52 weeks
- **52-Week Low**: Lowest price in past 52 weeks

#### 💹 Valuation Metrics
- **P/E Ratio**: Price-to-Earnings ratio
  - Lower = Potentially undervalued, Higher = More expensive
  
- **Forward P/E**: Forward Price-to-Earnings
  - Based on forecasted earnings
  
- **P/B Ratio**: Price-to-Book ratio
  - Compares market value to book value
  
- **P/S Ratio**: Price-to-Sales ratio
  - Good for unprofitable companies
  
- **PEG Ratio**: Price/Earnings-to-Growth
  - Compares P/E to growth rate
  
- **Dividend Yield**: Annual dividend as % of price
  - Higher = Better income, but verify sustainability

#### 📊 Financial Health
- **ROE**: Return on Equity
  - Higher = Better use of shareholder capital
  
- **ROA**: Return on Assets
  - Higher = Better asset efficiency
  
- **Debt-to-Equity**: Leverage ratio
  - Lower = Less financial risk
  
- **Current Ratio**: Short-term liquidity
  - > 1.0 = Can pay short-term debts
  
- **Profit Margin**: Net profitability
  - Higher = More efficient operations
  
- **Beta**: Volatility vs. market
  - > 1 = More volatile (higher risk)
  - < 1 = Less volatile (lower risk)

---

## 📈 Charts and Visualizations

### 1. Candlestick Chart
- Shows daily Open, High, Low, Close prices
- **Green candles**: Day close > open (bullish)
- **Red candles**: Day close < open (bearish)
- **Period**: 1 year

### 2. Volume Chart
- Shows daily trading volume
- **High volume**: Strong investor interest
- **Low volume**: Weak investor interest

### 3. Moving Averages Chart
- **SMA20 (Cyan)**: 20-day simple moving average
  - Tracks short-term trend
  
- **SMA50 (Yellow)**: 50-day simple moving average
  - Tracks medium-term trend
  
- **SMA200 (Red)**: 200-day simple moving average
  - Tracks long-term trend

---

## 💡 How to Read the Data

### Example: Analyzing AAPL

```
Company Name: Apple Inc.
Market: NASDAQ
Country: United States

Sector: Technology
Industry: Electronics Manufacturer
Category: 🟩 Mega-cap > $100B

Current Price: $267.26
1-Year Change: +32.5%

P/E Ratio: 28.5
ROE: 145% (Excellent)
Dividend Yield: 0.45%
```

### Interpretation:
- **NASDAQ**: High-quality tech stock
- **Mega-cap**: Established, stable company
- **+32.5% (1yr)**: Strong price appreciation
- **P/E 28.5**: Relatively expensive vs. earnings
- **ROE 145%**: Excellent shareholder returns

---

## 🔍 Using Data for Investment Decisions

### 📌 Key Indicators to Check

1. **Before Investing in a New Stock**:
   - Market & Industry: What business?
   - Market Cap: Company size
   - 52-week range: Normal price range?

2. **Value Assessment**:
   - P/E Ratio: Expensive or cheap?
   - Dividend Yield: Dividend income?
   - PEG Ratio: Is price justified by growth?

3. **Financial Health**:
   - ROE, ROA: Efficient operations?
   - Debt-to-Equity: Excessive debt?
   - Current Ratio: Can pay debts?

4. **Price Movement**:
   - Candlestick chart: Support/resistance levels
   - Moving averages: Price trend
   - Volume: Investor sentiment

---

## ⚠️ Important Notes

1. **Data Source**: Information from Yahoo Finance may be delayed or incomplete
2. **Not Investment Advice**: For educational purposes only
3. **Cross-Reference**: Always verify with other sources
4. **Multi-Factor Analysis**: Never rely on a single metric

---

## 📞 Support

If you encounter issues:
1. Check internet connection
2. Refresh Dashboard page
3. Try another stock to test

---

**Documentation Released**: January 2026
**Version**: 1.0
