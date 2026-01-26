"""
Backtesting Module
ระบบทดสอบกลยุทธ์การเทรดกับข้อมูลในอดีต
"""

from .backtester import Backtester
from .metrics import PerformanceMetrics

__all__ = ['Backtester', 'PerformanceMetrics']
