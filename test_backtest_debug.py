"""
ทดสอบ Debug Backtest
"""
from src.backtesting.backtester import Backtester
from main import StockAnalyzerApp
import logging

# เพิ่ม logging level
logging.basicConfig(level=logging.DEBUG)

# สร้าง app และ backtester
app = StockAnalyzerApp()
bt = Backtester(initial_capital=10000, commission=0.001, slippage=0.0005)

# รัน backtest สำหรับ NVDA 3 เดือน (ควรมีสัญญาณมากกว่า)
print("Testing Backtest with NVDA (Oct-Dec 2024)...")
result = bt.run_backtest(app, ['NVDA'], '2024-10-01', '2024-12-31', min_confidence=0.5)

# แสดงผลลัพธ์
print(f"\n{'='*60}")
print(f"BACKTEST RESULTS")
print(f"{'='*60}")
print(f"Total Trades: {len(bt.trades)}")
print(f"Final Capital: ${bt.capital:,.2f}")
print(f"Total Return: {result.get('total_return', 0):.2f}%")

# แสดงรายละเอียด trades ทั้งหมด
if bt.trades:
    print(f"\nTRADE HISTORY:")
    for i, trade in enumerate(bt.trades, 1):
        profit_str = f"P/L: ${trade.profit_loss:+.2f} ({trade.profit_loss_pct:+.2f}%)" if trade.action == 'SELL' else ""
        print(f"{i}. {trade.action:4s} {trade.quantity:3d} {trade.symbol} @ ${trade.price:7.2f} on {trade.date.date()} {profit_str}")
        if trade.reason:
            print(f"      Reason: {trade.reason[:80]}")
else:
    print("\nNO TRADES GENERATED!")
    print("Possible reasons:")
    print("- Confidence threshold too high (try lowering min_confidence)")
    print("- No buy signals detected in the period")
    print("- Technical indicators not generating signals")
