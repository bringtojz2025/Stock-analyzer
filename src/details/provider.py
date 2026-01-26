"""
Stock Details Module
ดึงข้อมูลรายละเอียดของหุ้น
"""

import logging
import yfinance as yf
import pandas as pd
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDetailsProvider:
    """ดึงข้อมูลรายละเอียดของหุ้น"""
    
    # ข้อมูลตลาดของหุ้น
    MARKET_INFO = {
        'AAPL': {
            'name': 'Apple Inc.',
            'sector': 'เทคโนโลยี',
            'industry': 'อุตสาหกรรมอิเล็กทรอนิกส์',
            'market': 'NASDAQ',
            'description': 'บริษัทที่ผลิต iPhone, Mac, iPad และบริการต่างๆ',
            'country': 'สหรัฐอเมริกา',
            'founded': '1976'
        },
        'MSFT': {
            'name': 'Microsoft Corporation',
            'sector': 'เทคโนโลยี',
            'industry': 'ซอฟต์แวร์',
            'market': 'NASDAQ',
            'description': 'บริษัทซอฟต์แวร์ ผู้พัฒนา Windows, Office, Azure',
            'country': 'สหรัฐอเมริกา',
            'founded': '1975'
        },
        'GOOGL': {
            'name': 'Alphabet Inc.',
            'sector': 'เทคโนโลยี',
            'industry': 'ความปลอดภัยบนอินเทอร์เน็ต',
            'market': 'NASDAQ',
            'description': 'บริษัทแม่ของ Google ให้บริการค้นหาและโฆษณาออนไลน์',
            'country': 'สหรัฐอเมริกา',
            'founded': '1998'
        },
        'AMZN': {
            'name': 'Amazon.com Inc.',
            'sector': 'ผู้บริโภค',
            'industry': 'ค้าปลีกออนไลน์',
            'market': 'NASDAQ',
            'description': 'ผู้ค้าปลีกออนไลน์ที่ใหญ่ที่สุด AWS, บริการคลาวด์',
            'country': 'สหรัฐอเมริกา',
            'founded': '1994'
        },
        'TSLA': {
            'name': 'Tesla Inc.',
            'sector': 'อุตสาหกรรมยานพาหนะ',
            'industry': 'รถยนต์ไฟฟ้า',
            'market': 'NASDAQ',
            'description': 'ผู้ผลิตรถยนต์ไฟฟ้า แบตเตอรี่ พลังงานหมุนเวียน',
            'country': 'สหรัฐอเมริกา',
            'founded': '2003'
        },
        'META': {
            'name': 'Meta Platforms Inc.',
            'sector': 'เทคโนโลยี',
            'industry': 'สื่อสังคม',
            'market': 'NASDAQ',
            'description': 'บริษัทแม่ของ Facebook, Instagram, WhatsApp',
            'country': 'สหรัฐอเมริกา',
            'founded': '2004'
        },
        'NVDA': {
            'name': 'NVIDIA Corporation',
            'sector': 'เทคโนโลยี',
            'industry': 'อุตสาหกรรมอิเล็กทรอนิกส์',
            'market': 'NASDAQ',
            'description': 'ผู้ผลิต GPU การ์ดจอสำหรับเกมส์ และ AI',
            'country': 'สหรัฐอเมริกา',
            'founded': '1993'
        },
        'NFLX': {
            'name': 'Netflix Inc.',
            'sector': 'ผู้บริโภค',
            'industry': 'บันเทิงออนไลน์',
            'market': 'NASDAQ',
            'description': 'บริการสตรีมมิงเนื้อหาวิดีโอ ละครโทรทัศน์ และภาพยนตร์',
            'country': 'สหรัฐอเมริกา',
            'founded': '1997'
        },
        'JPM': {
            'name': 'JPMorgan Chase & Co.',
            'sector': 'การเงิน',
            'industry': 'บริการการเงิน',
            'market': 'NYSE',
            'description': 'ธนาคารพาณิชย์ ให้บริการเงินกู้ หลักทรัพย์ ประกันภัย',
            'country': 'สหรัฐอเมริกา',
            'founded': '2000'
        },
        'V': {
            'name': 'Visa Inc.',
            'sector': 'การเงิน',
            'industry': 'บริการการชำระเงิน',
            'market': 'NYSE',
            'description': 'บริษัทประมวลผลการชำระเงินที่ใหญ่ที่สุดในโลก',
            'country': 'สหรัฐอเมริกา',
            'founded': '1958'
        },
    }
    
    @staticmethod
    def get_stock_info(symbol):
        """ดึงข้อมูลหุ้นจาก yfinance"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get current price with fallback
            current_price = info.get('currentPrice')
            if current_price is None or current_price == 0:
                current_price = info.get('regularMarketPrice')
            if current_price is None or current_price == 0:
                current_price = info.get('previousClose')
            
            # Get previous close
            previous_close = info.get('previousClose')
            if previous_close is None or previous_close == 0:
                previous_close = info.get('regularMarketPreviousClose')
            
            # Get PE ratio
            pe_ratio = info.get('trailingPE')
            if pe_ratio is None:
                pe_ratio = info.get('forwardPE')
            
            return {
                'symbol': symbol,
                'name': info.get('longName', info.get('shortName', 'ไม่ทราบชื่อ')),
                'current_price': current_price if current_price else 'N/A',
                'previous_close': previous_close if previous_close else 'N/A',
                'market_cap': info.get('marketCap', 'ไม่ทราบ'),
                'pe_ratio': pe_ratio,
                'forward_pe': info.get('forwardPE'),
                'peg_ratio': info.get('pegRatio'),
                'price_to_book': info.get('priceToBook'),
                'price_to_sales': info.get('priceToSalesTrailing12Months'),
                'dividend_yield': info.get('dividendYield'),
                'fifty_two_week_high': info.get('fiftyTwoWeekHigh'),
                'fifty_two_week_low': info.get('fiftyTwoWeekLow'),
                'avg_volume': info.get('averageVolume', info.get('volume')),
                'sector': info.get('sector', 'ไม่ทราบ'),
                'industry': info.get('industry', 'ไม่ทราบ'),
                'website': info.get('website', 'ไม่ทราบ'),
                'description': info.get('longBusinessSummary', 'ไม่มีรายละเอียด'),
                'country': info.get('country', 'ไม่ทราบ'),
                'employees': info.get('fullTimeEmployees', 'ไม่ทราบ'),
                # Financial health metrics
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'profit_margin': info.get('profitMargins'),
                'debt_to_equity': info.get('debtToEquity'),
                'current_ratio': info.get('currentRatio'),
                'beta': info.get('beta'),
            }
        except Exception as e:
            logger.error(f"Error getting info for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def get_enhanced_stock_info(symbol):
        """ดึงข้อมูลหุ้นแบบรายละเอียด"""
        info = StockDetailsProvider.get_stock_info(symbol)
        
        # รวมข้อมูลจาก MARKET_INFO
        if symbol in StockDetailsProvider.MARKET_INFO:
            market_info = StockDetailsProvider.MARKET_INFO[symbol]
            if info:
                info.update(market_info)
        
        return info
    
    @staticmethod
    def get_historical_data(symbol, period='1y'):
        """ดึงข้อมูลราคาประวัติศาสตร์"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            return data
        except Exception as e:
            logger.error(f"Error getting historical data for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def calculate_price_change(symbol, period='1y'):
        """คำนวณการเปลี่ยนแปลงราคา"""
        try:
            data = StockDetailsProvider.get_historical_data(symbol, period)
            if data is not None and len(data) > 0:
                start_price = data['Close'].iloc[0]
                end_price = data['Close'].iloc[-1]
                change = end_price - start_price
                change_percent = (change / start_price) * 100
                
                return {
                    'start_price': start_price,
                    'end_price': end_price,
                    'change': change,
                    'change_percent': change_percent,
                    'high': data['High'].max(),
                    'low': data['Low'].min(),
                }
            return None
        except Exception as e:
            logger.error(f"Error calculating price change for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def get_market_category(market_cap):
        """จำแนกหมวดหมู่ตลาด"""
        if market_cap is None or market_cap == 'ไม่ทราบ':
            return 'ไม่ทราบ'
        
        try:
            if isinstance(market_cap, str):
                # แปลง string ให้เป็นตัวเลข
                market_cap = float(market_cap)
            
            if market_cap < 300e6:  # < $300M
                return '💎 จิ๋ว (Micro-cap) < $300M'
            elif market_cap < 2e9:    # < $2B
                return '🔹 เล็ก (Small-cap) < $2B'
            elif market_cap < 10e9:   # < $10B
                return '🔷 กลาง (Mid-cap) < $10B'
            elif market_cap < 100e9:  # < $100B
                return '🏪 ใหญ่ (Large-cap) < $100B'
            else:
                return '🏭 ยิ่งใหญ่ (Mega-cap) > $100B'
        except:
            return 'ไม่ทราบ'
    
    @staticmethod
    def format_market_cap(market_cap):
        """ฟอร์แมตค่า Market Cap"""
        if market_cap is None or market_cap == 'ไม่ทราบ':
            return 'ไม่ทราบ'
        
        try:
            if isinstance(market_cap, str):
                market_cap = float(market_cap)
            
            if market_cap >= 1e9:
                return f"${market_cap/1e9:.1f}B"
            elif market_cap >= 1e6:
                return f"${market_cap/1e6:.1f}M"
            else:
                return f"${market_cap:.0f}"
        except:
            return str(market_cap)


if __name__ == "__main__":
    # ทดสอบ
    provider = StockDetailsProvider()
    
    # ดึงข้อมูล AAPL
    print("\n📊 ข้อมูลหุ้น AAPL:")
    info = provider.get_enhanced_stock_info('AAPL')
    if info:
        print(f"ชื่อ: {info.get('name')}")
        print(f"ตลาด: {info.get('market')}")
        print(f"ส่วนชั้น: {info.get('sector')}")
        print(f"อุตสาหกรรม: {info.get('industry')}")
        print(f"ราคาปัจจุบัน: ${info.get('current_price'):.2f}")
        print(f"Market Cap: {provider.format_market_cap(info.get('market_cap'))}")
    
    # คำนวณการเปลี่ยนแปลง
    print("\n📈 การเปลี่ยนแปลงราคา (1 ปี):")
    change = provider.calculate_price_change('AAPL', '1y')
    if change:
        print(f"ราคาเริ่ม: ${change['start_price']:.2f}")
        print(f"ราคาปัจจุบัน: ${change['end_price']:.2f}")
        print(f"เปลี่ยนแปลง: {change['change_percent']:.2f}%")
