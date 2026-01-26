"""
Backtesting Engine
ทดสอบกลยุทธ์การเทรดกับข้อมูลในอดีต
"""

import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Trade:
    """คลาสสำหรับเก็บข้อมูลการซื้อขาย"""
    
    def __init__(self, symbol, action, price, quantity, date, reason=""):
        self.symbol = symbol
        self.action = action  # 'BUY' หรือ 'SELL'
        self.price = price
        self.quantity = quantity
        self.date = date
        self.reason = reason
        self.profit_loss = 0
        self.profit_loss_pct = 0
    
    def __repr__(self):
        return f"Trade({self.action} {self.symbol} @ ${self.price:.2f} on {self.date})"


class Position:
    """คลาสสำหรับเก็บข้อมูล Position ที่ถือครอง"""
    
    def __init__(self, symbol, entry_price, quantity, entry_date):
        self.symbol = symbol
        self.entry_price = entry_price
        self.quantity = quantity
        self.entry_date = entry_date
        self.exit_price = None
        self.exit_date = None
        self.profit_loss = 0
        self.profit_loss_pct = 0
        self.holding_days = 0
    
    def close(self, exit_price, exit_date):
        """ปิด Position"""
        self.exit_price = exit_price
        self.exit_date = exit_date
        self.profit_loss = (exit_price - self.entry_price) * self.quantity
        self.profit_loss_pct = ((exit_price - self.entry_price) / self.entry_price) * 100
        self.holding_days = (exit_date - self.entry_date).days
    
    def __repr__(self):
        status = f"OPEN @ ${self.entry_price:.2f}"
        if self.exit_price:
            status = f"CLOSED @ ${self.exit_price:.2f} ({self.profit_loss_pct:+.2f}%)"
        return f"Position({self.symbol} {status})"


class Backtester:
    """
    ระบบ Backtesting สำหรับทดสอบกลยุทธ์การเทรด
    
    Features:
    - ทดสอบกับข้อมูลในอดีต
    - คำนวณ performance metrics
    - จำลองค่า commission และ slippage
    - Position sizing
    - Stop loss และ Take profit
    """
    
    def __init__(self, 
                 initial_capital=10000,
                 commission=0.001,  # 0.1%
                 slippage=0.0005,   # 0.05%
                 position_size_pct=0.2):  # ใช้ 20% ของเงินต่อ trade
        """
        Initialize Backtester
        
        Args:
            initial_capital: เงินทุนเริ่มต้น ($)
            commission: ค่า commission (0.001 = 0.1%)
            slippage: ค่า slippage (0.0005 = 0.05%)
            position_size_pct: เปอร์เซ็นต์เงินทุนต่อ trade (0.2 = 20%)
        """
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.commission = commission
        self.slippage = slippage
        self.position_size_pct = position_size_pct
        
        # Trade tracking
        self.trades: List[Trade] = []
        self.positions: Dict[str, Position] = {}  # Open positions
        self.closed_positions: List[Position] = []
        
        # Portfolio tracking
        self.portfolio_values = []  # (date, value)
        self.equity_curve = pd.DataFrame()
        
        logger.info(f"Backtester initialized with ${initial_capital:,.2f}")
    
    def reset(self):
        """รีเซ็ตสถานะทั้งหมด"""
        self.capital = self.initial_capital
        self.trades = []
        self.positions = {}
        self.closed_positions = []
        self.portfolio_values = []
        self.equity_curve = pd.DataFrame()
        logger.info("Backtester reset")
    
    def calculate_position_size(self, price):
        """
        คำนวณจำนวนหุ้นที่ซื้อตาม position sizing
        
        Args:
            price: ราคาหุ้น
            
        Returns:
            int: จำนวนหุ้น
        """
        max_investment = self.capital * self.position_size_pct
        quantity = int(max_investment / price)
        return max(1, quantity)  # อย่างน้อย 1 หุ้น
    
    def execute_trade(self, symbol, action, price, date, reason="", stop_loss=None, take_profit=None):
        """
        ดำเนินการซื้อขาย
        
        Args:
            symbol: รหัสหุ้น
            action: 'BUY' หรือ 'SELL'
            price: ราคา
            date: วันที่ทำการซื้อขาย
            reason: เหตุผลในการซื้อขาย
            stop_loss: ราคา Stop Loss
            take_profit: ราคา Take Profit
            
        Returns:
            bool: สำเร็จหรือไม่
        """
        # Apply slippage
        if action == 'BUY':
            execution_price = price * (1 + self.slippage)
        else:
            execution_price = price * (1 - self.slippage)
        
        if action == 'BUY':
            # ตรวจสอบว่ามีเงินพอซื้อหรือไม่
            quantity = self.calculate_position_size(execution_price)
            total_cost = execution_price * quantity
            commission_fee = total_cost * self.commission
            
            if self.capital >= (total_cost + commission_fee):
                # ซื้อหุ้น
                self.capital -= (total_cost + commission_fee)
                
                # สร้าง Position
                position = Position(symbol, execution_price, quantity, date)
                self.positions[symbol] = position
                
                # บันทึก Trade
                trade = Trade(symbol, action, execution_price, quantity, date, reason)
                self.trades.append(trade)
                
                logger.info(f"BUY {quantity} {symbol} @ ${execution_price:.2f} (Commission: ${commission_fee:.2f})")
                return True
            else:
                logger.warning(f"Insufficient capital for BUY {symbol}")
                return False
        
        elif action == 'SELL':
            # ตรวจสอบว่ามี Position หรือไม่
            if symbol in self.positions:
                position = self.positions[symbol]
                quantity = position.quantity
                
                # ขายหุ้น
                total_revenue = execution_price * quantity
                commission_fee = total_revenue * self.commission
                self.capital += (total_revenue - commission_fee)
                
                # ปิด Position
                position.close(execution_price, date)
                self.closed_positions.append(position)
                del self.positions[symbol]
                
                # บันทึก Trade
                trade = Trade(symbol, action, execution_price, quantity, date, reason)
                trade.profit_loss = position.profit_loss
                trade.profit_loss_pct = position.profit_loss_pct
                self.trades.append(trade)
                
                logger.info(f"SELL {quantity} {symbol} @ ${execution_price:.2f} (P/L: {position.profit_loss_pct:+.2f}%)")
                return True
            else:
                logger.warning(f"No position to SELL for {symbol}")
                return False
        
        return False
    
    def check_stop_loss_take_profit(self, symbol, current_price, date, stop_loss=None, take_profit=None):
        """
        ตรวจสอบ Stop Loss และ Take Profit
        
        Args:
            symbol: รหัสหุ้น
            current_price: ราคาปัจจุบัน
            date: วันที่
            stop_loss: ราคา Stop Loss
            take_profit: ราคา Take Profit
            
        Returns:
            bool: ถูก trigger หรือไม่
        """
        if symbol not in self.positions:
            return False
        
        position = self.positions[symbol]
        
        # Check Stop Loss
        if stop_loss and current_price <= stop_loss:
            logger.info(f"Stop Loss triggered for {symbol}")
            self.execute_trade(symbol, 'SELL', current_price, date, "Stop Loss")
            return True
        
        # Check Take Profit
        if take_profit and current_price >= take_profit:
            logger.info(f"Take Profit triggered for {symbol}")
            self.execute_trade(symbol, 'SELL', current_price, date, "Take Profit")
            return True
        
        return False
    
    def update_portfolio_value(self, date, current_prices):
        """
        อัปเดตมูลค่า Portfolio
        
        Args:
            date: วันที่
            current_prices: dict ของราคาปัจจุบัน {symbol: price}
        """
        # คำนวณมูลค่า positions ที่ถือครอง
        positions_value = 0
        for symbol, position in self.positions.items():
            if symbol in current_prices:
                positions_value += current_prices[symbol] * position.quantity
        
        total_value = self.capital + positions_value
        self.portfolio_values.append((date, total_value))
    
    def run_backtest(self, analyzer_app, symbols, start_date, end_date, 
                     strategy='technical', min_confidence=0.6):
        """
        รัน Backtest ด้วยข้อมูลย้อนหลังจริง
        
        Args:
            analyzer_app: StockAnalyzerApp instance
            symbols: รายการหุ้นที่จะทดสอบ
            start_date: วันเริ่มต้น (YYYY-MM-DD)
            end_date: วันสิ้นสุด (YYYY-MM-DD)
            strategy: กลยุทธ์ ('technical', 'ai', 'combined')
            min_confidence: ความมั่นใจขั้นต่ำสำหรับสัญญาณ
            
        Returns:
            dict: ผลลัพธ์การทดสอบ
        """
        logger.info(f"Starting backtest from {start_date} to {end_date}")
        self.reset()
        
        # แปลง string เป็น datetime
        start_dt = pd.to_datetime(start_date)
        end_dt = pd.to_datetime(end_date)
        
        # ดึงข้อมูลย้อนหลังของแต่ละหุ้น
        from src.data.fetcher import StockDataFetcher
        fetcher = StockDataFetcher()
        
        historical_data = {}
        for symbol in symbols:
            try:
                # ดึงข้อมูลย้อนหลังพอสำหรับคำนวณ indicators
                days_diff = (end_dt - start_dt).days
                period = 'max' if days_diff > 365 else f'{days_diff + 200}d'
                
                data = fetcher.fetch_historical_data(symbol, period=period)
                if data is not None and not data.empty:
                    # แปลง timezone-aware index เป็น timezone-naive
                    try:
                        data.index = pd.to_datetime(data.index).tz_localize(None)
                    except:
                        pass  # ถ้าไม่มี timezone ก็ข้าม
                    
                    # กรองเฉพาะช่วงที่ต้องการ + ข้อมูลย้อนหลัง 200 วันเพื่อคำนวณ indicators
                    lookback_start = start_dt - pd.Timedelta(days=200)
                    data_filtered = data[data.index >= lookback_start]
                    historical_data[symbol] = data_filtered
                    logger.info(f"Loaded {len(data_filtered)} days of data for {symbol}")
            except Exception as e:
                logger.error(f"Error fetching {symbol}: {str(e)}")
        
        if not historical_data:
            logger.error("No historical data available")
            return self.get_results()
        
        # สร้าง date range เฉพาะวันที่มีการซื้อขาย (business days)
        date_range = pd.bdate_range(start=start_dt, end=end_dt)
        
        # วนลูปผ่านแต่ละวัน
        for current_date in date_range:
            current_prices = {}
            
            # ตรวจสอบแต่ละหุ้น
            for symbol in symbols:
                if symbol not in historical_data:
                    continue
                
                data = historical_data[symbol]
                
                # หาข้อมูลณ current_date (ใช้ข้อมูลถึงวันนั้น)
                data_up_to_date = data[data.index <= current_date]
                
                if len(data_up_to_date) < 50:  # ต้องมีข้อมูลพอสำหรับ indicators
                    continue
                
                # ใช้ข้อมูลล่าสุด (ณ current_date)
                current_price = data_up_to_date['Close'].iloc[-1]
                current_prices[symbol] = current_price
                
                # คำนวณ indicators ณ current_date
                from src.analysis.technical import TechnicalAnalyzer
                analyzer = TechnicalAnalyzer()
                technical_summary = analyzer.get_technical_summary(data_up_to_date)
                
                # คำนวณสัญญาณ
                from src.signals.generator import SignalGenerator
                signal_gen = SignalGenerator()
                signals = signal_gen.generate_signals_from_indicators(technical_summary)
                entry_exit = signal_gen.generate_entry_exit_points(data_up_to_date)
                
                # ตรวจสอบ Stop Loss / Take Profit สำหรับ positions ที่เปิดอยู่
                if symbol in self.positions:
                    stop_loss = entry_exit.get('stop_loss')
                    take_profit = entry_exit.get('target_price')
                    self.check_stop_loss_take_profit(symbol, current_price, current_date, 
                                                     stop_loss, take_profit)
                
                # ตรวจสอบสัญญาณซื้อ
                if signals.get('buy') == 1 and signals.get('confidence', 0) >= min_confidence:
                    if symbol not in self.positions:  # ยังไม่มี position
                        reason = ", ".join(signals.get('reasons', []))[:100]  # จำกัดความยาว
                        self.execute_trade(symbol, 'BUY', current_price, current_date, reason)
                
                # ตรวจสอบสัญญาณขาย
                elif signals.get('sell') == 1 and signals.get('confidence', 0) >= min_confidence:
                    if symbol in self.positions:  # มี position อยู่
                        reason = ", ".join(signals.get('reasons', []))[:100]
                        self.execute_trade(symbol, 'SELL', current_price, current_date, reason)
            
            # อัปเดตมูลค่า portfolio
            self.update_portfolio_value(current_date, current_prices)
        
        # ปิด positions ที่เหลือ (ณ วันสุดท้าย)
        for symbol in list(self.positions.keys()):
            if symbol in current_prices:
                self.execute_trade(symbol, 'SELL', current_prices[symbol], end_dt, 
                                 "End of backtest")
        
        logger.info(f"Backtest completed. Final capital: ${self.capital:,.2f}")
        
        return self.get_results()
    
    def get_results(self):
        """
        สรุปผลลัพธ์การทดสอบ
        
        Returns:
            dict: ผลลัพธ์ทั้งหมด
        """
        if not self.portfolio_values:
            return {}
        
        # สร้าง equity curve
        dates, values = zip(*self.portfolio_values)
        self.equity_curve = pd.DataFrame({
            'Date': dates,
            'Portfolio Value': values
        }).set_index('Date')
        
        # คำนวณ metrics
        final_value = self.capital
        total_return = ((final_value - self.initial_capital) / self.initial_capital) * 100
        
        # นับ trades
        total_trades = len([t for t in self.trades if t.action == 'BUY'])
        winning_trades = len([p for p in self.closed_positions if p.profit_loss > 0])
        losing_trades = len([p for p in self.closed_positions if p.profit_loss < 0])
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        
        # คำนวณ Average Win/Loss
        wins = [p.profit_loss for p in self.closed_positions if p.profit_loss > 0]
        losses = [p.profit_loss for p in self.closed_positions if p.profit_loss < 0]
        avg_win = np.mean(wins) if wins else 0
        avg_loss = np.mean(losses) if losses else 0
        
        # คำนวณ Max Drawdown
        peak = self.initial_capital
        max_drawdown = 0
        for _, value in self.portfolio_values:
            if value > peak:
                peak = value
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_drawdown:
                max_drawdown = drawdown
        
        results = {
            'initial_capital': self.initial_capital,
            'final_capital': final_value,
            'total_return': total_return,
            'total_return_pct': total_return,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'profit_factor': abs(avg_win / avg_loss) if avg_loss != 0 else 0,
            'max_drawdown': max_drawdown,
            'trades': self.trades,
            'closed_positions': self.closed_positions,
            'equity_curve': self.equity_curve
        }
        
        return results
    
    def get_trade_history(self):
        """
        ดึงประวัติการซื้อขายทั้งหมด
        
        Returns:
            pd.DataFrame: ตาราง trade history
        """
        if not self.trades:
            return pd.DataFrame()
        
        data = []
        for trade in self.trades:
            data.append({
                'Date': trade.date,
                'Symbol': trade.symbol,
                'Action': trade.action,
                'Price': trade.price,
                'Quantity': trade.quantity,
                'Total': trade.price * trade.quantity,
                'P/L': trade.profit_loss,
                'P/L %': trade.profit_loss_pct,
                'Reason': trade.reason
            })
        
        return pd.DataFrame(data)


if __name__ == "__main__":
    # ทดสอบ Backtester
    print("Testing Backtester...")
    
    backtester = Backtester(initial_capital=10000)
    print(f"Initial capital: ${backtester.capital:,.2f}")
    
    # จำลองการซื้อขาย
    from datetime import datetime
    
    # ซื้อ AAPL
    backtester.execute_trade('AAPL', 'BUY', 150.0, datetime(2024, 1, 1), "Test buy")
    print(f"After BUY: ${backtester.capital:,.2f}")
    
    # ขาย AAPL
    backtester.execute_trade('AAPL', 'SELL', 160.0, datetime(2024, 2, 1), "Test sell")
    print(f"After SELL: ${backtester.capital:,.2f}")
    
    # แสดงผลลัพธ์
    results = backtester.get_results()
    print(f"\nResults:")
    print(f"Total Return: {results['total_return']:.2f}%")
    print(f"Win Rate: {results['win_rate']:.2f}%")
