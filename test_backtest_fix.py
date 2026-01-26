"""
ทดสอบ Backtesting ที่แก้ไขแล้ว
"""
from src.backtesting.backtester import Backtester
from main import StockAnalyzerApp

# สร้าง app และ backtester
app = StockAnalyzerApp()
bt = Backtester(initial_capital=10000, commission=0.001, slippage=0.0005)

# รัน backtest สำหรับ AAPL ในเดือน มกราคม 2024
print("🔬 Testing Backtest with AAPL (Jan 2024)...")
result = bt.run_backtest(app, ['AAPL'], '2024-01-01', '2024-01-31')

# แสดงผลลัพธ์
print(f"\n{'='*60}")
print(f"📊 BACKTEST RESULTS")
print(f"{'='*60}")
print(f"Total Trades: {len(bt.trades)}")
print(f"Final Capital: ${bt.capital:,.2f}")
print(f"Total Return: {result.get('total_return', 0):.2f}%")
print(f"Win Rate: {result.get('win_rate', 0):.1f}%")
print(f"Profit Factor: {result.get('profit_factor', 0):.2f}")
print(f"Max Drawdown: {result.get('max_drawdown', 0):.2f}%")

# แสดง trades
if bt.trades:
    print(f"\n📝 TRADE HISTORY:")
    for i, trade in enumerate(bt.trades, 1):
        profit_symbol = "💰" if trade.profit_loss > 0 else "📉"
        print(f"{i}. {trade.action} {trade.symbol} @ ${trade.price:.2f} on {trade.date.date()} - {profit_symbol} ${trade.profit_loss:.2f}")
