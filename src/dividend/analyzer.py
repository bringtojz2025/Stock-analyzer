"""
Dividend Stock Analyzer
วิเคราะห์หุ้นปันผลและค้นหาหุ้นที่จ่ายปันผลสูง
"""

import logging
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DividendAnalyzer:
    """วิเคราะห์หุ้นปันผล"""
    
    # หุ้นปันผลที่มีชื่อเสียง
    HIGH_DIVIDEND_STOCKS = {
        'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'yield': 3.5},
        'PG': {'name': 'Procter & Gamble', 'sector': 'Consumer', 'yield': 2.5},
        'KO': {'name': 'Coca-Cola', 'sector': 'Consumer', 'yield': 3.0},
        'MCD': {'name': "McDonald's", 'sector': 'Consumer', 'yield': 2.3},
        'WMT': {'name': 'Walmart', 'sector': 'Consumer', 'yield': 1.5},
        'PEP': {'name': 'PepsiCo', 'sector': 'Consumer', 'yield': 2.8},
        'ABBV': {'name': 'AbbVie', 'sector': 'Healthcare', 'yield': 4.0},
        'PM': {'name': 'Philip Morris', 'sector': 'Consumer', 'yield': 5.8},
        'T': {'name': 'AT&T', 'sector': 'Telecom', 'yield': 7.2},
        'VZ': {'name': 'Verizon', 'sector': 'Telecom', 'yield': 6.5},
        'IBM': {'name': 'IBM', 'sector': 'Technology', 'yield': 3.8},
        'MSFT': {'name': 'Microsoft', 'sector': 'Technology', 'yield': 0.8},
        'AAPL': {'name': 'Apple', 'sector': 'Technology', 'yield': 0.5},
        'UNH': {'name': 'UnitedHealth', 'sector': 'Healthcare', 'yield': 1.3},
        'CVX': {'name': 'Chevron', 'sector': 'Energy', 'yield': 3.5},
        'XOM': {'name': 'ExxonMobil', 'sector': 'Energy', 'yield': 3.8},
        'LMT': {'name': 'Lockheed Martin', 'sector': 'Defense', 'yield': 2.6},
        'RTX': {'name': 'RTX Corp', 'sector': 'Defense', 'yield': 2.4},
        'SO': {'name': 'Southern Company', 'sector': 'Utilities', 'yield': 4.5},
        'NEE': {'name': 'NextEra Energy', 'sector': 'Utilities', 'yield': 2.8},
        'AWK': {'name': 'American Water', 'sector': 'Utilities', 'yield': 1.8},
        'O': {'name': 'Realty Income', 'sector': 'REIT', 'yield': 3.8},
        'PLD': {'name': 'Prologis', 'sector': 'REIT', 'yield': 2.5},
        'DLR': {'name': 'Digital Realty', 'sector': 'REIT', 'yield': 3.5},
        'JEPI': {'name': 'JPMorgan Equity Premium Income', 'sector': 'ETF', 'yield': 10.0},
        'XYLD': {'name': 'Xylem Premium Income', 'sector': 'ETF', 'yield': 9.5},
    }
    
    @staticmethod
    def get_dividend_info(symbol):
        """
        ดึงข้อมูลปันผลของหุ้น
        
        Args:
            symbol: สัญลักษณ์หุ้น
        
        Returns:
            dict: ข้อมูลปันผล
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # ดึงข้อมูลปันผล
            dividend_yield = info.get('dividendYield', 0)
            dividend_per_share = info.get('trailingAnnualDividendPerShare', 0)
            last_dividend_date = info.get('lastDividendDate', None)
            
            # ดึงข้อมูลประวัติปันผล
            dividends = ticker.dividends
            
            result = {
                'symbol': symbol,
                'name': info.get('longName', 'Unknown'),
                'price': info.get('currentPrice', 0),
                'dividend_yield': dividend_yield if dividend_yield else 0,
                'dividend_per_share': dividend_per_share if dividend_per_share else 0,
                'last_dividend_date': last_dividend_date,
                'sector': info.get('sector', 'Unknown'),
                'industry': info.get('industry', 'Unknown'),
            }
            
            # คำนวณปันผลรายสัปดาห์และรายเดือน
            if len(dividends) > 0:
                recent_dividend = dividends.iloc[-1]
                result['latest_dividend'] = float(recent_dividend)
                result['latest_dividend_date'] = dividends.index[-1].strftime('%Y-%m-%d')
                
                # ประมาณปันผลรายสัปดาห์
                if result['dividend_per_share'] > 0:
                    result['weekly_dividend'] = result['dividend_per_share'] / 52
                    result['monthly_dividend'] = result['dividend_per_share'] / 12
                else:
                    result['weekly_dividend'] = 0
                    result['monthly_dividend'] = 0
            else:
                result['latest_dividend'] = 0
                result['latest_dividend_date'] = 'N/A'
                result['weekly_dividend'] = 0
                result['monthly_dividend'] = 0
            
            return result
            
        except Exception as e:
            logger.error(f"Error getting dividend info for {symbol}: {str(e)}")
            return None
    
    @staticmethod
    def find_high_dividend_stocks(min_yield=2.0, limit=20):
        """
        ค้นหาหุ้นปันผลสูง
        
        Args:
            min_yield: ผลตอบแทนขั้นต่ำ (%)
            limit: จำนวนหุ้นสูงสุด
        
        Returns:
            list: รายชื่อหุ้นปันผล
        """
        high_dividend_list = []
        
        for symbol, info in DividendAnalyzer.HIGH_DIVIDEND_STOCKS.items():
            try:
                dividend_info = DividendAnalyzer.get_dividend_info(symbol)
                
                if dividend_info and dividend_info['dividend_yield'] >= min_yield:
                    high_dividend_list.append({
                        'symbol': symbol,
                        'name': dividend_info['name'],
                        'price': dividend_info['price'],
                        'yield': dividend_info['dividend_yield'],
                        'annual_dividend': dividend_info['dividend_per_share'],
                        'weekly_dividend': dividend_info['weekly_dividend'],
                        'monthly_dividend': dividend_info['monthly_dividend'],
                        'sector': dividend_info['sector'],
                    })
            except:
                pass
        
        # เรียงลำดับตาม yield สูงสุด
        high_dividend_list.sort(key=lambda x: x['yield'], reverse=True)
        
        return high_dividend_list[:limit]
    
    @staticmethod
    def calculate_dividend_income(initial_investment, dividend_yield, period='yearly'):
        """
        คำนวณรายได้จากปันผล
        
        Args:
            initial_investment: เงินลงทุนเริ่มต้น
            dividend_yield: ผลตอบแทนปันผล (%)
            period: ระยะเวลา (yearly, monthly, weekly)
        
        Returns:
            float: รายได้จากปันผล
        """
        annual_income = initial_investment * (dividend_yield / 100)
        
        if period == 'yearly':
            return annual_income
        elif period == 'monthly':
            return annual_income / 12
        elif period == 'weekly':
            return annual_income / 52
        else:
            return annual_income
    
    @staticmethod
    def get_dividend_ranking():
        """
        จัดอันดับหุ้นปันผล
        
        Returns:
            dict: จัดอันดับ
        """
        ranking = {
            'very_high': [],  # > 5%
            'high': [],        # 3-5%
            'moderate': [],    # 2-3%
            'low': [],         # 1-2%
            'very_low': []     # < 1%
        }
        
        for symbol, info in DividendAnalyzer.HIGH_DIVIDEND_STOCKS.items():
            try:
                dividend_info = DividendAnalyzer.get_dividend_info(symbol)
                
                if dividend_info:
                    stock_data = {
                        'symbol': symbol,
                        'name': dividend_info['name'],
                        'yield': dividend_info['dividend_yield'],
                        'price': dividend_info['price'],
                    }
                    
                    yield_val = dividend_info['dividend_yield']
                    
                    if yield_val > 0.05:
                        ranking['very_high'].append(stock_data)
                    elif yield_val >= 0.03:
                        ranking['high'].append(stock_data)
                    elif yield_val >= 0.02:
                        ranking['moderate'].append(stock_data)
                    elif yield_val >= 0.01:
                        ranking['low'].append(stock_data)
                    else:
                        ranking['very_low'].append(stock_data)
            except:
                pass
        
        return ranking
    
    @staticmethod
    def format_dividend_display(dividend_info):
        """
        จัดรูปแบบการแสดงผลข้อมูลปันผล
        
        Args:
            dividend_info: ข้อมูลปันผล
        
        Returns:
            dict: ข้อมูลที่จัดรูปแบบแล้ว
        """
        return {
            'สัญลักษณ์': dividend_info.get('symbol', 'N/A'),
            'ชื่อบริษัท': dividend_info.get('name', 'N/A'),
            'ราคาปัจจุบัน': f"${dividend_info.get('price', 0):.2f}",
            'Dividend Yield (%)': f"{dividend_info.get('dividend_yield', 0)*100:.2f}%",
            'ปันผลรายปี': f"${dividend_info.get('dividend_per_share', 0):.2f}",
            'ปันผลรายเดือน': f"${dividend_info.get('monthly_dividend', 0):.3f}",
            'ปันผลรายสัปดาห์': f"${dividend_info.get('weekly_dividend', 0):.3f}",
            'ส่วนชั้น': dividend_info.get('sector', 'N/A'),
        }


if __name__ == "__main__":
    analyzer = DividendAnalyzer()
    
    # ค้นหาหุ้นปันผลสูง
    print("\n🎯 หุ้นปันผลสูง (> 2%):")
    high_dividend = analyzer.find_high_dividend_stocks(min_yield=2.0, limit=10)
    for stock in high_dividend:
        print(f"{stock['symbol']:6} | {stock['name']:30} | Yield: {stock['yield']*100:5.2f}% | Weekly: ${stock['weekly_dividend']:.3f}")
    
    # ข้อมูลสำหรับหุ้นเดียว
    print("\n📊 ข้อมูล T (AT&T):")
    t_info = analyzer.get_dividend_info('T')
    if t_info:
        formatted = analyzer.format_dividend_display(t_info)
        for key, value in formatted.items():
            print(f"{key:20}: {value}")
