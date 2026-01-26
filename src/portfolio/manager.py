"""
Portfolio Manager Module
จัดการพอร์ตการลงทุนหุ้น
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PortfolioManager:
    """จัดการพอร์ตการลงทุนหุ้น"""
    
    def __init__(self, portfolio_file: str = "data/portfolio.json"):
        """
        Initialize Portfolio Manager
        
        Args:
            portfolio_file: ไฟล์เก็บข้อมูล portfolio
        """
        self.portfolio_file = portfolio_file
        self._ensure_data_dir()
        self.portfolio = self._load_portfolio()
    
    def _ensure_data_dir(self):
        """สร้างโฟลเดอร์ data ถ้ายังไม่มี"""
        data_dir = os.path.dirname(self.portfolio_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def _load_portfolio(self) -> List[Dict]:
        """โหลดข้อมูล portfolio จากไฟล์"""
        if os.path.exists(self.portfolio_file):
            try:
                with open(self.portfolio_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    logger.info(f"Loaded {len(data)} stocks from portfolio")
                    return data
            except Exception as e:
                logger.error(f"Error loading portfolio: {e}")
                return []
        return []
    
    def _save_portfolio(self):
        """บันทึกข้อมูล portfolio ลงไฟล์"""
        try:
            with open(self.portfolio_file, 'w', encoding='utf-8') as f:
                json.dump(self.portfolio, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.portfolio)} stocks to portfolio")
            return True
        except Exception as e:
            logger.error(f"Error saving portfolio: {e}")
            return False
    
    def add_stock(self, symbol: str, shares: float, buy_price: float, 
                  buy_date: str = None, notes: str = "") -> bool:
        """
        เพิ่มหุ้นเข้า portfolio
        
        Args:
            symbol: รหัสหุ้น (เช่น AAPL)
            shares: จำนวนหุ้น
            buy_price: ราคาซื้อต่อหุ้น
            buy_date: วันที่ซื้อ (YYYY-MM-DD)
            notes: หมายเหตุ
            
        Returns:
            True ถ้าเพิ่มสำเร็จ
        """
        if not buy_date:
            buy_date = datetime.now().strftime("%Y-%m-%d")
        
        # ตรวจสอบว่ามีหุ้นนี้แล้วหรือไม่
        for stock in self.portfolio:
            if stock['symbol'] == symbol.upper():
                # ถ้ามีแล้ว ให้อัพเดทข้อมูล (เฉลี่ยราคา)
                total_shares = stock['shares'] + shares
                total_cost = (stock['shares'] * stock['buy_price']) + (shares * buy_price)
                avg_price = total_cost / total_shares
                
                stock['shares'] = total_shares
                stock['buy_price'] = avg_price
                stock['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                stock['notes'] = notes if notes else stock.get('notes', '')
                
                logger.info(f"Updated {symbol}: {total_shares} shares @ avg ${avg_price:.2f}")
                return self._save_portfolio()
        
        # เพิ่มหุ้นใหม่
        stock_data = {
            'symbol': symbol.upper(),
            'shares': shares,
            'buy_price': buy_price,
            'buy_date': buy_date,
            'notes': notes,
            'added_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.portfolio.append(stock_data)
        logger.info(f"Added {symbol}: {shares} shares @ ${buy_price:.2f}")
        return self._save_portfolio()
    
    def remove_stock(self, symbol: str) -> bool:
        """
        ลบหุ้นออกจาก portfolio
        
        Args:
            symbol: รหัสหุ้น
            
        Returns:
            True ถ้าลบสำเร็จ
        """
        symbol = symbol.upper()
        original_len = len(self.portfolio)
        self.portfolio = [s for s in self.portfolio if s['symbol'] != symbol]
        
        if len(self.portfolio) < original_len:
            logger.info(f"Removed {symbol} from portfolio")
            return self._save_portfolio()
        
        logger.warning(f"Stock {symbol} not found in portfolio")
        return False
    
    def update_stock(self, symbol: str, shares: Optional[float] = None, 
                     buy_price: Optional[float] = None, notes: Optional[str] = None) -> bool:
        """
        อัพเดทข้อมูลหุ้นใน portfolio
        
        Args:
            symbol: รหัสหุ้น
            shares: จำนวนหุ้นใหม่
            buy_price: ราคาซื้อใหม่
            notes: หมายเหตุใหม่
            
        Returns:
            True ถ้าอัพเดทสำเร็จ
        """
        symbol = symbol.upper()
        
        for stock in self.portfolio:
            if stock['symbol'] == symbol:
                if shares is not None:
                    stock['shares'] = shares
                if buy_price is not None:
                    stock['buy_price'] = buy_price
                if notes is not None:
                    stock['notes'] = notes
                
                stock['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Updated {symbol} in portfolio")
                return self._save_portfolio()
        
        logger.warning(f"Stock {symbol} not found in portfolio")
        return False
    
    def get_portfolio(self) -> List[Dict]:
        """
        ดึงข้อมูล portfolio ทั้งหมด
        
        Returns:
            List ของหุ้นใน portfolio
        """
        return self.portfolio.copy()
    
    def get_stock(self, symbol: str) -> Optional[Dict]:
        """
        ดึงข้อมูลหุ้นเฉพาะตัว
        
        Args:
            symbol: รหัสหุ้น
            
        Returns:
            Dict ของข้อมูลหุ้น หรือ None ถ้าไม่พบ
        """
        symbol = symbol.upper()
        for stock in self.portfolio:
            if stock['symbol'] == symbol:
                return stock.copy()
        return None
    
    def get_symbols(self) -> List[str]:
        """
        ดึงรายชื่อหุ้นทั้งหมดใน portfolio
        
        Returns:
            List ของรหัสหุ้น
        """
        return [stock['symbol'] for stock in self.portfolio]
    
    def calculate_portfolio_value(self, current_prices: Dict[str, float]) -> Dict:
        """
        คำนวณมูลค่า portfolio
        
        Args:
            current_prices: Dict ของราคาปัจจุบัน {symbol: price}
            
        Returns:
            Dict ของข้อมูลมูลค่า portfolio
        """
        total_cost = 0.0
        total_value = 0.0
        
        stocks_detail = []
        
        for stock in self.portfolio:
            symbol = stock['symbol']
            shares = stock['shares']
            buy_price = stock['buy_price']
            
            cost = shares * buy_price
            current_price = current_prices.get(symbol, buy_price)
            value = shares * current_price
            
            profit_loss = value - cost
            profit_loss_pct = ((current_price - buy_price) / buy_price * 100) if buy_price > 0 else 0
            
            stocks_detail.append({
                'symbol': symbol,
                'shares': shares,
                'buy_price': buy_price,
                'current_price': current_price,
                'cost': cost,
                'value': value,
                'profit_loss': profit_loss,
                'profit_loss_pct': profit_loss_pct,
                'buy_date': stock.get('buy_date', 'N/A'),
                'notes': stock.get('notes', '')
            })
            
            total_cost += cost
            total_value += value
        
        total_profit_loss = total_value - total_cost
        total_profit_loss_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'total_cost': total_cost,
            'total_value': total_value,
            'total_profit_loss': total_profit_loss,
            'total_profit_loss_pct': total_profit_loss_pct,
            'stocks': stocks_detail,
            'num_stocks': len(stocks_detail)
        }
    
    def clear_portfolio(self) -> bool:
        """
        ล้างข้อมูล portfolio ทั้งหมด
        
        Returns:
            True ถ้าล้างสำเร็จ
        """
        self.portfolio = []
        logger.info("Cleared portfolio")
        return self._save_portfolio()
