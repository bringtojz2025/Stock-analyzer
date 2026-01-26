"""
Performance Metrics Calculator
คำนวณ metrics ทางสถิติสำหรับ backtesting
"""

import numpy as np
import pandas as pd
from typing import List


class PerformanceMetrics:
    """คำนวณ performance metrics สำหรับ backtesting"""
    
    @staticmethod
    def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
        """
        คำนวณ Sharpe Ratio
        
        Args:
            returns: Series ของ returns
            risk_free_rate: อัตราดอกเบี้ยปลอดความเสี่ยง (default 2%)
            
        Returns:
            float: Sharpe Ratio
        """
        if len(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)  # daily risk-free rate
        
        if excess_returns.std() == 0:
            return 0
        
        sharpe = np.sqrt(252) * (excess_returns.mean() / excess_returns.std())
        return sharpe
    
    @staticmethod
    def calculate_sortino_ratio(returns, risk_free_rate=0.02):
        """
        คำนวณ Sortino Ratio (เหมือน Sharpe แต่ใช้ downside deviation)
        
        Args:
            returns: Series ของ returns
            risk_free_rate: อัตราดอกเบี้ยปลอดความเสี่ยง
            
        Returns:
            float: Sortino Ratio
        """
        if len(returns) == 0:
            return 0
        
        excess_returns = returns - (risk_free_rate / 252)
        downside_returns = returns[returns < 0]
        
        if len(downside_returns) == 0 or downside_returns.std() == 0:
            return 0
        
        sortino = np.sqrt(252) * (excess_returns.mean() / downside_returns.std())
        return sortino
    
    @staticmethod
    def calculate_max_drawdown(equity_curve):
        """
        คำนวณ Maximum Drawdown
        
        Args:
            equity_curve: Series ของมูลค่า portfolio
            
        Returns:
            tuple: (max_drawdown_pct, max_drawdown_duration_days)
        """
        if len(equity_curve) == 0:
            return 0, 0
        
        # คำนวณ running maximum
        running_max = equity_curve.cummax()
        
        # คำนวณ drawdown
        drawdown = (equity_curve - running_max) / running_max * 100
        max_drawdown = drawdown.min()
        
        # คำนวณ duration
        in_drawdown = False
        drawdown_start = 0
        max_duration = 0
        current_duration = 0
        
        for i, dd in enumerate(drawdown):
            if dd < 0 and not in_drawdown:
                in_drawdown = True
                drawdown_start = i
            elif dd == 0 and in_drawdown:
                in_drawdown = False
                current_duration = i - drawdown_start
                if current_duration > max_duration:
                    max_duration = current_duration
        
        return abs(max_drawdown), max_duration
    
    @staticmethod
    def calculate_calmar_ratio(total_return, max_drawdown, years=1.0):
        """
        คำนวณ Calmar Ratio = Annual Return / Max Drawdown
        
        Args:
            total_return: Total return (%)
            max_drawdown: Maximum drawdown (%)
            years: จำนวนปี
            
        Returns:
            float: Calmar Ratio
        """
        if max_drawdown == 0:
            return 0
        
        annual_return = total_return / years
        return annual_return / abs(max_drawdown)
    
    @staticmethod
    def calculate_win_loss_ratio(wins, losses):
        """
        คำนวณ Win/Loss Ratio
        
        Args:
            wins: จำนวนการชนะ
            losses: จำนวนการแพ้
            
        Returns:
            float: Win/Loss Ratio
        """
        if losses == 0:
            return float('inf') if wins > 0 else 0
        return wins / losses
    
    @staticmethod
    def calculate_profit_factor(gross_profit, gross_loss):
        """
        คำนวณ Profit Factor = Gross Profit / Gross Loss
        
        Args:
            gross_profit: กำไรรวม
            gross_loss: ขาดทุนรวม
            
        Returns:
            float: Profit Factor
        """
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0
        return abs(gross_profit / gross_loss)
    
    @staticmethod
    def calculate_expectancy(win_rate, avg_win, avg_loss):
        """
        คำนวณ Expectancy = (Win Rate × Avg Win) - (Loss Rate × Avg Loss)
        
        Args:
            win_rate: อัตราการชนะ (0-1)
            avg_win: กำไรเฉลี่ย
            avg_loss: ขาดทุนเฉลี่ย
            
        Returns:
            float: Expectancy
        """
        loss_rate = 1 - win_rate
        return (win_rate * avg_win) - (loss_rate * abs(avg_loss))
    
    @staticmethod
    def calculate_alpha_beta(portfolio_returns, benchmark_returns):
        """
        คำนวณ Alpha และ Beta
        
        Args:
            portfolio_returns: Series ของ portfolio returns
            benchmark_returns: Series ของ benchmark returns (เช่น S&P 500)
            
        Returns:
            tuple: (alpha, beta)
        """
        if len(portfolio_returns) == 0 or len(benchmark_returns) == 0:
            return 0, 0
        
        # คำนวณ Beta (slope ของ regression)
        covariance = np.cov(portfolio_returns, benchmark_returns)[0][1]
        benchmark_variance = np.var(benchmark_returns)
        
        if benchmark_variance == 0:
            beta = 0
        else:
            beta = covariance / benchmark_variance
        
        # คำนวณ Alpha (intercept)
        alpha = portfolio_returns.mean() - (beta * benchmark_returns.mean())
        
        return alpha, beta
    
    @staticmethod
    def calculate_volatility(returns, annualize=True):
        """
        คำนวณความผันผวน (Standard Deviation of Returns)
        
        Args:
            returns: Series ของ returns
            annualize: แปลงเป็นรายปีหรือไม่
            
        Returns:
            float: Volatility
        """
        if len(returns) == 0:
            return 0
        
        volatility = returns.std()
        
        if annualize:
            volatility *= np.sqrt(252)  # annualize (252 trading days)
        
        return volatility
    
    @staticmethod
    def calculate_information_ratio(portfolio_returns, benchmark_returns):
        """
        คำนวณ Information Ratio = (Portfolio Return - Benchmark Return) / Tracking Error
        
        Args:
            portfolio_returns: Series ของ portfolio returns
            benchmark_returns: Series ของ benchmark returns
            
        Returns:
            float: Information Ratio
        """
        if len(portfolio_returns) == 0 or len(benchmark_returns) == 0:
            return 0
        
        excess_returns = portfolio_returns - benchmark_returns
        tracking_error = excess_returns.std()
        
        if tracking_error == 0:
            return 0
        
        return np.sqrt(252) * (excess_returns.mean() / tracking_error)
    
    @staticmethod
    def generate_report(backtest_results, equity_curve):
        """
        สร้างรายงานสรุปผลลัพธ์
        
        Args:
            backtest_results: dict จาก Backtester.get_results()
            equity_curve: DataFrame ของ equity curve
            
        Returns:
            dict: รายงานสรุป
        """
        if equity_curve.empty:
            return {}
        
        # คำนวณ returns
        returns = equity_curve['Portfolio Value'].pct_change().dropna()
        
        # คำนวณ metrics
        sharpe = PerformanceMetrics.calculate_sharpe_ratio(returns)
        sortino = PerformanceMetrics.calculate_sortino_ratio(returns)
        max_dd, max_dd_duration = PerformanceMetrics.calculate_max_drawdown(
            equity_curve['Portfolio Value']
        )
        volatility = PerformanceMetrics.calculate_volatility(returns)
        
        # คำนวณ Calmar Ratio
        total_return = backtest_results.get('total_return', 0)
        years = len(equity_curve) / 252  # ประมาณการจำนวนปี
        calmar = PerformanceMetrics.calculate_calmar_ratio(total_return, max_dd, years)
        
        # คำนวณ Expectancy
        win_rate = backtest_results.get('win_rate', 0) / 100
        avg_win = backtest_results.get('avg_win', 0)
        avg_loss = backtest_results.get('avg_loss', 0)
        expectancy = PerformanceMetrics.calculate_expectancy(win_rate, avg_win, avg_loss)
        
        report = {
            'sharpe_ratio': sharpe,
            'sortino_ratio': sortino,
            'max_drawdown': max_dd,
            'max_drawdown_duration': max_dd_duration,
            'volatility': volatility * 100,  # เป็น %
            'calmar_ratio': calmar,
            'expectancy': expectancy,
            'total_return': total_return,
            'win_rate': backtest_results.get('win_rate', 0),
            'profit_factor': backtest_results.get('profit_factor', 0),
            'total_trades': backtest_results.get('total_trades', 0),
            'avg_win': avg_win,
            'avg_loss': avg_loss
        }
        
        return report


if __name__ == "__main__":
    # ทดสอบ PerformanceMetrics
    print("Testing PerformanceMetrics...")
    
    # สร้างข้อมูลจำลอง
    returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.015, 0.005, -0.002])
    
    sharpe = PerformanceMetrics.calculate_sharpe_ratio(returns)
    print(f"Sharpe Ratio: {sharpe:.2f}")
    
    sortino = PerformanceMetrics.calculate_sortino_ratio(returns)
    print(f"Sortino Ratio: {sortino:.2f}")
    
    # สร้าง equity curve จำลอง
    equity = pd.Series([10000, 10100, 10050, 10200, 10100, 10250, 10300, 10280])
    max_dd, duration = PerformanceMetrics.calculate_max_drawdown(equity)
    print(f"Max Drawdown: {max_dd:.2f}%, Duration: {duration} days")
