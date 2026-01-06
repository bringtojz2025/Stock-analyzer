"""
Stock Discovery Scanner
สแกนและค้นหาหุ้นจากตลาด
"""

import logging
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockScanner:
    """สแกนหุ้นจากตลาด"""
    
    # หุ้นที่มีแนวโน้มสูง (Large Cap & Mid Cap)
    POPULAR_STOCKS = [
        'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
        'META', 'NFLX', 'NVDA', 'AMD', 'INTEL',
        'JPM', 'BAC', 'WFC', 'GS', 'MS',
        'JNJ', 'PFE', 'UNH', 'ABBV', 'MRK',
        'PG', 'KO', 'MCD', 'NKE', 'ADBE',
        'CRM', 'ORCL', 'SAP', 'IBM', 'CSCO',
        'MA', 'V', 'PYPL', 'SHOP', 'DASH',
        'UBER', 'ABNB', 'SQ', 'COIN', 'RIOT'
    ]
    
    # หุ้นจิ๋ว (Micro-cap) ที่มีศักยภาพ
    MICROCAP_STOCKS = [
        'CLSK', 'RIOT', 'MARA', 'CORZ', 'MICT',
        'IMTX', 'TLSS', 'GFAI', 'FFIE', 'NKLA',
        'ZASH', 'IDAI', 'PTG', 'INTU', 'REXR',
        'PHUN', 'REFR', 'OCGX', 'AGRX', 'GROM',
        'RMTI', 'LGMK', 'PROG', 'CIDM', 'TREV'
    ]
    
    def __init__(self):
        self.popular_stocks = self.POPULAR_STOCKS
        self.microcap_stocks = self.MICROCAP_STOCKS
    
    def get_popular_stocks(self):
        """
        ดึงรายชื่อหุ้นที่มีแนวโน้มสูง
        
        Returns:
            list: รายชื่อสัญลักษณ์หุ้น
        """
        logger.info(f"Getting {len(self.popular_stocks)} popular stocks")
        return self.popular_stocks
    
    def get_microcap_stocks(self):
        """
        ดึงรายชื่อหุ้นจิ๋วที่มีศักยภาพ
        
        Returns:
            list: รายชื่อสัญลักษณ์หุ้นจิ๋ว
        """
        logger.info(f"Getting {len(self.microcap_stocks)} microcap stocks")
        return self.microcap_stocks
    
    def scan_trending_stocks(self, period='5d'):
        """
        สแกนหุ้นที่มีแนวโน้มขึ้นในช่วง 5 วันล่าสุด
        
        Args:
            period: ระยะเวลา
        
        Returns:
            dict: หุ้นที่มีแนวโน้มขึ้น
        """
        logger.info("Scanning for trending stocks...")
        trending = {
            'up_5_percent': [],
            'up_10_percent': [],
            'up_20_percent': [],
            'down_5_percent': []
        }
        
        stocks_to_scan = self.popular_stocks[:15]  # สแกน 15 หุ้นแรก
        
        for symbol in stocks_to_scan:
            try:
                data = yf.download(symbol, period=period, progress=False)
                if data is not None and len(data) > 0:
                    first_price = data['Close'].iloc[0]
                    last_price = data['Close'].iloc[-1]
                    change = ((last_price - first_price) / first_price) * 100
                    
                    if change >= 20:
                        trending['up_20_percent'].append({
                            'symbol': symbol,
                            'change': change,
                            'price': last_price
                        })
                    elif change >= 10:
                        trending['up_10_percent'].append({
                            'symbol': symbol,
                            'change': change,
                            'price': last_price
                        })
                    elif change >= 5:
                        trending['up_5_percent'].append({
                            'symbol': symbol,
                            'change': change,
                            'price': last_price
                        })
                    elif change <= -5:
                        trending['down_5_percent'].append({
                            'symbol': symbol,
                            'change': change,
                            'price': last_price
                        })
            except Exception as e:
                logger.warning(f"Error scanning {symbol}: {str(e)}")
        
        return trending
    
    def scan_microcap_gainers(self, min_price=0, max_price=None, min_volume=None):
        """
        สแกนหุ้นจิ๋วที่มีแนวโน้มขึ้น
        
        Args:
            min_price: ราคาต่ำสุด (เริ่มต้น 0)
            max_price: ราคาสูงสุด (เริ่มต้น ไม่มีจำกัด)
            min_volume: ปริมาณการซื้อขายต่ำสุด (เริ่มต้น ไม่มีจำกัด)
        
        Returns:
            dict: หุ้นจิ๋วที่มีศักยภาพ
        """
        logger.info(f"Scanning microcap gainers (Price: ${min_price}-${max_price if max_price else 'unlimited'})...")
        gainers = {
            'high_volatility': [],      # ความผันผวนสูง
            'low_price_high_gain': [],  # ราคาต่ำแต่ขึ้นมาก
            'breakout': []              # ทะลุขึ้น
        }
        
        for symbol in self.microcap_stocks[:15]:
            try:
                data = yf.download(symbol, period='3mo', progress=False)
                if data is not None and isinstance(data, pd.DataFrame) and len(data) >= 20:
                    current_price = float(data['Close'].iloc[-1])
                    
                    # ตรวจสอบเงื่อนไขราคา
                    if current_price < min_price:
                        continue
                    if max_price is not None and current_price > max_price:
                        continue
                    
                    high_52 = float(data['Close'].max())
                    low_52 = float(data['Close'].min())
                    
                    # คำนวณ Volatility
                    volatility = (float(data['Close'].std()) / float(data['Close'].mean())) * 100
                    
                    # ตรวจสอบ Breakout
                    recent_20_high = float(data['Close'].tail(20).max())
                    if current_price >= recent_20_high * 0.99:
                        gainers['breakout'].append({
                            'symbol': symbol,
                            'price': current_price,
                            'volatility': volatility
                        })
                    
                    # ความผันผวนสูง
                    if volatility > 50:
                        gainers['high_volatility'].append({
                            'symbol': symbol,
                            'price': current_price,
                            'volatility': volatility,
                            'range': float(high_52 - low_52)
                        })
                    
                    # ราคาต่ำแต่ขึ้นมาก
                    if current_price < 5 and (high_52 - current_price) > (current_price - low_52):
                        gainers['low_price_high_gain'].append({
                            'symbol': symbol,
                            'price': current_price,
                            'potential_upside': ((high_52 - current_price) / current_price) * 100
                        })
            except Exception as e:
                logger.warning(f"Error scanning microcap {symbol}: {str(e)}")
        
        return gainers
    
    def get_stock_info(self, symbol):
        """
        ดึงข้อมูลหุ้นพื้นฐาน
        
        Args:
            symbol: สัญลักษณ์หุ้น
        
        Returns:
            dict: ข้อมูลหุ้น
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'name': info.get('longName', 'N/A'),
                'price': info.get('currentPrice', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A')
            }
        except Exception as e:
            logger.error(f"Error getting info for {symbol}: {str(e)}")
            return None
    
    def get_stock_summary(self, symbol):
        """
        ดึงข้อมูลสรุปของหุ้น
        
        Args:
            symbol: สัญลักษณ์หุ้น
        
        Returns:
            dict: สรุปข้อมูล
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # คำนวณ Market Cap Category
            market_cap = info.get('marketCap', 0)
            if market_cap == 0:
                market_cap_category = 'ไม่ทราบ'
            elif market_cap < 300e6:  # < $300M
                market_cap_category = 'จิ๋ว (Micro-cap) < $300M'
            elif market_cap < 2e9:    # < $2B
                market_cap_category = 'เล็ก (Small-cap) < $2B'
            elif market_cap < 10e9:   # < $10B
                market_cap_category = 'กลาง (Mid-cap) < $10B'
            else:
                market_cap_category = 'ใหญ่ (Large-cap) > $10B'
            
            return {
                'symbol': symbol,
                'name': info.get('longName', 'ไม่ทราบชื่อ'),
                'current_price': info.get('currentPrice', 'N/A'),
                'market_cap': market_cap,
                'market_cap_category': market_cap_category,
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'forward_pe': info.get('forwardPE', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'sector': info.get('sector', 'ไม่ทราบ'),
                'industry': info.get('industry', 'ไม่ทราบ'),
                '52_week_high': info.get('fiftyTwoWeekHigh', 'N/A'),
                '52_week_low': info.get('fiftyTwoWeekLow', 'N/A')
            }
        except Exception as e:
            logger.error(f"Error getting summary for {symbol}: {str(e)}")
            return None


if __name__ == "__main__":
    scanner = StockScanner()
    
    # ดึงหุ้นที่มีแนวโน้มสูง
    print("\n📊 หุ้นที่มีแนวโน้มสูง:")
    popular = scanner.get_popular_stocks()
    print(f"จำนวน: {len(popular)} หุ้น")
    print(f"ตัวอย่าง: {', '.join(popular[:10])}")
    
    # สแกนหุ้นที่มีแนวโน้มขึ้น
    print("\n📈 หุ้นที่มีแนวโน้มขึ้น (5 วันล่าสุด):")
    trending = scanner.scan_trending_stocks()
    print(f"ขึ้น 20%+: {len(trending['up_20_percent'])} หุ้น")
    print(f"ขึ้น 10-20%: {len(trending['up_10_percent'])} หุ้น")
    
    # สแกนหุ้นจิ๋ว
    print("\n💎 หุ้นจิ๋วที่มีศักยภาพ:")
    microcap = scanner.get_microcap_stocks()
    print(f"จำนวน: {len(microcap)} หุ้น")
    print(f"ตัวอย่าง: {', '.join(microcap[:10])}")
