"""
Stock Analyzer - Main Application
โปรแกรมหลักสำหรับวิเคราะห์หุ้น
"""

import logging
import json
from datetime import datetime
from src.data.fetcher import StockDataFetcher, FundamentalAnalyzer
from src.analysis.technical import TechnicalAnalyzer
from src.signals.generator import SignalGenerator, AISignalGenerator
from src.notifications.notifier import NotificationManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class StockAnalyzerApp:
    """แอปพลิเคชันหลักสำหรับวิเคราะห์หุ้น"""
    
    def __init__(self):
        self.fetcher = StockDataFetcher()
        self.technical_analyzer = TechnicalAnalyzer()
        self.fundamental_analyzer = FundamentalAnalyzer()
        self.signal_generator = SignalGenerator()
        self.ai_signal_generator = AISignalGenerator()
        self.notification_manager = NotificationManager()
        self.analysis_results = {}
    
    def analyze_single_stock(self, symbol, period='1y'):
        """
        วิเคราะห์หุ้นตัวเดียว
        
        Args:
            symbol: สัญลักษณ์หุ้น
            period: ระยะเวลา
        
        Returns:
            dict: ผลการวิเคราะห์
        """
        logger.info(f"Analyzing {symbol}...")
        
        try:
            # ดึงข้อมูล
            data = self.fetcher.fetch_historical_data(symbol, period=period)
            if data is None or data.empty:
                logger.error(f"No data available for {symbol}")
                return None
            
            # วิเคราะห์ทางเทคนิค
            technical_summary = self.technical_analyzer.get_technical_summary(data)
            
            # วิเคราะห์พื้นฐาน
            valuation = self.fundamental_analyzer.analyze_valuation(symbol)
            health = self.fundamental_analyzer.analyze_financial_health(symbol)
            
            # สร้างสัญญาณ
            signals = self.signal_generator.generate_signals_from_indicators(technical_summary)
            entry_exit = self.signal_generator.generate_entry_exit_points(data)
            
            # รวมผลลัพธ์
            result = {
                'symbol': symbol,
                'timestamp': datetime.now().isoformat(),
                'technical': technical_summary,
                'valuation': valuation,
                'health': health,
                'signals': signals,
                'entry_exit': entry_exit
            }
            
            self.analysis_results[symbol] = result
            logger.info(f"Analysis complete for {symbol}")
            
            return result
        
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {str(e)}")
            return None
    
    def analyze_multiple_stocks(self, symbols, period='1y'):
        """
        วิเคราะห์หุ้นหลายตัว
        
        Args:
            symbols: รายชื่อสัญลักษณ์หุ้น
            period: ระยะเวลา
        
        Returns:
            dict: ผลการวิเคราะห์ทั้งหมด
        """
        results = {}
        for symbol in symbols:
            result = self.analyze_single_stock(symbol, period=period)
            if result:
                results[symbol] = result
        
        return results
    
    def find_buy_opportunities(self, symbols, min_confidence=0.6):
        """
        หาโอกาสในการซื้อ
        
        Args:
            symbols: รายชื่อสัญลักษณ์หุ้น
            min_confidence: ระดับความมั่นใจขั้นต่ำ
        
        Returns:
            list: หุ้นที่มีสัญญาณซื้อ
        """
        buy_opportunities = []
        
        for symbol in symbols:
            result = self.analyze_single_stock(symbol)
            if result is None:
                continue
            
            signals = result['signals']
            if signals['buy'] == 1 and signals['confidence'] >= min_confidence:
                buy_opportunities.append({
                    'symbol': symbol,
                    'signal': 'BUY',
                    'confidence': signals['confidence'],
                    'reasons': signals['reasons'],
                    'entry_price': result['entry_exit']['entry_price'],
                    'target_price': result['entry_exit']['target_price'],
                    'stop_loss': result['entry_exit']['stop_loss']
                })
        
        # เรียงลำดับตามความมั่นใจ
        buy_opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        
        return buy_opportunities
    
    def find_sell_opportunities(self, symbols, min_confidence=0.6):
        """
        หาโอกาสในการขาย
        
        Args:
            symbols: รายชื่อสัญลักษณ์หุ้น
            min_confidence: ระดับความมั่นใจขั้นต่ำ
        
        Returns:
            list: หุ้นที่มีสัญญาณขาย
        """
        sell_opportunities = []
        
        for symbol in symbols:
            result = self.analyze_single_stock(symbol)
            if result is None:
                continue
            
            signals = result['signals']
            if signals['sell'] == 1 and signals['confidence'] >= min_confidence:
                sell_opportunities.append({
                    'symbol': symbol,
                    'signal': 'SELL',
                    'confidence': signals['confidence'],
                    'reasons': signals['reasons'],
                    'exit_price': result['entry_exit']['entry_price']
                })
        
        # เรียงลำดับตามความมั่นใจ
        sell_opportunities.sort(key=lambda x: x['confidence'], reverse=True)
        
        return sell_opportunities
    
    def get_hot_stocks(self, symbols):
        """
        หาหุ้นที่โดดเด่น (จากสัญญาณที่ชัดเจน)
        
        Args:
            symbols: รายชื่อสัญลักษณ์หุ้น
        
        Returns:
            dict: หุ้นที่น่าสนใจ
        """
        hot_stocks = {
            'strong_buys': [],
            'buys': [],
            'sells': [],
            'strong_sells': []
        }
        
        for symbol in symbols:
            result = self.analyze_single_stock(symbol)
            if result is None:
                continue
            
            signals = result['signals']
            confidence = signals['confidence']
            
            stock_info = {
                'symbol': symbol,
                'price': result['technical']['latest_price'],
                'confidence': confidence,
                'reasons': signals['reasons']
            }
            
            if signals['buy'] == 1:
                if confidence >= 0.8:
                    hot_stocks['strong_buys'].append(stock_info)
                else:
                    hot_stocks['buys'].append(stock_info)
            elif signals['sell'] == 1:
                if confidence >= 0.8:
                    hot_stocks['strong_sells'].append(stock_info)
                else:
                    hot_stocks['sells'].append(stock_info)
        
        return hot_stocks
    
    def save_results_to_json(self, filename='analysis_results.json'):
        """บันทึกผลลัพธ์เป็น JSON"""
        try:
            with open(filename, 'w') as f:
                json.dump(self.analysis_results, f, indent=4, default=str)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
    
    def print_analysis_summary(self, symbol):
        """พิมพ์สรุปผลการวิเคราะห์"""
        if symbol not in self.analysis_results:
            print(f"ไม่พบผลการวิเคราะห์สำหรับ {symbol}")
            return
        
        result = self.analysis_results[symbol]
        
        print(f"\n{'='*60}")
        print(f"รายงานวิเคราะห์หุ้น: {symbol}")
        print(f"{'='*60}\n")
        
        # Technical Info
        technical = result['technical']
        print("📊 ตัวชี้วัดเทคนิค:")
        print(f"  ราคาปัจจุบัน: ${technical['latest_price']:.2f}")
        print(f"  ค่าเฉลี่ยเคลื่อนที่ 20 วัน: ${technical['sma_20']:.2f}")
        print(f"  ค่าเฉลี่ยเคลื่อนที่ 50 วัน: ${technical['sma_50']:.2f}")
        print(f"  ค่าเฉลี่ยเคลื่อนที่ 200 วัน: ${technical['sma_200']:.2f}")
        print(f"  ดัชนีความแข็งแกร่งสัมพัทธ์ (RSI): {technical['rsi']:.2f}")
        print(f"  MACD: {technical['macd']:.4f}")
        print(f"  ช่วงแท้จริงเฉลี่ย (ATR): {technical['atr']:.4f}")
        
        # Signals
        signals = result['signals']
        print(f"\n📈 สัญญาณ:")
        signal_type = 'ซื้อ' if signals['buy'] else ('ขาย' if signals['sell'] else 'คงตำแหน่ง')
        print(f"  สัญญาณ: {signal_type}")
        print(f"  ระดับความเชื่อมั่น: {signals['confidence']:.2%}")
        print(f"  เหตุผล:")
        for reason in signals['reasons']:
            print(f"    • {reason}")
        
        # Entry/Exit
        entry_exit = result['entry_exit']
        print(f"\n🎯 จุดการเทรด:")
        print(f"  จุดเข้า: ${entry_exit['entry_price']:.2f}")
        print(f"  เป้าหมาย: ${entry_exit['target_price']:.2f}")
        print(f"  ตัดขาดทุน: ${entry_exit['stop_loss']:.2f}")
        
        # Valuation
        valuation = result['valuation']
        print(f"\n💰 การประเมินมูลค่า:")
        print(f"  อัตราส่วนราคาต่อกำไร (P/E): {valuation.get('pe_ratio', 'ไม่มีข้อมูล')}")
        print(f"  P/E ไปข้างหน้า: {valuation.get('forward_pe', 'ไม่มีข้อมูล')}")
        print(f"  ผลตอบแทนจากเงินปันผล: {valuation.get('dividend_yield', 'ไม่มีข้อมูล')}")
        
        print(f"\n{'='*60}\n")


if __name__ == "__main__":
    # ตัวอย่างการใช้งาน
    app = StockAnalyzerApp()
    
    # วิเคราะห์หุ้นที่น่าสนใจ
    stocks_to_analyze = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN', 'META', 'NFLX', 'NVDA']
    
    print("เริ่มการวิเคราะห์หุ้น...")
    results = app.analyze_multiple_stocks(stocks_to_analyze, period='6mo')
    
    # หาโอกาสซื้อ
    buy_opps = app.find_buy_opportunities(stocks_to_analyze)
    print("\n💚 โอกาสในการซื้อ:")
    for opp in buy_opps:
        print(f"\n{opp['symbol']}")
        print(f"  ระดับความเชื่อมั่น: {opp['confidence']:.2%}")
        print(f"  จุดเข้า: ${opp['entry_price']:.2f}")
        print(f"  เป้าหมาย: ${opp['target_price']:.2f}")
        print(f"  ตัดขาดทุน: ${opp['stop_loss']:.2f}")
    
    # หาหุ้นโดดเด่น
    hot = app.get_hot_stocks(stocks_to_analyze)
    print("\n🔥 หุ้นโดดเด่น:")
    print(f"ซื้อแรง: {len(hot['strong_buys'])}")
    print(f"ซื้อ: {len(hot['buys'])}")
    print(f"ขาย: {len(hot['sells'])}")
    print(f"ขายแรง: {len(hot['strong_sells'])}")
    
    # บันทึกผลลัพธ์
    app.save_results_to_json()
