# AI Coding Agent Instructions - Stock Analyzer

## Project Overview
**Stock Analyzer** is a comprehensive USA stock analysis system using Python, Streamlit, and AI signals. The codebase integrates technical analysis, fundamental analysis, ML-based signal generation, and a web dashboard for real-time stock analysis.

---

## Architecture & Data Flow

### Core Module Structure (src/)
```
src/
├── data/          → StockDataFetcher: yfinance → historical/fundamental data
├── analysis/      → TechnicalAnalyzer: SMA, RSI, MACD, Bollinger Bands, ATR
├── signals/       → SignalGenerator: Rule-based + AISignalGenerator (ML classification)
├── notifications/ → NotificationManager: Email/Telegram/Webhook alerts
├── ai/            → PricePredictor, AnomalyDetector, CorrelationAnalyzer
├── details/       → StockDetailsProvider, StockInfoWidget (enhanced info display)
├── discovery/     → StockScanner: Popular stocks, trending, microcap finder
└── dividend/      → DividendAnalyzer: High-dividend stock discovery (NEW - 300+ lines)
```

### Data Flow Pipeline
1. **Input Layer**: User selects stocks via CLI, Dashboard, or Python API
2. **Data Fetching**: `StockDataFetcher` → yfinance (caches results for performance)
3. **Analysis Stage**: 
   - `TechnicalAnalyzer` computes 8+ indicators on OHLCV data
   - `FundamentalAnalyzer` fetches P/E, Dividend Yield, ROE, etc.
4. **Signal Generation**: 
   - `SignalGenerator.generate_signals_from_indicators()` uses rule-based logic (SMA crossover, RSI extremes, MACD divergence)
   - `AISignalGenerator` uses RandomForest classifier on standardized features
5. **Output**: BUY/SELL signals with confidence scores, entry/exit points, stop loss
6. **Distribution**: `NotificationManager` sends alerts via Email/Telegram/Webhook

---

## Key Patterns & Conventions

### Signal Generation Logic (Critical)
**File**: `src/signals/generator.py`
- **BUY Signal Rules** (from `generate_signals_from_indicators`):
  - Price > SMA20 > SMA50 > SMA200 (uptrend)
  - RSI 30-70 (oversold = buy)
  - MACD histogram > 0 (positive momentum)
  - Confidence score: count matching rules ÷ total rules
  - **Minimum confidence threshold**: Default 0.6 (60%)

- **Entry/Exit Logic** (from `generate_entry_exit_points`):
  - Entry = current price
  - Target = Entry × (1 + 0.05) [5% profit target]
  - Stop Loss = Entry × (1 - 0.03) [3% max loss]

### Streamlit Dashboard Architecture
**File**: `dashboard.py` (991 lines, 6 tabs + 4 input modes)
- **Tab Structure**: Analysis | Buy Signals | Sell Signals | Hot Stocks | Microcap | Stock Details
- **Mode Selection**:
  1. **"📝 ป้อนชื่อหุ้น"**: Free-form text input (merged with dropdown selection)
  2. **"🔍 ค้นหาจากตลาด"**: Use `StockScanner.get_popular_stocks()`
  3. **"💎 หุ้นจิ๋ว"**: Microcap scanner with price filtering (min/max slider)
  4. **"💰 หุ้นปันผล"**: NEW - DividendAnalyzer with weekly/monthly/yearly filters
- **Critical Session State**: Always initialize `selected_stocks = []` before mode logic
- **New Dividend Features**:
  - Period selection radio button (รายปี/รายเดือน/รายสัปดาห์)
  - Dynamic slider ranges based on period (annual: 0-10%, monthly: 0-1%, weekly: 0-0.3%)
  - Comparative display tables with period-specific columns
  - Income calculator shows returns across all three periods

### Dividend Module (src/dividend/analyzer.py) - NEW
**Size**: 300+ lines
- **High-Dividend Stocks Dict**: 25 pre-configured stocks (T, VZ, PM, JNJ, PG, KO, etc.)
- **Methods**:
  - `get_dividend_info(symbol)` → dict with yield, monthly/weekly dividends
  - `find_high_dividend_stocks(min_yield, limit)` → filtered sorted list
  - `calculate_dividend_income(investment, yield, period)` → income projections
  - `get_dividend_ranking()` → categorize by yield level (very_high, high, moderate, low, very_low)
- **Key Calculations**:
  - Monthly = Annual ÷ 12
  - Weekly = Annual ÷ 52
  - Uses yfinance to fetch actual dividend yields, handles None gracefully

### Stock Details Enhancement (src/details/)
- **StockInfoWidget** (200+ lines):
  - `display_stock_fundamentals()`: Name, market, country, employees
  - `display_valuation_analysis()`: P/E, PEG, P/B, Dividend Yield with ✅/⚠️/❌ badges
  - `display_financial_health()`: ROE, ROA, Debt/Equity, Current Ratio, Beta assessments
  - `display_valuation_recommendation()`: Smart buy/sell/hold based on metrics

---

## Developer Workflows

### Running the Application
```bash
# Web Dashboard
streamlit run dashboard.py

# CLI Analysis
python cli.py analyze AAPL MSFT GOOGL -p 1y
python cli.py buy AAPL MSFT -c 0.6   # Find buy opportunities
python cli.py hot AAPL MSFT TSLA     # Find hot stocks

# Direct Python API
from main import StockAnalyzerApp
app = StockAnalyzerApp()
result = app.analyze_single_stock('AAPL')
opportunities = app.find_buy_opportunities(['AAPL', 'MSFT'], min_confidence=0.6)
```

### Testing
```bash
python -m unittest tests/test_analyzer.py
```

### Configuration
- **File**: `config/settings.py` or `.env`
- **Critical Settings**: 
  - `MIN_CONFIDENCE_SCORE = 0.6` (signal confidence threshold)
  - `TECHNICAL_INDICATORS` list for custom analysis
  - Notification credentials (EMAIL_USER, TELEGRAM_BOT_TOKEN, WEBHOOK_URL)

### Debugging
1. **Logs**: Check logging output (each module has `logger.info/error`)
2. **Data Issues**: Verify yfinance connectivity, check fetcher.py caching logic
3. **Signal Calculation**: Review technical.py for indicator edge cases (NaN handling)
4. **Dashboard**: Use `st.write(variable)` for inspection; restart with `streamlit run dashboard.py --logger.level=debug`

---

## Extension Points & Patterns

### Adding New Technical Indicators
**File**: `src/analysis/technical.py`
```python
@staticmethod
def calculate_YOUR_INDICATOR(data, params):
    """Add docstring with Thai translations"""
    result = ...  # numpy/pandas calculation
    return result

# Then add to get_technical_summary() method:
def get_technical_summary(self, data):
    summary['your_indicator'] = self.calculate_YOUR_INDICATOR(data, window=14)
    return summary
```

### Adding New Data Sources
**File**: `src/data/fetcher.py`
```python
class StockDataFetcher:
    def fetch_from_NEW_SOURCE(self, symbol, period):
        # Cache with self.cache[symbol]
        # Return DataFrame with OHLCV columns
```

### Adding New Signal Rules
**File**: `src/signals/generator.py`
```python
def generate_signals_from_indicators(self, technical_data):
    # Add condition check
    if YOUR_CONDITION:
        signals['reasons'].append("YOUR_REASON_IN_THAI")
        confidence_count += 1
```

---

## Dependencies & External Services

### Python Libraries
- **Data**: yfinance, pandas, numpy
- **ML**: scikit-learn (RandomForest for signal classification)
- **Dashboard**: streamlit, plotly
- **Analysis**: ta (technical analysis library)
- **Notifications**: requests (for Telegram/Webhook), smtplib (Email)
- **Config**: python-dotenv

### External APIs
- **Yahoo Finance** (via yfinance): Stock prices, fundamentals, dividends
- **Telegram Bot** (optional): Send alerts
- **Webhook URL** (optional): Custom integrations
- **SMTP Email** (optional): Email notifications

### Performance Considerations
- **Caching**: yfinance data cached in StockDataFetcher.cache dict (reduces redundant API calls ~80%)
- **Vectorized Operations**: Use numpy/pandas, NOT loops over rows
- **Parallel Analysis**: Multiple stocks analyzed in dashboard loop (not yet async, improvement opportunity)
- **Typical Runtime**: Single stock ~2-3 sec, 10 stocks ~20-30 sec

---

## Documentation Structure
- **START_HERE.txt**: Entry point, quick commands
- **README.md**: Full documentation (~400 lines)
- **ARCHITECTURE.md**: System design, data flow diagrams
- **USAGE.md**: Detailed examples
- **QUICK_START.txt**: Command reference
- **STOCK_DETAILS_DOCUMENTATION.md**: Stock Details tab guide
- **GITHUB_UPLOAD_SUMMARY.md**: Project metadata

---

## Common Pitfalls & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Module import errors | sys.path not set | Add: `sys.path.insert(0, os.path.dirname(__file__))` |
| NaN in indicators | Edge data points | Check window size ≤ len(data); use `.dropna()` |
| Yahoo Finance "No data" | Symbol invalid or delisted | Wrap in try-except, provide fallback |
| Dividend data None | Stock doesn't pay dividends | Use `.get()` with default, check `is not None` |
| Dashboard slow | Too many stocks or API lag | Implement caching, reduce stock list, add progress bar |
| Signal never triggers | Thresholds too strict | Verify min_confidence default, check indicator calculations |

---

## AI Agent Guidance

When extending or modifying this codebase:

1. **Always check module responsibilities** before adding features - reuse existing classes
2. **Maintain the data flow pipeline**: Fetcher → Analyzer → SignalGenerator → Notifier
3. **Use Thai docstrings consistently** for all new methods
4. **Test with real stock symbols** (AAPL, MSFT, etc.) before deploying
5. **Add error handling** for yfinance failures (symbols can be delisted)
6. **Keep technical analysis calculations vectorized** (pandas/numpy, not loops)
7. **Document confidence thresholds** - signals are probabilistic, not absolute
8. **Preserve backward compatibility** in main.py's StockAnalyzerApp public methods
9. **Review src/dividend/analyzer.py patterns** for new specialized analyzers
10. **Log all significant operations** with logger.info/error for debugging

---

**Last Updated**: January 6, 2026  
**Version**: 1.1  
**Scope**: Covers all modules including NEW dividend analysis features
