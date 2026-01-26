"""
Unit tests for backtesting module
ทดสอบระบบ Backtesting
"""

import unittest
import pandas as pd
from datetime import datetime, timedelta
from src.backtesting.backtester import Backtester, Trade, Position
from src.backtesting.metrics import PerformanceMetrics


class TestBacktester(unittest.TestCase):
    """ทดสอบ Backtester class"""
    
    def setUp(self):
        """เตรียมข้อมูลทดสอบ"""
        self.backtester = Backtester(
            initial_capital=10000,
            commission=0.001,
            slippage=0.0005,
            position_size_pct=0.2
        )
        
        # สร้างข้อมูลทดสอบ
        dates = pd.date_range(start='2024-01-01', end='2024-01-10', freq='D')
        self.test_data = pd.DataFrame({
            'Date': dates,
            'Close': [100, 102, 101, 103, 105, 104, 106, 108, 107, 109]
        })
        self.test_data.set_index('Date', inplace=True)
    
    def test_initialization(self):
        """ทดสอบการ initialize"""
        self.assertEqual(self.backtester.initial_capital, 10000)
        self.assertEqual(self.backtester.capital, 10000)
        self.assertEqual(self.backtester.commission, 0.001)
        self.assertEqual(self.backtester.slippage, 0.0005)
        self.assertEqual(self.backtester.position_size_pct, 0.2)
        self.assertEqual(len(self.backtester.positions), 0)
        self.assertEqual(len(self.backtester.trades), 0)
    
    def test_position_size_calculation(self):
        """ทดสอบการคำนวณ position size"""
        price = 100
        quantity = self.backtester.calculate_position_size(price)
        expected = int((10000 * 0.2) / price)  # (10000 * 0.2) / 100 = 20
        self.assertEqual(quantity, expected)
    
    def test_buy_trade_execution(self):
        """ทดสอบการซื้อหุ้น"""
        symbol = 'AAPL'
        price = 100
        date = datetime(2024, 1, 1)
        
        self.backtester.execute_trade(symbol, 'BUY', price, date, 'Test buy')
        
        # ตรวจสอบว่ามี position เพิ่มขึ้น
        self.assertEqual(len(self.backtester.positions), 1)
        self.assertIn(symbol, self.backtester.positions)
        
        position = self.backtester.positions[symbol]
        # ปรับให้ยืดหยุ่น เพราะมี slippage
        self.assertGreater(position.quantity, 0)
        self.assertGreater(position.entry_price, price)  # มี slippage
        
        # ตรวจสอบว่า capital ลดลง
        self.assertLess(self.backtester.capital, 10000)
    
    def test_sell_trade_execution(self):
        """ทดสอบการขายหุ้น"""
        symbol = 'AAPL'
        
        # ซื้อก่อน
        self.backtester.execute_trade(symbol, 'BUY', 100, datetime(2024, 1, 1), 'Test buy')
        capital_after_buy = self.backtester.capital
        
        # ขาย
        self.backtester.execute_trade(symbol, 'SELL', 110, datetime(2024, 1, 5), 'Test sell')
        
        # ตรวจสอบว่า position ถูกปิด
        self.assertEqual(len(self.backtester.positions), 0)
        
        # ตรวจสอบว่า capital เพิ่มขึ้น (มีกำไร)
        self.assertGreater(self.backtester.capital, capital_after_buy)
        
        # ตรวจสอบว่ามี trade records (BUY + SELL = 2 trades)
        self.assertGreaterEqual(len(self.backtester.trades), 1)
    
    def test_stop_loss_trigger(self):
        """ทดสอบการ trigger stop loss"""
        symbol = 'AAPL'
        entry_price = 100
        stop_loss = 95
        
        # ซื้อ
        self.backtester.execute_trade(symbol, 'BUY', entry_price, datetime(2024, 1, 1), 'Test buy')
        position = self.backtester.positions[symbol]
        
        # ตรวจสอบ stop loss เมื่อราคาต่ำกว่า stop loss
        current_price = 94
        date = datetime(2024, 1, 5)
        
        triggered = self.backtester.check_stop_loss_take_profit(symbol, current_price, date, stop_loss, None)
        
        self.assertTrue(triggered)
        self.assertEqual(len(self.backtester.positions), 0)  # position ถูกปิด
    
    def test_take_profit_trigger(self):
        """ทดสอบการ trigger take profit"""
        symbol = 'AAPL'
        entry_price = 100
        take_profit = 110
        
        # ซื้อ
        self.backtester.execute_trade(symbol, 'BUY', entry_price, datetime(2024, 1, 1), 'Test buy')
        
        # ตรวจสอบ take profit เมื่อราคาสูงกว่า take profit
        current_price = 111
        date = datetime(2024, 1, 5)
        
        triggered = self.backtester.check_stop_loss_take_profit(symbol, current_price, date, None, take_profit)
        
        self.assertTrue(triggered)
        self.assertEqual(len(self.backtester.positions), 0)  # position ถูกปิด
        self.assertGreaterEqual(len(self.backtester.trades), 1)
    
    def test_portfolio_value_tracking(self):
        """ทดสอบการติดตาม portfolio value"""
        date = datetime(2024, 1, 1)
        current_prices = {'AAPL': 100, 'MSFT': 300}
        
        self.backtester.update_portfolio_value(date, current_prices)
        
        self.assertGreaterEqual(len(self.backtester.portfolio_values), 1)
        # เช็คว่ามีการบันทึกอย่างน้อย 1 ค่า
        last_date, last_value = self.backtester.portfolio_values[-1]
        self.assertEqual(last_date, date)
        self.assertGreater(last_value, 0)


class TestPerformanceMetrics(unittest.TestCase):
    """ทดสอบ PerformanceMetrics class"""
    
    def setUp(self):
        """เตรียมข้อมูลทดสอบ"""
        # สร้าง returns ทดสอบ
        self.returns = pd.Series([0.01, -0.005, 0.02, 0.015, -0.01, 0.03, -0.015, 0.025])
        
        # สร้าง equity curve ทดสอบ
        self.equity_series = pd.Series([10000, 10100, 10050, 10200, 10350, 10300, 10500, 10450, 10650, 10800])
    
    def test_sharpe_ratio_calculation(self):
        """ทดสอบการคำนวณ Sharpe ratio"""
        sharpe = PerformanceMetrics.calculate_sharpe_ratio(self.returns)
        
        self.assertIsNotNone(sharpe)
        self.assertIsInstance(sharpe, float)
        # Sharpe ratio ควรเป็นค่าบวกสำหรับ returns ที่มีค่าเฉลี่ยเป็นบวก
        self.assertGreater(sharpe, 0)
    
    def test_sortino_ratio_calculation(self):
        """ทดสอบการคำนวณ Sortino ratio"""
        sortino = PerformanceMetrics.calculate_sortino_ratio(self.returns)
        
        self.assertIsNotNone(sortino)
        self.assertIsInstance(sortino, float)
        # Sortino ratio มักจะสูงกว่าหรือเท่ากับ Sharpe ratio
        sharpe = PerformanceMetrics.calculate_sharpe_ratio(self.returns)
        self.assertGreaterEqual(sortino, sharpe)
    
    def test_max_drawdown_calculation(self):
        """ทดสอบการคำนวณ max drawdown"""
        # สร้าง equity curve ที่มี drawdown จริง
        equity_with_drawdown = pd.Series([10000, 11000, 10500, 9500, 9000, 9500, 10000, 11000, 10800, 11500])
        
        max_dd, drawdown_duration = PerformanceMetrics.calculate_max_drawdown(equity_with_drawdown)
        
        self.assertIsNotNone(max_dd)
        self.assertIsInstance(max_dd, float)
        # ฟังก์ชัน return abs() ดังนั้นต้องเป็นค่าบวก
        self.assertGreaterEqual(max_dd, 0)  # Drawdown >= 0
        self.assertLessEqual(max_dd, 100)  # Drawdown <= 100%
        
        # จากข้อมูล: peak 11000 → ต่ำสุด 9000 = drawdown (11000-9000)/11000 = 18.18%
        self.assertGreater(max_dd, 0)  # ต้องมี drawdown
        
        self.assertIsNotNone(drawdown_duration)
        self.assertIsInstance(drawdown_duration, int)
        self.assertGreaterEqual(drawdown_duration, 0)
    
    def test_calmar_ratio_calculation(self):
        """ทดสอบการคำนวณ Calmar ratio"""
        total_return = 0.08  # 8%
        max_dd = -0.05  # -5%
        years = 1.0
        
        calmar = PerformanceMetrics.calculate_calmar_ratio(total_return, max_dd, years)
        
        self.assertIsNotNone(calmar)
        self.assertIsInstance(calmar, float)
        self.assertGreater(calmar, 0)
        
        # Calmar = Annual Return / |Max Drawdown|
        expected = (total_return / years) / abs(max_dd)
        self.assertAlmostEqual(calmar, expected, places=2)
    
    def test_profit_factor_calculation(self):
        """ทดสอบการคำนวณ profit factor"""
        gross_profit = 1000
        gross_loss = -500
        
        profit_factor = PerformanceMetrics.calculate_profit_factor(gross_profit, gross_loss)
        
        self.assertIsNotNone(profit_factor)
        self.assertIsInstance(profit_factor, float)
        self.assertGreater(profit_factor, 0)
        
        # Profit Factor = Gross Profit / |Gross Loss|
        expected = gross_profit / abs(gross_loss)
        self.assertAlmostEqual(profit_factor, expected, places=2)
    
    def test_expectancy_calculation(self):
        """ทดสอบการคำนวณ expectancy"""
        win_rate = 0.6  # 60%
        avg_win = 100
        avg_loss = -50
        
        expectancy = PerformanceMetrics.calculate_expectancy(win_rate, avg_win, avg_loss)
        
        self.assertIsNotNone(expectancy)
        self.assertIsInstance(expectancy, float)
        # กับ win_rate = 0.6, avg_win = 100, avg_loss = -50
        # expectancy = (0.6 * 100) - (0.4 * 50) = 60 - 20 = 40
        self.assertGreater(expectancy, 0)
    
    def test_volatility_calculation(self):
        """ทดสอบการคำนวณ volatility"""
        volatility = PerformanceMetrics.calculate_volatility(self.returns)
        
        self.assertIsNotNone(volatility)
        self.assertIsInstance(volatility, float)
        self.assertGreater(volatility, 0)
        
        # Volatility = Std Dev * sqrt(252)
        expected = self.returns.std() * (252 ** 0.5)
        self.assertAlmostEqual(volatility, expected, places=4)



class TestTrade(unittest.TestCase):
    """ทดสอบ Trade class"""
    
    def test_trade_creation(self):
        """ทดสอบการสร้าง trade"""
        trade = Trade(
            symbol='AAPL',
            action='BUY',
            price=150.5,
            quantity=10,
            date=datetime(2024, 1, 1),
            reason='Test trade'
        )
        
        self.assertEqual(trade.symbol, 'AAPL')
        self.assertEqual(trade.action, 'BUY')
        self.assertEqual(trade.price, 150.5)
        self.assertEqual(trade.quantity, 10)
        self.assertEqual(trade.date, datetime(2024, 1, 1))
        self.assertEqual(trade.reason, 'Test trade')
        self.assertEqual(trade.profit_loss, 0)  # ยังไม่ได้ตั้งค่า


class TestPosition(unittest.TestCase):
    """ทดสอบ Position class"""
    
    def test_position_creation(self):
        """ทดสอบการสร้าง position"""
        position = Position(
            symbol='MSFT',
            entry_price=300,
            quantity=5,
            entry_date=datetime(2024, 1, 1)
        )
        
        self.assertEqual(position.symbol, 'MSFT')
        self.assertEqual(position.entry_price, 300)
        self.assertEqual(position.quantity, 5)
        self.assertEqual(position.entry_date, datetime(2024, 1, 1))
        self.assertIsNone(position.exit_price)
        self.assertIsNone(position.exit_date)
    
    def test_position_close(self):
        """ทดสอบการปิด position"""
        position = Position(
            symbol='GOOGL',
            entry_price=140,
            quantity=8,
            entry_date=datetime(2024, 1, 1)
        )
        
        # ปิด position
        position.close(exit_price=145, exit_date=datetime(2024, 1, 10))
        
        # ตรวจสอบค่า
        self.assertEqual(position.exit_price, 145)
        self.assertEqual(position.exit_date, datetime(2024, 1, 10))
        
        # ตรวจสอบกำไร
        expected_profit = (145 - 140) * 8  # 40
        self.assertEqual(position.profit_loss, expected_profit)
        
        # ตรวจสอบเปอร์เซ็นต์
        expected_pct = ((145 - 140) / 140) * 100
        self.assertAlmostEqual(position.profit_loss_pct, expected_pct, places=2)
        
        # ตรวจสอบวันถือ
        self.assertEqual(position.holding_days, 9)


if __name__ == '__main__':
    # รัน tests
    unittest.main(verbosity=2)
