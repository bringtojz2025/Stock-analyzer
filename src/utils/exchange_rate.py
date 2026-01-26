"""
Exchange Rate Fetcher
ดึงอัตราแลกเปลี่ยนแบบ Real-time
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ExchangeRateFetcher:
    """ดึงอัตราแลกเปลี่ยน USD to THB แบบ Real-time"""
    
    def __init__(self):
        """Initialize Exchange Rate Fetcher"""
        self.cache = {}
        self.default_rate = 35.5  # ค่าเริ่มต้นถ้าดึงไม่ได้
    
    def get_usd_to_thb(self) -> float:
        """
        ดึงอัตราแลกเปลี่ยน USD to THB แบบ Real-time
        
        Returns:
            float: อัตราแลกเปลี่ยน (THB per USD)
        """
        # Method 1: Try exchangerate-api.com (Free API)
        try:
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                rate = data.get('rates', {}).get('THB')
                
                if rate:
                    logger.info(f"Fetched USD/THB rate: {rate:.2f}")
                    self.cache['usd_thb'] = rate
                    return rate
        except Exception as e:
            logger.warning(f"Failed to fetch from exchangerate-api: {e}")
        
        # Method 2: Try currencyapi.com (Alternative)
        try:
            url = "https://api.currencyapi.com/v3/latest"
            params = {
                'apikey': 'cur_live_free',  # Free tier
                'base_currency': 'USD',
                'currencies': 'THB'
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                rate = data.get('data', {}).get('THB', {}).get('value')
                
                if rate:
                    logger.info(f"Fetched USD/THB rate: {rate:.2f}")
                    self.cache['usd_thb'] = rate
                    return rate
        except Exception as e:
            logger.warning(f"Failed to fetch from currencyapi: {e}")
        
        # Method 3: Try fixer.io API
        try:
            url = "https://api.fixer.io/latest"
            params = {
                'base': 'USD',
                'symbols': 'THB'
            }
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                rate = data.get('rates', {}).get('THB')
                
                if rate:
                    logger.info(f"Fetched USD/THB rate: {rate:.2f}")
                    self.cache['usd_thb'] = rate
                    return rate
        except Exception as e:
            logger.warning(f"Failed to fetch from fixer.io: {e}")
        
        # Fallback: Use cached value or default
        if 'usd_thb' in self.cache:
            logger.info(f"Using cached USD/THB rate: {self.cache['usd_thb']:.2f}")
            return self.cache['usd_thb']
        
        logger.warning(f"Using default USD/THB rate: {self.default_rate:.2f}")
        return self.default_rate
    
    def get_rate_with_source(self) -> dict:
        """
        ดึงอัตราแลกเปลี่ยนพร้อมแหล่งที่มา
        
        Returns:
            dict: {'rate': float, 'source': str, 'timestamp': str}
        """
        from datetime import datetime
        
        rate = self.get_usd_to_thb()
        
        result = {
            'rate': rate,
            'source': 'Real-time API' if rate != self.default_rate else 'Default',
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_live': rate != self.default_rate
        }
        
        return result
    
    def format_rate(self, rate: float) -> str:
        """
        Format อัตราแลกเปลี่ยนสำหรับแสดงผล
        
        Args:
            rate: อัตราแลกเปลี่ยน
            
        Returns:
            str: Formatted rate
        """
        return f"฿{rate:.2f}/USD"
