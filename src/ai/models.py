"""
Advanced AI Models for Stock Analysis
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PricePredictor:
    """ทำนายราคาหุ้น"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
    
    def train(self, X_train, y_train):
        """ฝึก Price Prediction Model"""
        try:
            self.model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
            X_scaled = self.scaler.fit_transform(X_train)
            self.model.fit(X_scaled, y_train)
            logger.info("Price predictor trained")
        except Exception as e:
            logger.error(f"Error training price predictor: {str(e)}")
    
    def predict(self, X):
        """ทำนายราคา"""
        if self.model is None:
            return None
        
        try:
            X_scaled = self.scaler.transform(X)
            return self.model.predict(X_scaled)
        except Exception as e:
            logger.error(f"Error predicting price: {str(e)}")
            return None


class SignalClassifier:
    """ใช้ Machine Learning แบบ Gradient Boosting เพื่อ classify signals"""
    
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
    
    def train(self, X_train, y_train):
        """ฝึก Signal Classifier Model"""
        try:
            self.model = GradientBoostingClassifier(
                n_estimators=200,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            )
            X_scaled = self.scaler.fit_transform(X_train)
            self.model.fit(X_scaled, y_train)
            logger.info("Signal classifier trained")
        except Exception as e:
            logger.error(f"Error training signal classifier: {str(e)}")
    
    def predict(self, X):
        """Classify signal"""
        if self.model is None:
            return None
        
        try:
            X_scaled = self.scaler.transform(X)
            predictions = self.model.predict(X_scaled)
            probabilities = self.model.predict_proba(X_scaled)
            
            return {
                'prediction': predictions,
                'probabilities': probabilities,
                'confidence': np.max(probabilities, axis=1)
            }
        except Exception as e:
            logger.error(f"Error predicting signal: {str(e)}")
            return None


class AnomalyDetector:
    """ตรวจจับ Anomalies ในราคาหรือ Trading pattern"""
    
    @staticmethod
    def detect_price_anomalies(data, window=20, threshold=2.0):
        """ตรวจจับราคาที่ผิดปกติ"""
        close = data['Close']
        
        # Calculate rolling mean and std
        rolling_mean = close.rolling(window=window).mean()
        rolling_std = close.rolling(window=window).std()
        
        # Z-score
        z_scores = np.abs((close - rolling_mean) / rolling_std)
        
        anomalies = z_scores > threshold
        
        return anomalies
    
    @staticmethod
    def detect_volume_anomalies(data, window=20, threshold=2.0):
        """ตรวจจับปริมาณการซื้อขายที่ผิดปกติ"""
        volume = data['Volume']
        
        # Calculate rolling mean and std
        rolling_mean = volume.rolling(window=window).mean()
        rolling_std = volume.rolling(window=window).std()
        
        # Z-score
        z_scores = np.abs((volume - rolling_mean) / rolling_std)
        
        anomalies = z_scores > threshold
        
        return anomalies


class CorrelationAnalyzer:
    """วิเคราะห์ความสัมพันธ์ระหว่างหุ้นต่างๆ"""
    
    @staticmethod
    def calculate_correlation_matrix(price_data):
        """คำนวณ Correlation Matrix"""
        returns = price_data.pct_change()
        correlation = returns.corr()
        
        return correlation
    
    @staticmethod
    def find_correlated_stocks(correlation_matrix, reference_stock, threshold=0.7):
        """หาหุ้นที่เกี่ยวข้องกับหุ้นอ้างอิง"""
        if reference_stock not in correlation_matrix.columns:
            return []
        
        corr_with_reference = correlation_matrix[reference_stock]
        corr_with_reference = corr_with_reference.drop(reference_stock)
        
        highly_correlated = corr_with_reference[
            np.abs(corr_with_reference) > threshold
        ]
        
        return highly_correlated.sort_values(ascending=False)
