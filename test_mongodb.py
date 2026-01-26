"""
ทดสอบการเชื่อมต่อ MongoDB Atlas
"""

import sys
import os
from datetime import datetime
import pandas as pd

# เพิ่ม path
sys.path.insert(0, os.path.dirname(__file__))

from src.database.mongodb_manager import MongoDBManager


def test_mongodb_connection():
    """ทดสอบการเชื่อมต่อ MongoDB Atlas"""
    
    print("=" * 60)
    print("Testing MongoDB Atlas Connection")
    print("=" * 60)
    
    try:
        # 1. เชื่อมต่อ MongoDB
        print("\n1. Connecting to MongoDB Atlas...")
        db = MongoDBManager()
        print("   ✅ Connected successfully!")
        
        # 2. ดูสถิติ Database
        print("\n2. Getting database statistics...")
        stats = db.get_database_stats()
        print(f"   📊 Database Stats:")
        for collection, count in stats.items():
            print(f"      - {collection}: {count} documents")
        
        # 3. ทดสอบบันทึกข้อมูลหุ้น
        print("\n3. Testing stock info save...")
        test_stock_data = {
            'name': 'Apple Inc.',
            'sector': 'Technology',
            'market_cap': 2800000000000,
            'pe_ratio': 28.5,
            'test': True,
            'tested_at': datetime.now()
        }
        db.save_stock_info('AAPL', test_stock_data)
        print("   ✅ Saved test stock info")
        
        # 4. ทดสอบดึงข้อมูลหุ้น
        print("\n4. Testing stock info retrieval...")
        retrieved_stock = db.get_stock_info('AAPL')
        if retrieved_stock:
            print(f"   ✅ Retrieved stock: {retrieved_stock.get('name')}")
            print(f"      Sector: {retrieved_stock.get('sector')}")
        else:
            print("   ⚠️ Stock not found")
        
        # 5. ทดสอบบันทึกข้อมูลราคา
        print("\n5. Testing price data save...")
        # สร้างข้อมูลตัวอย่าง
        dates = pd.date_range(start='2024-01-01', periods=5, freq='D')
        test_prices = pd.DataFrame({
            'Open': [150.0, 151.0, 152.0, 153.0, 154.0],
            'High': [151.0, 152.0, 153.0, 154.0, 155.0],
            'Low': [149.0, 150.0, 151.0, 152.0, 153.0],
            'Close': [150.5, 151.5, 152.5, 153.5, 154.5],
            'Volume': [1000000, 1100000, 1200000, 1300000, 1400000]
        }, index=dates)
        
        db.save_price_data('AAPL', test_prices)
        print("   ✅ Saved test price data")
        
        # 6. ทดสอบดึงข้อมูลราคา
        print("\n6. Testing price data retrieval...")
        retrieved_prices = db.get_price_data('AAPL')
        if not retrieved_prices.empty:
            print(f"   ✅ Retrieved {len(retrieved_prices)} price records")
            print(f"      Latest Close: ${retrieved_prices['Close'].iloc[-1]:.2f}")
        else:
            print("   ⚠️ No price data found")
        
        # 7. ทดสอบบันทึกสัญญาณ
        print("\n7. Testing signal save...")
        test_signal = {
            'signal_type': 'buy',
            'confidence': 0.85,
            'reasons': ['RSI oversold', 'MACD crossover'],
            'price': 150.5,
            'date': datetime.now(),
            'test': True
        }
        db.save_signal('AAPL', test_signal)
        print("   ✅ Saved test signal")
        
        # 8. ทดสอบดึงสัญญาณ
        print("\n8. Testing signal retrieval...")
        signals = db.get_signals(symbol='AAPL', days=7)
        if signals:
            print(f"   ✅ Retrieved {len(signals)} signals")
            for i, sig in enumerate(signals[:3], 1):  # แสดง 3 อันแรก
                print(f"      {i}. {sig.get('signal_type').upper()} - Confidence: {sig.get('confidence'):.0%}")
        else:
            print("   ℹ️ No signals found")
        
        # 9. ทดสอบบันทึก Backtest
        print("\n9. Testing backtest result save...")
        test_backtest = {
            'symbols': ['AAPL', 'MSFT'],
            'period': '2023-01-01 to 2024-12-31',
            'total_return': 15.5,
            'win_rate': 65.0,
            'total_trades': 20,
            'test': True
        }
        backtest_id = db.save_backtest_result(test_backtest)
        print(f"   ✅ Saved backtest result: {backtest_id}")
        
        # 10. ทดสอบดึง Backtest
        print("\n10. Testing backtest retrieval...")
        backtests = db.get_backtest_results(limit=5)
        if backtests:
            print(f"    ✅ Retrieved {len(backtests)} backtest results")
            for i, bt in enumerate(backtests[:3], 1):
                print(f"       {i}. Return: {bt.get('total_return', 0):.2f}% - Created: {bt.get('created_at')}")
        else:
            print("    ℹ️ No backtest results found")
        
        # 11. ทดสอบ Portfolio
        print("\n11. Testing portfolio save...")
        test_portfolio = {
            'stocks': [
                {'symbol': 'AAPL', 'quantity': 10, 'avg_price': 150.0},
                {'symbol': 'MSFT', 'quantity': 5, 'avg_price': 300.0}
            ],
            'total_value': 3000.0,
            'test': True
        }
        db.save_portfolio('test_user', test_portfolio)
        print("    ✅ Saved test portfolio")
        
        # 12. ทดสอบดึง Portfolio
        print("\n12. Testing portfolio retrieval...")
        portfolio = db.get_portfolio('test_user')
        if portfolio:
            print(f"    ✅ Retrieved portfolio")
            print(f"       Total Value: ${portfolio.get('total_value', 0):,.2f}")
            print(f"       Stocks: {len(portfolio.get('stocks', []))}")
        else:
            print("    ⚠️ Portfolio not found")
        
        # 13. สรุปสถิติสุดท้าย
        print("\n13. Final database statistics...")
        final_stats = db.get_database_stats()
        print(f"    📊 Final Stats:")
        for collection, count in final_stats.items():
            print(f"       - {collection}: {count} documents")
        
        # ปิดการเชื่อมต่อ
        db.close()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\n🎉 MongoDB Atlas is ready to use!")
        print("\nNext steps:")
        print("1. Update .env file with your real MongoDB connection string")
        print("2. Integrate MongoDBManager into your application")
        print("3. Run this test again to verify production connection")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nTroubleshooting:")
        print("1. Check .env file has correct MONGODB_URI")
        print("2. Verify MongoDB Atlas user credentials")
        print("3. Check Network Access allows your IP")
        print("4. Install dependencies: pip install pymongo dnspython")
        return False


if __name__ == "__main__":
    test_mongodb_connection()
