"""
อินเทอร์เฟสบรรทัดคำสั่ง (CLI) สำหรับ Stock Analyzer
อินเทอร์เฟสบรรทัดคำสั่งเพื่อการโต้ตอบที่ง่ายดาย
"""

import argparse
import json
from datetime import datetime
from main import StockAnalyzerApp
from src.discovery.scanner import StockScanner


def main():
    parser = argparse.ArgumentParser(
        description='Stock Analyzer - เครื่องมือวิเคราะห์หุ้น USA'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='คำสั่งที่มีอยู่')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='วิเคราะห์หุ้น')
    analyze_parser.add_argument('symbols', nargs='+', help='สัญลักษณ์หุ้น (เช่น AAPL MSFT GOOGL)')
    analyze_parser.add_argument('-p', '--period', default='1y', 
                               help='ระยะเวลา (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y)')
    analyze_parser.add_argument('-o', '--output', help='ไฟล์เอาท์พุต JSON')
    
    # Buy signals command
    buy_parser = subparsers.add_parser('buy', help='หาโอกาสในการซื้อ')
    buy_parser.add_argument('symbols', nargs='+', help='สัญลักษณ์หุ้น')
    buy_parser.add_argument('-c', '--confidence', type=float, default=0.6,
                           help='ระดับความเชื่อมั่นขั้นต่ำ (0.0-1.0)')
    
    # Sell signals command
    sell_parser = subparsers.add_parser('sell', help='หาโอกาสในการขาย')
    sell_parser.add_argument('symbols', nargs='+', help='สัญลักษณ์หุ้น')
    sell_parser.add_argument('-c', '--confidence', type=float, default=0.6,
                            help='ระดับความเชื่อมั่นขั้นต่ำ (0.0-1.0)')
    
    # Hot stocks command
    hot_parser = subparsers.add_parser('hot', help='หาหุ้นโดดเด่น')
    hot_parser.add_argument('symbols', nargs='+', help='สัญลักษณ์หุ้น')
    
    # Discovery commands
    discover_parser = subparsers.add_parser('discover', help='ค้นหาหุ้นจากตลาด')
    discover_parser.add_argument('type', choices=['popular', 'trending', 'microcap'],
                                help='ประเภทการค้นหา (popular/trending/microcap)')
    discover_parser.add_argument('-a', '--analyze', action='store_true',
                                help='วิเคราะห์หุ้นที่พบทั้งหมด')
    
    # Microcap scanner
    microcap_parser = subparsers.add_parser('microcap', help='สแกนหุ้นจิ๋ว')
    microcap_parser.add_argument('type', choices=['gainers', 'high-vol', 'low-price'],
                                help='ประเภทหุ้นจิ๋ว')
    microcap_parser.add_argument('-l', '--limit', type=int, default=10,
                                help='จำนวนหุ้นที่แสดง')
    microcap_parser.add_argument('--min-price', type=float, default=0.0,
                                help='ราคาต่ำสุด ($)')
    microcap_parser.add_argument('--max-price', type=float, default=None,
                                help='ราคาสูงสุด ($)')
    
    args = parser.parse_args()
    
    app = StockAnalyzerApp()
    
    if args.command == 'analyze':
        print(f"\n{'='*60}")
        print(f"กำลังวิเคราะห์ {', '.join(args.symbols)}...")
        print(f"{'='*60}\n")
        
        results = app.analyze_multiple_stocks(args.symbols, period=args.period)
        
        for symbol, result in results.items():
            if result:
                app.print_analysis_summary(symbol)
        
        if args.output:
            app.save_results_to_json(args.output)
            print(f"\n✅ บันทึกผลลัพธ์ไปยัง {args.output}")
    
    elif args.command == 'buy':
        print(f"\n{'='*60}")
        print(f"หาโอกาสในการซื้อใน {', '.join(args.symbols)}...")
        print(f"{'='*60}\n")
        
        buy_opps = app.find_buy_opportunities(args.symbols, args.confidence)
        
        if buy_opps:
            print(f"💚 พบโอกาสในการซื้อ {len(buy_opps)} รายการ:\n")
            for i, opp in enumerate(buy_opps, 1):
                print(f"{i}. {opp['symbol']}")
                print(f"   ระดับความเชื่อมั่น: {opp['confidence']:.1%}")
                print(f"   จุดเข้า: ${opp['entry_price']:.2f}")
                print(f"   เป้าหมาย: ${opp['target_price']:.2f}")
                print(f"   ตัดขาดทุน: ${opp['stop_loss']:.2f}")
                print(f"   ศักยภาพกำไร: {((opp['target_price']-opp['entry_price'])/opp['entry_price']*100):.1f}%")
                print(f"   เหตุผล:")
                for reason in opp['reasons']:
                    print(f"     • {reason}")
                print()
        else:
            print("❌ ไม่พบโอกาสในการซื้อที่ตรงกับเกณฑ์ความเชื่อมั่น")
    
    elif args.command == 'sell':
        print(f"\n{'='*60}")
        print(f"หาโอกาสในการขายใน {', '.join(args.symbols)}...")
        print(f"{'='*60}\n")
        
        sell_opps = app.find_sell_opportunities(args.symbols, args.confidence)
        
        if sell_opps:
            print(f"🔴 พบโอกาสในการขาย {len(sell_opps)} รายการ:\n")
            for i, opp in enumerate(sell_opps, 1):
                print(f"{i}. {opp['symbol']}")
                print(f"   ระดับความเชื่อมั่น: {opp['confidence']:.1%}")
                print(f"   ราคาออก: ${opp['exit_price']:.2f}")
                print(f"   เหตุผล:")
                for reason in opp['reasons']:
                    print(f"     • {reason}")
                print()
        else:
            print("❌ ไม่พบโอกาสในการขายที่ตรงกับเกณฑ์ความเชื่อมั่น")
    
    elif args.command == 'hot':
        print(f"\n{'='*60}")
        print(f"หุ้นโดดเด่นใน {', '.join(args.symbols)}...")
        print(f"{'='*60}\n")
        
        hot = app.get_hot_stocks(args.symbols)
        
        print(f"🟢 ซื้อแรง: {len(hot['strong_buys'])}")
        for stock in hot['strong_buys']:
            print(f"   {stock['symbol']} ({stock['confidence']:.1%})")
        
        print(f"\n💚 ซื้อ: {len(hot['buys'])}")
        for stock in hot['buys']:
            print(f"   {stock['symbol']} ({stock['confidence']:.1%})")
        
        print(f"\n📉 ขาย: {len(hot['sells'])}")
        for stock in hot['sells']:
            print(f"   {stock['symbol']} ({stock['confidence']:.1%})")
        
        print(f"\n🔴 ขายแรง: {len(hot['strong_sells'])}")
        for stock in hot['strong_sells']:
            print(f"   {stock['symbol']} ({stock['confidence']:.1%})")
        
        print()
    
    elif args.command == 'discover':
        print(f"\n{'='*60}")
        print(f"🔍 ค้นหาหุ้น - {args.type}")
        print(f"{'='*60}\n")
        
        scanner = StockScanner()
        
        if args.type == 'popular':
            stocks = scanner.get_popular_stocks()
            print(f"📊 หุ้นแนวโน้มสูง ({len(stocks)} ตัว):\n")
            for i, symbol in enumerate(stocks[:20], 1):
                info = scanner.get_stock_summary(symbol)
                if info:
                    market_cap_category = info.get('market_cap_category', 'ไม่ทราบ')
                    print(f"{i}. {symbol} - {info.get('name', 'N/A')}")
                    print(f"   ราคา: ${info.get('current_price', 'N/A')}")
                    print(f"   หมวดหมู่: {market_cap_category}\n")
        
        elif args.type == 'trending':
            print("🔄 กำลังสแกนหุ้นที่มีแนวโน้มขึ้น...")
            trending = scanner.scan_trending_stocks()
            
            print(f"\n📈 ขึ้น 20%+:")
            for stock in trending['up_20_percent'][:5]:
                print(f"   {stock['symbol']}: {stock['change']:.2f}% - ${stock['price']:.2f}")
            
            print(f"\n📈 ขึ้น 10-20%:")
            for stock in trending['up_10_percent'][:5]:
                print(f"   {stock['symbol']}: {stock['change']:.2f}% - ${stock['price']:.2f}")
        
        elif args.type == 'microcap':
            stocks = scanner.get_microcap_stocks()
            print(f"💎 หุ้นจิ๋ว ({len(stocks)} ตัว):\n")
            for i, symbol in enumerate(stocks[:15], 1):
                info = scanner.get_stock_summary(symbol)
                if info:
                    print(f"{i}. {symbol} - {info.get('name', 'N/A')}")
                    print(f"   ราคา: ${info.get('current_price', 'N/A')}")
                    print(f"   หมวดหมู่: {info.get('market_cap_category', 'ไม่ทราบ')}\n")
        
        # Analyze if requested
        if args.analyze and args.type in ['popular', 'microcap']:
            stocks = scanner.get_popular_stocks() if args.type == 'popular' else scanner.get_microcap_stocks()
            print(f"\n🔄 กำลังวิเคราะห์หุ้น {len(stocks[:5])} ตัวแรก...")
            results = app.analyze_multiple_stocks(stocks[:5])
            print("✅ เสร็จสิ้นการวิเคราะห์")
    
    elif args.command == 'microcap':
        print(f"\n{'='*60}")
        print(f"💎 สแกนหุ้นจิ๋ว - {args.type}")
        print(f"ช่วงราคา: ${args.min_price:.2f} - ${args.max_price if args.max_price else 'unlimited'}")
        print(f"{'='*60}\n")
        
        scanner = StockScanner()
        print("🔄 กำลังสแกนหุ้นจิ๋ว...")
        gainers = scanner.scan_microcap_gainers(min_price=args.min_price, max_price=args.max_price)
        
        if args.type == 'gainers':
            print("\n🎢 ความผันผวนสูง:")
            for stock in gainers['high_volatility'][:args.limit]:
                print(f"   {stock['symbol']}: ความผันผวน {stock['volatility']:.1f}% - ${stock['price']:.2f}")
        
        elif args.type == 'high-vol':
            print("\n🎢 ทะลุขึ้น (Breakout):")
            for stock in gainers['breakout'][:args.limit]:
                print(f"   {stock['symbol']}: ราคา ${stock['price']:.2f}")
        
        elif args.type == 'low-price':
            print("\n💰 ราคาต่ำแต่ศักยภาพสูง:")
            for stock in gainers['low_price_high_gain'][:args.limit]:
                print(f"   {stock['symbol']}: ศักยภาพ {stock['potential_upside']:.1f}% - ${stock['price']:.2f}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
