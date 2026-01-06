"""
Stock Analyzer - AI Signal Generator
ใช้ Machine Learning หรือ Rule-based engine เพื่อสร้าง Buy/Sell signals
"""

import numpy as np
import pandas as pd
from datetime import datetime
import logging
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SignalGenerator:
    """สร้างสัญญาณซื้อ/ขายโดยใช้ Rule-based logic"""
    
    def __init__(self):
        self.buy_signals = []
        self.sell_signals = []
    
    def generate_signals_from_indicators(self, technical_data):
        """
        สร้างสัญญาณจาก Technical Indicators
        
        Args:
            technical_data: dict ที่มี SMA, RSI, MACD เป็นต้น
        
        Returns:
            dict: Buy/Sell signals
        """
        signals = {
            'buy': 0,
            'sell': 0,
            'hold': 0,
            'confidence': 0.0,
            'reasons': []
        }
        
        price = technical_data.get('latest_price', 0)
        sma_20 = technical_data.get('sma_20', 0)
        sma_50 = technical_data.get('sma_50', 0)
        sma_200 = technical_data.get('sma_200', 0)
        rsi = technical_data.get('rsi', 50)
        macd = technical_data.get('macd', 0)
        macd_signal = technical_data.get('macd_signal', 0)
        macd_hist = technical_data.get('macd_histogram', 0)
        
        buy_score = 0
        sell_score = 0
        
        # SMA Cross Over Analysis
        if sma_20 > sma_50 > sma_200:
            buy_score += 2
            signals['reasons'].append("Golden Cross (SMA 20 > 50 > 200)")
        elif sma_20 < sma_50 < sma_200:
            sell_score += 2
            signals['reasons'].append("Death Cross (SMA 20 < 50 < 200)")
        
        # RSI Analysis
        if rsi < 30:
            buy_score += 2
            signals['reasons'].append(f"RSI Oversold ({rsi:.2f})")
        elif rsi > 70:
            sell_score += 2
            signals['reasons'].append(f"RSI Overbought ({rsi:.2f})")
        
        # MACD Analysis
        if macd > macd_signal and macd_hist > 0:
            buy_score += 1.5
            signals['reasons'].append("MACD Bullish")
        elif macd < macd_signal and macd_hist < 0:
            sell_score += 1.5
            signals['reasons'].append("MACD Bearish")
        
        # Price vs SMA
        if price > sma_50 and price > sma_200:
            buy_score += 1
            signals['reasons'].append("Price above MA50 and MA200")
        elif price < sma_50 and price < sma_200:
            sell_score += 1
            signals['reasons'].append("Price below MA50 and MA200")
        
        # Determine signal
        total_score = buy_score + sell_score
        if total_score > 0:
            signals['confidence'] = (max(buy_score, sell_score) / total_score)
        
        if buy_score > sell_score:
            signals['buy'] = 1
            signals['hold'] = 0
            signals['sell'] = 0
        elif sell_score > buy_score:
            signals['sell'] = 1
            signals['hold'] = 0
            signals['buy'] = 0
        else:
            signals['hold'] = 1
            signals['buy'] = 0
            signals['sell'] = 0
        
        return signals
    
    def generate_entry_exit_points(self, data):
        """
        สร้างจุดเข้า-ออก (Entry/Exit points)
        
        Args:
            data: DataFrame ของราคาหุ้น
        
        Returns:
            dict: entry price, exit price, stop loss
        """
        # Handle None or empty data
        if data is None or (hasattr(data, 'empty') and data.empty):
            logger.warning("Data is None or empty in generate_entry_exit_points, returning defaults")
            return {
                'entry_price': 0,
                'target_price': 0,
                'stop_loss': 0,
                'bb_upper': 0,
                'bb_lower': 0,
                'atr': 0
            }
        
        from src.analysis.technical import TechnicalAnalyzer
        
        analyzer = TechnicalAnalyzer()
        
        try:
            # Calculate indicators
            atr = analyzer.calculate_atr(data)
            bb = analyzer.calculate_bollinger_bands(data)
            sma_20 = analyzer.calculate_sma(data, 20)
            sma_50 = analyzer.calculate_sma(data, 50)
            
            latest_price = data['Close'].iloc[-1]
            latest_atr = atr.iloc[-1] if atr is not None and not atr.empty else 0
            bb_lower = bb['lower'].iloc[-1] if bb is not None and not bb.empty else 0
            bb_upper = bb['upper'].iloc[-1] if bb is not None and not bb.empty else 0
            
            return {
                'entry_price': latest_price,
                'target_price': latest_price * 1.05,  # 5% profit target
                'stop_loss': latest_price * 0.97,     # 3% stop loss
                'bb_upper': bb_upper,
                'bb_lower': bb_lower,
                'atr': latest_atr
            }
        except Exception as e:
            logger.error(f"Error in generate_entry_exit_points: {str(e)}")
            return {
                'entry_price': 0,
                'target_price': 0,
                'stop_loss': 0,
                'bb_upper': 0,
                'bb_lower': 0,
                'atr': 0
            }


class AISignalGenerator:
    """สร้างสัญญาณโดยใช้ Machine Learning"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.trained = False
    
    def prepare_features(self, technical_data):
        """เตรียม Features สำหรับ ML Model"""
        features = np.array([
            technical_data.get('sma_20', 0),
            technical_data.get('sma_50', 0),
            technical_data.get('sma_200', 0),
            technical_data.get('rsi', 50),
            technical_data.get('macd', 0),
            technical_data.get('macd_signal', 0),
            technical_data.get('macd_histogram', 0),
            technical_data.get('atr', 0),
            technical_data.get('stoch_k', 50),
            technical_data.get('stoch_d', 50),
        ]).reshape(1, -1)
        
        return features
    
    def train_model(self, X_train, y_train):
        """
        ฝึก Random Forest Model
        
        Args:
            X_train: Feature array
            y_train: Label array (0: sell, 1: hold, 2: buy)
        """
        try:
            self.model = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
            X_scaled = self.scaler.fit_transform(X_train)
            self.model.fit(X_scaled, y_train)
            self.trained = True
            logger.info("AI Model trained successfully")
        except Exception as e:
            logger.error(f"Error training model: {str(e)}")
    
    def predict_signal(self, technical_data):
        """
        ทำนาย Signal จาก Technical Data
        
        Args:
            technical_data: dict ของ indicators
        
        Returns:
            dict: prediction result
        """
        if not self.trained:
            return {'error': 'Model not trained yet'}
        
        try:
            features = self.prepare_features(technical_data)
            X_scaled = self.scaler.transform(features)
            
            prediction = self.model.predict(X_scaled)[0]
            probability = self.model.predict_proba(X_scaled)[0]
            
            signal_map = {0: 'SELL', 1: 'HOLD', 2: 'BUY'}
            
            return {
                'signal': signal_map[prediction],
                'confidence': float(probability[prediction]),
                'probabilities': {
                    'sell': float(probability[0]),
                    'hold': float(probability[1]),
                    'buy': float(probability[2])
                }
            }
        except Exception as e:
            logger.error(f"Error predicting signal: {str(e)}")
            return {'error': str(e)}
