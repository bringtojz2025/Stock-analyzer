"""
Stock Analyzer - Data Fetcher Module
ดึงข้อมูลหุ้นจากแหล่งต่างๆ เช่น Yahoo Finance, Alpha Vantage
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDataFetcher:
    """ดึงข้อมูลหุ้นจาก Yahoo Finance"""
    
    def __init__(self):
        self.data_cache = {}
    
    def fetch_historical_data(self, symbol, period='1y', interval='1d'):
        """
        ดึงข้อมูลประวัติราคาหุ้น
        
        Args:
            symbol: สัญลักษณ์หุ้น (เช่น 'AAPL', 'MSFT')
            period: ระยะเวลา (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: ช่วงเวลา (1m, 5m, 15m, 30m, 60m, 1d, 1wk, 1mo)
        
        Returns:
            DataFrame: ข้อมูลราคาหุ้น
        """
        try:
            logger.info(f"Fetching data for {symbol} with period {period}...")
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return None
            
            self.data_cache[symbol] = data
            logger.info(f"Successfully fetched {len(data)} records for {symbol}")
            return data
        
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def fetch_stock_info(self, symbol):
        """
        ดึงข้อมูลพื้นฐานของหุ้น
        
        Args:
            symbol: สัญลักษณ์หุ้น
        
        Returns:
            dict: ข้อมูลพื้นฐาน
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Handle None or invalid info
            if info is None or not isinstance(info, dict):
                logger.warning(f"No valid info found for {symbol}")
                return {}
            
            return info
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return {}
    
    def fetch_multiple_stocks(self, symbols, period='1y'):
        """
        ดึงข้อมูลหุ้นหลายตัว
        
        Args:
            symbols: รายชื่อสัญลักษณ์หุ้น
            period: ระยะเวลา
        
        Returns:
            dict: ข้อมูลหุ้นทั้งหมด
        """
        data = {}
        for symbol in symbols:
            data[symbol] = self.fetch_historical_data(symbol, period=period)
        return data
    
    def get_latest_price(self, symbol):
        """ดึงราคาล่าสุด"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period='1d')
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            logger.error(f"Error getting latest price for {symbol}: {str(e)}")
            return None
    
    def get_realtime_data(self, symbols):
        """ดึงข้อมูลราคาปัจจุบัน"""
        try:
            data = yf.download(symbols, period='1d', progress=False)
            return data
        except Exception as e:
            logger.error(f"Error fetching realtime data: {str(e)}")
            return None


class FundamentalAnalyzer:
    """วิเคราะห์ข้อมูลพื้นฐานของบริษัท"""
    
    @staticmethod
    def analyze_valuation(symbol):
        """วิเคราะห์มูลค่า"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Handle None or invalid info
            if info is None or not isinstance(info, dict):
                logger.warning(f"No valid info for {symbol}, returning default")
                return {
                    'symbol': symbol,
                    'pe_ratio': 'N/A',
                    'forward_pe': 'N/A',
                    'peg_ratio': 'N/A',
                    'price_to_book': 'N/A',
                    'pb_ratio': 'N/A',
                    'dividend_yield': 'N/A',
                    'market_cap': 'N/A',
                    'enterprise_value': 'N/A',
                }
            
            valuation = {
                'symbol': symbol,
                'pe_ratio': info.get('trailingPE', 'N/A'),
                'forward_pe': info.get('forwardPE', 'N/A'),
                'peg_ratio': info.get('pegRatio', 'N/A'),
                'price_to_book': info.get('priceToBook', 'N/A'),
                'pb_ratio': info.get('priceToBook', 'N/A'),
                'dividend_yield': info.get('dividendYield', 'N/A'),
                'market_cap': info.get('marketCap', 'N/A'),
                'enterprise_value': info.get('enterpriseValue', 'N/A'),
            }
            return valuation
        except Exception as e:
            logger.error(f"Error analyzing valuation for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'pe_ratio': 'N/A',
                'forward_pe': 'N/A',
                'peg_ratio': 'N/A',
                'price_to_book': 'N/A',
                'pb_ratio': 'N/A',
                'dividend_yield': 'N/A',
                'market_cap': 'N/A',
                'enterprise_value': 'N/A',
            }
    
    @staticmethod
    def analyze_financial_health(symbol):
        """วิเคราะห์สุขภาพทางการเงิน"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Handle None or invalid info
            if info is None or not isinstance(info, dict):
                logger.warning(f"No valid info for {symbol}, returning default")
                return {
                    'symbol': symbol,
                    'debt_to_equity': 'N/A',
                    'current_ratio': 'N/A',
                    'quick_ratio': 'N/A',
                    'profit_margin': 'N/A',
                    'return_on_equity': 'N/A',
                    'return_on_assets': 'N/A',
                    'revenue_growth': 'N/A',
                }
            
            health = {
                'symbol': symbol,
                'debt_to_equity': info.get('debtToEquity', 'N/A'),
                'current_ratio': info.get('currentRatio', 'N/A'),
                'quick_ratio': info.get('quickRatio', 'N/A'),
                'profit_margin': info.get('profitMargins', 'N/A'),
                'return_on_equity': info.get('returnOnEquity', 'N/A'),
                'return_on_assets': info.get('returnOnAssets', 'N/A'),
                'revenue_growth': info.get('revenueGrowth', 'N/A'),
            }
            return health
        except Exception as e:
            logger.error(f"Error analyzing financial health for {symbol}: {str(e)}")
            return {
                'symbol': symbol,
                'debt_to_equity': 'N/A',
                'current_ratio': 'N/A',
                'quick_ratio': 'N/A',
                'profit_margin': 'N/A',
                'return_on_equity': 'N/A',
                'return_on_assets': 'N/A',
                'revenue_growth': 'N/A',
            }
