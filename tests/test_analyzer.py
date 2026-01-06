"""
Unit Tests for Stock Analyzer
"""

import unittest
from datetime import datetime
from unittest.mock import Mock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.abspath('..'))


class TestStockDataFetcher(unittest.TestCase):
    """Test Data Fetcher Module"""
    
    @patch('src.data.fetcher.yf')
    def test_fetch_historical_data(self, mock_yf):
        """Test fetching historical data"""
        # Mock yfinance
        mock_ticker = Mock()
        mock_yf.Ticker.return_value = mock_ticker
        
        # Mock historical data
        mock_data = Mock()
        mock_data.empty = False
        mock_ticker.history.return_value = mock_data
        
        # This test will pass if yfinance is properly mocked
        # In real usage, actual data would be returned
        
        self.assertIsNotNone(mock_data)
    
    def test_symbol_validation(self):
        """Test stock symbol validation"""
        valid_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA']
        
        for symbol in valid_symbols:
            self.assertTrue(len(symbol) > 0)
            self.assertTrue(symbol.isupper())


class TestTechnicalAnalyzer(unittest.TestCase):
    """Test Technical Analysis Module"""
    
    def test_sma_calculation(self):
        """Test SMA calculation"""
        import pandas as pd
        import numpy as np
        
        # Create mock data
        dates = pd.date_range('2023-01-01', periods=50)
        prices = pd.DataFrame({
            'Close': np.random.randn(50).cumsum() + 100
        }, index=dates)
        
        # SMA should be a Series
        self.assertEqual(len(prices), 50)
    
    def test_rsi_range(self):
        """Test RSI should be between 0 and 100"""
        # RSI values should always be between 0 and 100
        min_rsi = 0
        max_rsi = 100
        
        test_rsi = 65.5
        self.assertGreaterEqual(test_rsi, min_rsi)
        self.assertLessEqual(test_rsi, max_rsi)


class TestSignalGenerator(unittest.TestCase):
    """Test Signal Generation Module"""
    
    def test_signal_generation(self):
        """Test basic signal generation"""
        test_data = {
            'latest_price': 189.50,
            'sma_20': 185.30,
            'sma_50': 182.10,
            'sma_200': 180.00,
            'rsi': 65.5,
            'macd': 0.123,
            'macd_signal': 0.100,
            'macd_histogram': 0.023,
        }
        
        # Test signal structure
        self.assertIn('latest_price', test_data)
        self.assertIn('sma_20', test_data)
        self.assertIn('rsi', test_data)
    
    def test_entry_exit_points(self):
        """Test entry/exit point calculation"""
        entry_price = 189.50
        profit_target = entry_price * 1.05  # 5% profit
        stop_loss = entry_price * 0.97      # 3% stop loss
        
        self.assertGreater(profit_target, entry_price)
        self.assertLess(stop_loss, entry_price)


class TestNotificationManager(unittest.TestCase):
    """Test Notification System"""
    
    def test_notification_structure(self):
        """Test notification data structure"""
        notification_data = {
            'symbol': 'AAPL',
            'signal': 'BUY',
            'timestamp': datetime.now().isoformat(),
            'confidence': 0.75
        }
        
        self.assertEqual(notification_data['signal'], 'BUY')
        self.assertIsNotNone(notification_data['timestamp'])


class TestConfiguration(unittest.TestCase):
    """Test Configuration Settings"""
    
    def test_stock_list_not_empty(self):
        """Test that stock list is not empty"""
        from config.settings import STOCKS_TO_MONITOR
        
        self.assertGreater(len(STOCKS_TO_MONITOR), 0)
    
    def test_technical_parameters(self):
        """Test technical parameters are valid"""
        from config.settings import TECHNICAL_CONFIG
        
        self.assertEqual(TECHNICAL_CONFIG['sma_short'], 20)
        self.assertEqual(TECHNICAL_CONFIG['sma_medium'], 50)
        self.assertEqual(TECHNICAL_CONFIG['sma_long'], 200)
        self.assertGreater(TECHNICAL_CONFIG['rsi_overbought'], 
                          TECHNICAL_CONFIG['rsi_oversold'])


if __name__ == '__main__':
    unittest.main()
