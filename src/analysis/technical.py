"""
Stock Analyzer - Technical Analysis Module
ใช้ Technical Indicators เช่น SMA, RSI, MACD, Bollinger Bands
"""

import numpy as np
import pandas as pd
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalAnalyzer:
    """วิเคราะห์ทางเทคนิคโดยใช้ Indicators"""
    
    @staticmethod
    def calculate_sma(data, window=20):
        """
        Simple Moving Average (SMA)
        
        Args:
            data: Series ของราคาปิด
            window: ช่วงวันสำหรับคำนวณ
        
        Returns:
            Series: SMA values
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None
        try:
            return data['Close'].rolling(window=window).mean()
        except Exception as e:
            logger.error(f"Error calculating SMA: {str(e)}")
            return None
    
    @staticmethod
    def calculate_ema(data, window=12):
        """
        Exponential Moving Average (EMA)
        
        Args:
            data: DataFrame ของราคาหุ้น
            window: ช่วงวันสำหรับคำนวณ
        
        Returns:
            Series: EMA values
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None
        try:
            return data['Close'].ewm(span=window, adjust=False).mean()
        except Exception as e:
            logger.error(f"Error calculating EMA: {str(e)}")
            return None
    
    @staticmethod
    def calculate_rsi(data, window=14):
        """
        Relative Strength Index (RSI)
        ตัวบ่งชี้ Momentum 0-100
        - < 30: Oversold (ซื้อขาด)
        - > 70: Overbought (ขายเกิน)
        
        Args:
            data: DataFrame ของราคาหุ้น
            window: ช่วงวันสำหรับคำนวณ
        
        Returns:
            Series: RSI values
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None
        try:
            close = data['Close']
            delta = close.diff()
            
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return None
    
    @staticmethod
    def calculate_macd(data, fast=12, slow=26, signal=9):
        """
        MACD (Moving Average Convergence Divergence)
        สัญญาณความเร็วและการเปลี่ยนแปลงของแนวโน้ม
        
        Args:
            data: DataFrame ของราคาหุ้น
            fast: ช่วงเร็ว
            slow: ช่วงช้า
            signal: ช่วง Signal line
        
        Returns:
            tuple: (MACD, Signal, Histogram)
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None, None, None
        try:
            close = data['Close']
            
            ema_fast = close.ewm(span=fast, adjust=False).mean()
            ema_slow = close.ewm(span=slow, adjust=False).mean()
            
            macd = ema_fast - ema_slow
            signal = macd.ewm(span=signal, adjust=False).mean()
            histogram = macd - signal
            
            return macd, signal, histogram
        except Exception as e:
            logger.error(f"Error calculating MACD: {str(e)}")
            return None, None, None
    
    @staticmethod
    def calculate_bollinger_bands(data, window=20, num_std=2):
        """
        Bollinger Bands
        ตัวบ่งชี้ความผันผวน
        
        Args:
            data: DataFrame ของราคาหุ้น
            window: ช่วงวันสำหรับคำนวณ
            num_std: จำนวน Standard Deviation
        
        Returns:
            dict: upper band, middle band, lower band
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None
        try:
            close = data['Close']
            
            middle = close.rolling(window=window).mean()
            std = close.rolling(window=window).std()
            
            upper = middle + (std * num_std)
            lower = middle - (std * num_std)
            
            return {
                'upper': upper,
                'middle': middle,
                'lower': lower
            }
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {str(e)}")
            return None
    
    @staticmethod
    def calculate_atr(data, window=14):
        """
        Average True Range (ATR)
        วัดความผันผวนของราคา
        
        Args:
            data: DataFrame ของราคาหุ้น
            window: ช่วงวันสำหรับคำนวณ
        
        Returns:
            Series: ATR values
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=window).mean()
            
            return atr
        except Exception as e:
            logger.error(f"Error calculating ATR: {str(e)}")
            return None
    
    @staticmethod
    def calculate_stochastic(data, window=14, smooth_k=3, smooth_d=3):
        """
        Stochastic Oscillator
        ตัวบ่งชี้ Momentum
        
        Args:
            data: DataFrame ของราคาหุ้น
            window: ช่วงวันสำหรับคำนวณ
            smooth_k: Smoothing K
            smooth_d: Smoothing D
        
        Returns:
            dict: k_line, d_line
        """
        if data is None or (hasattr(data, 'empty') and data.empty):
            return None
        try:
            close = data['Close']
            high = data['High']
            low = data['Low']
            
            lowest_low = low.rolling(window=window).min()
            highest_high = high.rolling(window=window).max()
            
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            k_line = k_percent.rolling(window=smooth_k).mean()
            d_line = k_line.rolling(window=smooth_d).mean()
            
            return {
                'k_line': k_line,
                'd_line': d_line
            }
        except Exception as e:
            logger.error(f"Error calculating Stochastic: {str(e)}")
            return None
    
    @staticmethod
    def get_technical_summary(data):
        """
        สรุปผลการวิเคราะห์ทางเทคนิค
        
        Args:
            data: DataFrame ของราคาหุ้น
        
        Returns:
            dict: สรุปผล
        """
        # Handle None or empty data
        if data is None or data.empty:
            logger.warning("Data is None or empty, returning default summary")
            return {
                'latest_price': 0,
                'sma_20': 0,
                'sma_50': 0,
                'sma_200': 0,
                'rsi': 50,
                'macd': 0,
                'macd_signal': 0,
                'macd_histogram': 0,
                'bb_upper': 0,
                'bb_middle': 0,
                'bb_lower': 0,
                'atr': 0,
                'stoch_k': 50,
                'stoch_d': 50,
            }
        
        analyzer = TechnicalAnalyzer()
        
        try:
            sma_20 = analyzer.calculate_sma(data, 20)
            sma_50 = analyzer.calculate_sma(data, 50)
            sma_200 = analyzer.calculate_sma(data, 200)
            rsi = analyzer.calculate_rsi(data)
            macd, signal, hist = analyzer.calculate_macd(data)
            bb = analyzer.calculate_bollinger_bands(data)
            atr = analyzer.calculate_atr(data)
            stoch = analyzer.calculate_stochastic(data)
            
            latest_price = data['Close'].iloc[-1]
            
            # Safe access to potentially None values
            sma_20_val = sma_20.iloc[-1] if sma_20 is not None else 0
            sma_50_val = sma_50.iloc[-1] if sma_50 is not None else 0
            sma_200_val = sma_200.iloc[-1] if sma_200 is not None else 0
            rsi_val = rsi.iloc[-1] if rsi is not None else 50
            macd_val = macd.iloc[-1] if macd is not None else 0
            signal_val = signal.iloc[-1] if signal is not None else 0
            hist_val = hist.iloc[-1] if hist is not None else 0
            bb_upper_val = bb['upper'].iloc[-1] if bb is not None and 'upper' in bb else 0
            bb_middle_val = bb['middle'].iloc[-1] if bb is not None and 'middle' in bb else 0
            bb_lower_val = bb['lower'].iloc[-1] if bb is not None and 'lower' in bb else 0
            atr_val = atr.iloc[-1] if atr is not None else 0
            stoch_k_val = stoch['k_line'].iloc[-1] if stoch is not None and 'k_line' in stoch else 50
            stoch_d_val = stoch['d_line'].iloc[-1] if stoch is not None and 'd_line' in stoch else 50
            
            return {
                'latest_price': latest_price,
                'sma_20': sma_20_val,
                'sma_50': sma_50_val,
                'sma_200': sma_200_val,
                'rsi': rsi_val,
                'macd': macd_val,
                'macd_signal': signal_val,
                'macd_histogram': hist_val,
                'bb_upper': bb_upper_val,
                'bb_middle': bb_middle_val,
                'bb_lower': bb_lower_val,
                'atr': atr_val,
                'stoch_k': stoch_k_val,
                'stoch_d': stoch_d_val,
            }
        except Exception as e:
            logger.error(f"Error getting technical summary: {str(e)}")
            return {
                'latest_price': 0,
                'sma_20': 0,
                'sma_50': 0,
                'sma_200': 0,
                'rsi': 50,
                'macd': 0,
                'macd_signal': 0,
                'macd_histogram': 0,
                'bb_upper': 0,
                'bb_middle': 0,
                'bb_lower': 0,
                'atr': 0,
                'stoch_k': 50,
                'stoch_d': 50,
            }
