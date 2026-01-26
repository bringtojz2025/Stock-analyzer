"""
แอปพลิเคชัน Dashboard โดยใช้ Streamlit
แสดงผลวิเคราะห์หุ้นแบบเรียลไทม์
"""

import streamlit as st
from datetime import datetime
import sys
import os
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd
import subprocess

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from main import StockAnalyzerApp
from src.discovery.scanner import StockScanner
from src.details.provider import StockDetailsProvider
from src.details.widget import StockInfoWidget
from src.dividend.analyzer import DividendAnalyzer
from src.portfolio.manager import PortfolioManager


# ตั้งค่าเพจ
st.set_page_config(
    page_title="แอปพลิเคชันวิเคราะห์หุ้น USA",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================
# Navigation Bar
# ========================
st.markdown("""
<style>
    .nav-bar {
        background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
        padding: 1rem 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .nav-title {
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="nav-bar"><div class="nav-title">📊 แอปพลิเคชันวิเคราะห์หุ้น USA</div></div>', unsafe_allow_html=True)

# Initialize session state for navigation
if 'current_page' not in st.session_state:
    st.session_state.current_page = "วิเคราะห์หุ้น"

# Navigation Menu
col_nav1, col_nav2, col_nav3 = st.columns(3)

with col_nav1:
    if st.button("📊 Dashboard", use_container_width=True, type="primary" if st.session_state.current_page == "Dashboard" else "secondary"):
        st.session_state.current_page = "Dashboard"
        st.rerun()

with col_nav2:
    if st.button("💼 Portfolio", use_container_width=True, type="primary" if st.session_state.current_page == "Portfolio" else "secondary"):
        st.session_state.current_page = "Portfolio"
        st.rerun()

with col_nav3:
    if st.button("📈 วิเคราะห์หุ้น", use_container_width=True, type="primary" if st.session_state.current_page == "วิเคราะห์หุ้น" else "secondary"):
        st.session_state.current_page = "วิเคราะห์หุ้น"
        st.rerun()

st.divider()

# Sidebar
with st.sidebar:
    # Create tabs in sidebar for better organization
    sidebar_tab1, sidebar_tab2, sidebar_tab3 = st.tabs(["🏠 เลือกหุ้น", "⚙️ ตั้งค่า", "ℹ️ ช่วยเหลือ"])
    
    with sidebar_tab1:
        st.header("เลือกหุ้นที่วิเคราะห์")
        
        # Initialize selected_stocks
        selected_stocks = []
        
        # Mode selection with better styling
        mode = st.radio(
            "เลือกโหมดการใช้งาน",
            ["📝 ป้อนชื่อหุ้น", "🔍 ค้นหาจากตลาด", "💎 หุ้นจิ๋วที่น่าสนใจ", "💰 หุ้นปันผล"],
            index=0,
            help="เลือกวิธีการค้นหาหุ้นที่ต้องการวิเคราะห์"
        )
    
    with sidebar_tab2:
        st.header("⚙️ การตั้งค่า")
        
        # Settings section
        st.subheader("🔍 วิธีการแสดงผล")
        show_detailed_charts = st.checkbox("📊 แสดงกราฟรายละเอียด", value=True)
        show_technical_indicators = st.checkbox("📈 แสดง Technical Indicators", value=True)
        
        st.divider()
        st.subheader("🎯 ตั้งค่าสัญญาณ")
        min_confidence = st.slider(
            "ความมั่นใจขั้นต่ำของสัญญาณ (%)",
            min_value=30,
            max_value=100,
            value=60,
            step=5,
            help="สัญญาณจะแสดงเฉพาะที่มีความมั่นใจตั้งแต่ระดับนี้ขึ้นไป"
        )
        
        st.divider()
        st.subheader("📅 ช่วงเวลา")
        period = st.selectbox(
            "เลือกช่วงเวลาการวิเคราะห์",
            ["1mo", "3mo", "6mo", "1y", "2y", "5y"],
            index=3,
            help="ระยะเวลาของข้อมูลที่ใช้ในการวิเคราะห์"
        )
        
        st.divider()
        st.subheader("💾 การบันทึก")
        if st.button("💾 ดาวน์โหลดผลการวิเคราะห์", use_container_width=True):
            st.info("✅ ฟีเจอร์นี้จะอัปเดตในเร็ว ๆ นี้")
    
    with sidebar_tab3:
        st.header("ℹ️ ข้อมูลและช่วยเหลือ")
        st.markdown("""
        ### วิธีการใช้งาน
        1. **เลือกหุ้น**: ไปที่แท็บ "เลือกหุ้น" เพื่อเลือกหุ้นที่ต้องการวิเคราะห์
        2. **ตั้งค่า**: ปรับการตั้งค่าในแท็บ "ตั้งค่า"
        3. **ดูผลลัพธ์**: เลือกแท็บต่าง ๆ เพื่อดูผลการวิเคราะห์
        
        ### ความหมายของสิ่งต่อไปนี้
        - **RSI**: Relative Strength Index (แรงผลักดันของราคา)
        - **MACD**: Moving Average Convergence Divergence (แนวโน้ม)
        - **SMA**: Simple Moving Average (ค่าเฉลี่ยเคลื่อนที่)
        - **Buy Signal**: สัญญาณซื้อ (โอกาสที่ราคาจะขึ้น)
        - **Sell Signal**: สัญญาณขาย (โอกาสที่ราคาจะลง)
        
        ### ข้อจำกัด
        ⚠️ นี่คือเครื่องมือวิเคราะห์เท่านั้น ไม่ใช่คำแนะนำการลงทุน
        """)
    
    # Mode selection logic (moved outside tabs for functionality)
    if mode != "📝 ป้อนชื่อหุ้น":
        # Switch back to sidebar_tab1 for mode selection
        pass
    
    # Stock selection based on mode
    if mode == "📝 ป้อนชื่อหุ้น":
        stock_list = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA',
            'META', 'NFLX', 'NVDA', 'AMD', 'INTEL',
            'JPM', 'BAC', 'WFC', 'GS', 'MS'
        ]
        
        st.write("**วิธีการป้อน:** พิมพ์ชื่อหุ้น แยกด้วย `,` เช่น AAPL,MSFT,TSLA")
        
        # Option 1: ใช้ multiselect กับรายการที่มี
        st.write("**ตัวเลือก 1: เลือกจากรายการแนะนำ**")
        selected_from_list = st.multiselect(
            "เลือกหุ้นที่ต้องการวิเคราะห์ (ไม่บังคับ)",
            stock_list,
            default=['AAPL', 'MSFT', 'GOOGL'],
            key="stock_multiselect"
        )
        
        # Option 2: ป้อนชื่อหุ้นเองอย่างอิสระ
        st.write("**ตัวเลือก 2: ป้อนชื่อหุ้นเอง**")
        custom_stocks_input = st.text_input(
            "พิมพ์ชื่อหุ้นที่ต้องการ (แยกด้วย comma, เช่น: AAPL,MSFT,GOOGL,TSLA)",
            placeholder="AAPL,MSFT,GOOGL,NVDA",
            key="custom_stock_input"
        )
        
        # รวมหุ้นที่เลือก
        if custom_stocks_input.strip():
            # แปลงข้อความจากการป้อนเป็นลิสต์
            custom_list = [s.strip().upper() for s in custom_stocks_input.split(',') if s.strip()]
            # รวมกับหุ้นที่เลือกจากลิสต์ (ตัดซ้ำ)
            selected_stocks = list(dict.fromkeys(custom_list + selected_from_list))
            st.info(f"✅ จำนวนหุ้นที่เลือก: {len(selected_stocks)} ตัว - {', '.join(selected_stocks[:10])}")
            if len(selected_stocks) > 10:
                st.write(f"... และอีก {len(selected_stocks) - 10} ตัว")
        else:
            selected_stocks = selected_from_list
            if selected_stocks:
                st.info(f"✅ จำนวนหุ้นที่เลือก: {len(selected_stocks)} ตัว")
    
    elif mode == "🔍 ค้นหาจากตลาด":
        scanner = StockScanner()
        
        search_type = st.selectbox(
            "เลือกประเภทการค้นหา",
            ["หุ้นแนวโน้มสูง (Large-Cap)", "หุ้นที่มีแนวโน้มขึ้น", "หุ้นนำหน้า"]
        )
        
        if search_type == "หุ้นแนวโน้มสูง (Large-Cap)":
            selected_stocks = scanner.get_popular_stocks()[:20]
            st.info(f"📊 ค้นหาหุ้นแนวโน้มสูง {len(selected_stocks)} ตัว")
        
        elif search_type == "หุ้นที่มีแนวโน้มขึ้น":
            with st.spinner("🔄 กำลังสแกนหุ้นที่มีแนวโน้มขึ้น..."):
                trending = scanner.scan_trending_stocks()
                trending_list = trending['up_20_percent'] + trending['up_10_percent'] + trending['up_5_percent']
                selected_stocks = [stock['symbol'] for stock in trending_list[:15]]
                st.success(f"✅ พบหุ้นที่มีแนวโน้มขึ้น {len(selected_stocks)} ตัว")
        
        else:  # หุ้นนำหน้า
            selected_stocks = scanner.get_popular_stocks()[:10]
            st.info(f"⭐ หุ้นนำหน้า {len(selected_stocks)} ตัว")
    
    elif mode == "💎 หุ้นจิ๋วที่น่าสนใจ":
        scanner = StockScanner()
        
        microcap_type = st.selectbox(
            "เลือกประเภทหุ้นจิ๋ว",
            ["โอกาสขึ้นแรง", "ความผันผวนสูง", "ราคาต่ำแต่ศักยภาพสูง"]
        )
        
        # เพิ่มตัวควบคุมราคาสำหรับหุ้นจิ๋ว
        st.write("🎯 ปรับเงื่อนไขราคา:")
        price_range = st.slider(
            "ช่วงราคา ($)",
            min_value=0.0,
            max_value=50.0,
            value=(0.0, 20.0),
            step=0.5
        )
        
        min_price = price_range[0]
        max_price = price_range[1]
        
        if microcap_type == "โอกาสขึ้นแรง":
            selected_stocks = scanner.get_microcap_stocks()[:20]
            st.info("💎 หุ้นจิ๋วที่มีโอกาสขึ้นแรง")
        
        elif microcap_type == "ความผันผวนสูง":
            with st.spinner("🔄 กำลังสแกนหุ้นจิ๋ว..."):
                gainers = scanner.scan_microcap_gainers(min_price=min_price, max_price=max_price)
                selected_stocks = [stock['symbol'] for stock in gainers['high_volatility'][:15]]
                if not selected_stocks:
                    selected_stocks = scanner.get_microcap_stocks()[:15]
            st.info(f"🎢 หุ้นจิ๋วที่มีความผันผวนสูง (ราคา: ${min_price:.2f} - ${max_price:.2f})")
        
        else:  # ราคาต่ำแต่ศักยภาพสูง
            selected_stocks = scanner.get_microcap_stocks()[:20]
            st.info(f"💰 หุ้นจิ๋วราคาต่ำแต่ศักยภาพสูง (ราคา: ${min_price:.2f} - ${max_price:.2f})")
    
    elif mode == "💰 หุ้นปันผล":
        st.write("🎯 หุ้นปันผล (Dividend Stocks)")
        st.write("หุ้นที่จ่ายเงินปันผลสูง เหมาะสำหรับนักลงทุนรายได้")
        
        dividend_analyzer = DividendAnalyzer()
        
        # เลือกประเภทปันผล
        st.write("**เลือกประเภทปันผลที่ต้องการค้นหา:**")
        dividend_period = st.radio(
            "ระยะเวลาปันผล",
            ["📅 รายปี (Annual)", "📅 รายเดือน (Monthly)", "📅 รายสัปดาห์ (Weekly)"],
            key="dividend_period_search"
        )
        
        # ตั้งค่าผลตอบแทนที่ต้องการตามประเภท
        st.write("**ตั้งค่าตัวกรอง:**")
        
        if "รายปี" in dividend_period:
            min_dividend = st.slider(
                "Dividend Yield รายปี ต่ำสุด (%)",
                min_value=0.0,
                max_value=10.0,
                value=2.0,
                step=0.5,
                key="min_dividend_slider_year"
            )
            dividend_filter_type = "yearly"
            st.info("💡 ค้นหาหุ้นที่มีอัตราปันผลรายปี ≥ " + str(min_dividend) + "%")
        elif "รายเดือน" in dividend_period:
            min_dividend_monthly = st.slider(
                "Dividend ต่ำสุด/เดือน (%)",
                min_value=0.0,
                max_value=1.0,
                value=0.15,
                step=0.05,
                key="min_dividend_slider_month"
            )
            # แปลงจาก monthly % ไป annual %
            min_dividend = min_dividend_monthly * 12
            dividend_filter_type = "monthly"
            st.info(f"💡 ค้นหาหุ้นที่มีปันผล/เดือน ≥ {min_dividend_monthly:.2f}% (อัตรารายปี {min_dividend:.2f}%)")
        else:  # รายสัปดาห์
            min_dividend_weekly = st.slider(
                "Dividend ต่ำสุด/สัปดาห์ (%)",
                min_value=0.0,
                max_value=0.3,
                value=0.04,
                step=0.01,
                key="min_dividend_slider_week"
            )
            # แปลงจาก weekly % ไป annual %
            min_dividend = min_dividend_weekly * 52
            dividend_filter_type = "weekly"
            st.info(f"💡 ค้นหาหุ้นที่มีปันผล/สัปดาห์ ≥ {min_dividend_weekly:.3f}% (อัตรารายปี {min_dividend:.2f}%)")
        
        # ค้นหาหุ้นปันผลโดยอัตโนมัติ
        st.write("**ค้นหาหุ้นปันผล:**")
        search_col1, search_col2 = st.columns([3, 1])
        
        with search_col1:
            search_button_label = f"🔍 ค้นหาหุ้นปันผล{dividend_period}"
        with search_col2:
            pass
        
        if st.button(search_button_label, key="search_dividend_btn"):
            with st.spinner(f"🔄 กำลังค้นหาหุ้นปันผล{dividend_period}..."):
                high_dividend_stocks = dividend_analyzer.find_high_dividend_stocks(
                    min_yield=min_dividend/100,
                    limit=20
                )
                
                if high_dividend_stocks:
                    st.success(f"✅ พบหุ้นปันผล {len(high_dividend_stocks)} ตัว")
                    
                    # สร้างตารางตามประเภทปันผล
                    if "รายปี" in dividend_period:
                        df_dividend = pd.DataFrame([
                            {
                                'สัญลักษณ์': stock['symbol'],
                                'ชื่อ': stock['name'],
                                'ราคา': f"${stock['price']:.2f}",
                                'Yield ปีละ': f"{stock['yield']*100:.2f}%",
                                'ปันผล/ปี': f"${stock['annual_dividend']:.2f}",
                            }
                            for stock in high_dividend_stocks
                        ])
                    elif "รายเดือน" in dividend_period:
                        df_dividend = pd.DataFrame([
                            {
                                'สัญลักษณ์': stock['symbol'],
                                'ชื่อ': stock['name'],
                                'ราคา': f"${stock['price']:.2f}",
                                'Yield ปีละ': f"{stock['yield']*100:.2f}%",
                                'ปันผล/เดือน': f"${stock['monthly_dividend']:.3f}",
                                'ปันผล/ปี': f"${stock['annual_dividend']:.2f}",
                            }
                            for stock in high_dividend_stocks
                        ])
                    else:  # รายสัปดาห์
                        df_dividend = pd.DataFrame([
                            {
                                'สัญลักษณ์': stock['symbol'],
                                'ชื่อ': stock['name'],
                                'ราคา': f"${stock['price']:.2f}",
                                'Yield ปีละ': f"{stock['yield']*100:.2f}%",
                                'ปันผล/สัปดาห์': f"${stock['weekly_dividend']:.4f}",
                                'ปันผล/เดือน': f"${stock['monthly_dividend']:.3f}",
                            }
                            for stock in high_dividend_stocks
                        ])
                    
                    st.dataframe(df_dividend, use_container_width=True)
                    
                    # สร้างลิสต์หุ้นสำหรับวิเคราะห์
                    selected_stocks = [stock['symbol'] for stock in high_dividend_stocks]
                    st.info(f"✅ เลือก {len(selected_stocks)} หุ้นสำหรับวิเคราะห์เพิ่มเติม")
                else:
                    st.warning("❌ ไม่พบหุ้นปันผลที่ตรงกับเงื่อนไข กรุณาปรับเงื่อนไขใหม่")
                    selected_stocks = []
        else:
            # ให้เลือกมือ
            st.write("**หรือ - เลือกหุ้นปันผลด้วยตนเอง:**")
            st.write("**ตัวเลือก 1: เลือกจากรายการแนะนำ**")
            dividend_stocks = list(dividend_analyzer.HIGH_DIVIDEND_STOCKS.keys())
            selected_from_dividend_list = st.multiselect(
                "เลือกหุ้นปันผล",
                dividend_stocks,
                default=['T', 'VZ', 'PM', 'ABBV'],
                key="dividend_multiselect"
            )
            
            # Option 2: ป้อนเอง
            st.write("**ตัวเลือก 2: ป้อนชื่อหุ้นเอง**")
            custom_dividend_input = st.text_input(
                "พิมพ์ชื่อหุ้นปันผล (แยกด้วย comma, เช่น: T,VZ,PM,ABBV)",
                placeholder="T,VZ,PM,ABBV",
                key="custom_dividend_input"
            )
            
            # Merge selections
            custom_list = [s.strip().upper() for s in custom_dividend_input.split(',') if s.strip()]
            selected_stocks = list(dict.fromkeys(custom_list + selected_from_dividend_list))
            
            if selected_stocks:
                st.info(f"✅ จำนวนหุ้นปันผลที่เลือก: {len(selected_stocks)} ตัว")
        
        # แสดงข้อมูลปันผลของหุ้นที่เลือก
        if selected_stocks:
            st.subheader("📊 ข้อมูลปันผลโดยละเอียด")
            
            dividend_data = []
            for symbol in selected_stocks:
                try:
                    div_info = dividend_analyzer.get_dividend_info(symbol)
                    if div_info and div_info['dividend_yield'] is not None:
                        dividend_data.append({
                            'สัญลักษณ์': div_info['symbol'],
                            'ชื่อ': div_info['name'],
                            'ราคา': f"${div_info['price']:.2f}",
                            'Yield %': f"{div_info['dividend_yield']*100:.2f}%",
                            'ปันผล/ปี ($)': f"${div_info['dividend_per_share']:.2f}",
                            'ปันผล/เดือน ($)': f"${div_info['monthly_dividend']:.3f}",
                            'ปันผล/สัปดาห์ ($)': f"${div_info['weekly_dividend']:.4f}",
                        })
                except Exception as e:
                    st.warning(f"⚠️ ไม่สามารถดึงข้อมูล {symbol}: {str(e)}")
            
            if dividend_data:
                df_div = pd.DataFrame(dividend_data)
                st.dataframe(df_div, use_container_width=True)
                
                # แสดงสตรีมปันผลตามประเภท
                st.subheader("💰 เปรียบเทียบปันผลตามประเภท")
                
                comparison_col1, comparison_col2, comparison_col3 = st.columns(3)
                
                with comparison_col1:
                    st.write("**📅 ปันผลรายปี**")
                    for stock_data in dividend_data[:5]:
                        symbol = stock_data['สัญลักษณ์']
                        annual = stock_data['ปันผล/ปี ($)']
                        st.metric(f"{symbol}", annual)
                
                with comparison_col2:
                    st.write("**📅 ปันผลรายเดือน**")
                    for stock_data in dividend_data[:5]:
                        symbol = stock_data['สัญลักษณ์']
                        monthly = stock_data['ปันผล/เดือน ($)']
                        st.metric(f"{symbol}", monthly)
                
                with comparison_col3:
                    st.write("**📅 ปันผลรายสัปดาห์**")
                    for stock_data in dividend_data[:5]:
                        symbol = stock_data['สัญลักษณ์']
                        weekly = stock_data['ปันผล/สัปดาห์ ($)']
                        st.metric(f"{symbol}", weekly)
                
                # คำนวณรายได้ปันผล
                st.subheader("💵 คำนวณรายได้ปันผลตามจำนวนเงินลงทุน")
                investment_amount = st.number_input(
                    "จำนวนเงินลงทุน ($)",
                    min_value=1000.0,
                    max_value=1000000.0,
                    value=10000.0,
                    step=1000.0,
                    key="dividend_investment"
                )
                
                if st.button("🧮 คำนวณรายได้ประมาณการ", key="calculate_dividend"):
                    st.write(f"**การลงทุน ${investment_amount:,.0f} ในหุ้นเหล่านี้:**")
                    
                    calc_col1, calc_col2, calc_col3 = st.columns(3)
                    
                    with calc_col1:
                        st.write("**📅 รายได้/ปี**")
                        for stock_data in dividend_data[:5]:
                            symbol = stock_data['สัญลักษณ์']
                            try:
                                div_info = dividend_analyzer.get_dividend_info(symbol)
                                if div_info and div_info['dividend_yield'] is not None:
                                    yearly_income = dividend_analyzer.calculate_dividend_income(
                                        investment_amount,
                                        div_info['dividend_yield'],
                                        'yearly'
                                    )
                                    st.metric(f"{symbol}", f"${yearly_income:,.2f}")
                            except Exception as e:
                                pass
                    
                    with calc_col2:
                        st.write("**📅 รายได้/เดือน**")
                        for stock_data in dividend_data[:5]:
                            symbol = stock_data['สัญลักษณ์']
                            try:
                                div_info = dividend_analyzer.get_dividend_info(symbol)
                                if div_info and div_info['dividend_yield'] is not None:
                                    monthly_income = dividend_analyzer.calculate_dividend_income(
                                        investment_amount,
                                        div_info['dividend_yield'],
                                        'monthly'
                                    )
                                    st.metric(f"{symbol}", f"${monthly_income:,.2f}")
                            except Exception as e:
                                pass
                    
                    with calc_col3:
                        st.write("**📅 รายได้/สัปดาห์**")
                        for stock_data in dividend_data[:5]:
                            symbol = stock_data['สัญลักษณ์']
                            try:
                                div_info = dividend_analyzer.get_dividend_info(symbol)
                                if div_info and div_info['dividend_yield'] is not None:
                                    weekly_income = dividend_analyzer.calculate_dividend_income(
                                        investment_amount,
                                        div_info['dividend_yield'],
                                        'weekly'
                                    )
                                    st.metric(f"{symbol}", f"${weekly_income:,.2f}")
                            except Exception as e:
                                pass
            else:
                st.warning("❌ ไม่สามารถดึงข้อมูลปันผล กรุณาตรวจสอบสัญลักษณ์หุ้น")
        else:
            st.info("👈 เลือกหุ้นปันผลจากตัวเลือกด้านบน หรือ ใช้ปุ่มค้นหาเพื่อค้นหาอัตโนมัติ")

    
    st.divider()
    
    # Period selection
    period = st.selectbox(
        "ระยะเวลาวิเคราะห์",
        ['1mo', '3mo', '6mo', '1y', '2y']
    )
    
    # Confidence threshold (keep this as backup, main is in sidebar)
    min_confidence_threshold = st.slider(
        "ระดับความเชื่อมั่นสัญญาณต่ำสุด",
        min_value=0.0,
        max_value=1.0,
        value=0.6,
        step=0.05
    )
    
    # Refresh button
    if st.button("🔄 รีเฟรชการวิเคราะห์"):
        st.session_state.refresh = True

# Initialize app
app = StockAnalyzerApp()

# ========================
# PAGE ROUTING
# ========================

# PAGE 1: Dashboard (Portfolio Dashboard with Real-time FX)
if st.session_state.current_page == "Dashboard":
    st.header("📊 Dashboard - ภาพรวมพอร์ตโฟลิโอ")
    
    # Import real-time exchange rate
    try:
        from src.utils.exchange_rate import ExchangeRateFetcher
        fx_fetcher = ExchangeRateFetcher()
        rate_info = fx_fetcher.get_rate_with_source()
        usd_to_thb = rate_info['rate']
        
        # Display FX info
        col_fx1, col_fx2, col_fx3 = st.columns(3)
        with col_fx1:
            st.metric("💱 อัตราแลกเปลี่ยน USD/THB", f"฿{usd_to_thb:.4f}")
        with col_fx2:
            st.metric("📡 แหล่งข้อมูล", rate_info['source'])
        with col_fx3:
            st.metric("🕐 อัปเดต", rate_info['timestamp'])
    except:
        usd_to_thb = 35.5
        st.warning(f"⚠️ ใช้อัตราแลกเปลี่ยนเริ่มต้น: ฿{usd_to_thb:.2f}/USD")
    
    st.divider()
    
    # Initialize Portfolio Manager
    portfolio_mgr = PortfolioManager()
    portfolio_stocks = portfolio_mgr.get_symbols()
    
    if not portfolio_stocks:
        st.info("📭 ยังไม่มีหุ้นในพอร์ต กรุณาเพิ่มหุ้นในเมนู Portfolio ก่อน")
    else:
        # Fetch current prices
        import yfinance as yf
        current_prices = {}
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, symbol in enumerate(portfolio_stocks):
            try:
                status_text.text(f"กำลังดึงข้อมูล {symbol}...")
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period='1d')
                if not hist.empty:
                    current_prices[symbol] = hist['Close'].iloc[-1]
                else:
                    stock_info = portfolio_mgr.get_stock(symbol)
                    current_prices[symbol] = stock_info['buy_price']
            except:
                stock_info = portfolio_mgr.get_stock(symbol)
                current_prices[symbol] = stock_info['buy_price']
            
            progress_bar.progress((i + 1) / len(portfolio_stocks))
        
        status_text.empty()
        progress_bar.empty()
        
        # Calculate portfolio value
        portfolio_data = portfolio_mgr.calculate_portfolio_value(current_prices)
        
        # Display summary metrics (both USD and THB)
        st.markdown("#### 💵 สกุลเงินดอลลาร์ (USD)")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 มูลค่ารวม",
                f"${portfolio_data['total_value']:,.2f}",
                delta=f"${portfolio_data['total_profit_loss']:,.2f}"
            )
        
        with col2:
            st.metric(
                "💵 ต้นทุนรวม",
                f"${portfolio_data['total_cost']:,.2f}"
            )
        
        with col3:
            profit_color = "normal" if portfolio_data['total_profit_loss'] >= 0 else "inverse"
            st.metric(
                "📈 กำไร/ขาดทุน",
                f"${portfolio_data['total_profit_loss']:,.2f}",
                delta=f"{portfolio_data['total_profit_loss_pct']:.2f}%",
                delta_color=profit_color
            )
        
        with col4:
            st.metric(
                "🎯 จำนวนหุ้น",
                f"{portfolio_data['num_stocks']} ตัว"
            )
        
        st.divider()
        
        # THB Row
        total_value_thb = portfolio_data['total_value'] * usd_to_thb
        total_cost_thb = portfolio_data['total_cost'] * usd_to_thb
        total_profit_loss_thb = portfolio_data['total_profit_loss'] * usd_to_thb
        
        st.markdown(f"#### 💰 สกุลเงินบาท (THB) - อัตรา {usd_to_thb:.4f}")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "💰 มูลค่ารวม",
                f"฿{total_value_thb:,.2f}",
                delta=f"฿{total_profit_loss_thb:,.2f}"
            )
        
        with col2:
            st.metric(
                "💵 ต้นทุนรวม",
                f"฿{total_cost_thb:,.2f}"
            )
        
        with col3:
            profit_color = "normal" if portfolio_data['total_profit_loss'] >= 0 else "inverse"
            st.metric(
                "📈 กำไร/ขาดทุน",
                f"฿{total_profit_loss_thb:,.2f}",
                delta=f"{portfolio_data['total_profit_loss_pct']:.2f}%",
                delta_color=profit_color
            )
        
        with col4:
            st.metric(
                "💱 อัตราแลกเปลี่ยน",
                f"฿{usd_to_thb:.4f}/USD"
            )
        
        st.divider()
        
        # Display individual stocks (13-column dual currency table)
        st.markdown("#### 📋 รายละเอียดหุ้นแต่ละตัว")
        
        # Create DataFrame
        import pandas as pd
        df_stocks = pd.DataFrame(portfolio_data['stocks'])
        
        # Create display DataFrame with dual currency
        df_display = pd.DataFrame()
        df_display['รหัสหุ้น'] = df_stocks['symbol']
        df_display['จำนวน'] = df_stocks['shares'].apply(lambda x: f"{x:.2f}")
        df_display['ราคาซื้อ (USD)'] = df_stocks['buy_price'].apply(lambda x: f"${x:.2f}")
        df_display['ราคาซื้อ (THB)'] = df_stocks['buy_price'].apply(lambda x: f"฿{x*usd_to_thb:.2f}")
        df_display['ราคาปัจจุบัน (USD)'] = df_stocks['current_price'].apply(lambda x: f"${x:.2f}")
        df_display['ราคาปัจจุบัน (THB)'] = df_stocks['current_price'].apply(lambda x: f"฿{x*usd_to_thb:.2f}")
        df_display['ต้นทุน (USD)'] = df_stocks['cost'].apply(lambda x: f"${x:,.2f}")
        df_display['ต้นทุน (THB)'] = df_stocks['cost'].apply(lambda x: f"฿{x*usd_to_thb:,.2f}")
        df_display['มูลค่า (USD)'] = df_stocks['value'].apply(lambda x: f"${x:,.2f}")
        df_display['มูลค่า (THB)'] = df_stocks['value'].apply(lambda x: f"฿{x*usd_to_thb:,.2f}")
        df_display['กำไร/ขาดทุน (USD)'] = df_stocks.apply(
            lambda row: f"{'💸' if row['profit_loss'] >= 0 else '🔴'} ${abs(row['profit_loss']):,.2f}",
            axis=1
        )
        df_display['กำไร/ขาดทุน (THB)'] = df_stocks.apply(
            lambda row: f"{'💸' if row['profit_loss'] >= 0 else '🔴'} ฿{abs(row['profit_loss']*usd_to_thb):,.2f}",
            axis=1
        )
        df_display['% เปลี่ยนแปลง'] = df_stocks.apply(
            lambda row: f"{'↗️' if row['profit_loss_pct'] >= 0 else '↘️'} {abs(row['profit_loss_pct']):.2f}%",
            axis=1
        )
        
        st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        # Portfolio composition chart
        st.markdown("#### 📊 สัดส่วนการลงทุน")
        
        import plotly.graph_objects as go
        fig = go.Figure(data=[go.Pie(
            labels=[s['symbol'] for s in portfolio_data['stocks']],
            values=[s['value'] for s in portfolio_data['stocks']],
            hole=.3,
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title="สัดส่วนมูลค่าหุ้นในพอร์ต",
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Performance chart
        st.markdown("#### 📈 ผลการลงทุนแต่ละตัว")
        
        symbols = [s['symbol'] for s in portfolio_data['stocks']]
        profit_pcts = [s['profit_loss_pct'] for s in portfolio_data['stocks']]
        
        colors = ['green' if p >= 0 else 'red' for p in profit_pcts]
        
        fig2 = go.Figure(data=[go.Bar(
            x=symbols,
            y=profit_pcts,
            marker_color=colors,
            text=[f"{p:.2f}%" for p in profit_pcts],
            textposition='auto'
        )])
        
        fig2.update_layout(
            title="ผลตอบแทนแต่ละหุ้น (%)",
            xaxis_title="รหัสหุ้น",
            yaxis_title="% กำไร/ขาดทุน",
            height=400
        )
        
        st.plotly_chart(fig2, use_container_width=True)

# PAGE 2: Portfolio Management
elif st.session_state.current_page == "Portfolio":
    st.header("💼 จัดการ Portfolio")
    st.markdown("### เพิ่ม แก้ไข หรือลบหุ้นในพอร์ต")
    
    # Initialize Portfolio Manager
    portfolio_mgr = PortfolioManager()
    
    # Create two columns for layout
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("➕ เพิ่มหุ้นใหม่")
        
        with st.form("add_stock_form", clear_on_submit=True):
            new_symbol = st.text_input("รหัสหุ้น (เช่น AAPL)", key="new_symbol").upper()
            new_shares = st.number_input("จำนวนหุ้น", min_value=0.01, value=1.0, step=0.01, key="new_shares")
            new_price = st.number_input("ราคาซื้อ ($)", min_value=0.01, value=100.0, step=0.01, key="new_price")
            new_date = st.date_input("วันที่ซื้อ", value=datetime.now(), key="new_date")
            new_notes = st.text_area("หมายเหตุ (ถ้ามี)", key="new_notes")
            
            submitted = st.form_submit_button("✅ เพิ่มหุ้น")
            
            if submitted and new_symbol:
                if portfolio_mgr.add_stock(
                    new_symbol, 
                    new_shares, 
                    new_price, 
                    new_date.strftime("%Y-%m-%d"),
                    new_notes
                ):
                    st.success(f"✅ เพิ่มหุ้น {new_symbol} สำเร็จ!")
                    st.rerun()
                else:
                    st.error("❌ เกิดข้อผิดพลาดในการเพิ่มหุ้น")
        
        st.divider()
        
        st.subheader("🗑️ ลบหุ้น")
        portfolio_stocks = portfolio_mgr.get_symbols()
        
        if portfolio_stocks:
            with st.form("remove_stock_form"):
                remove_symbol = st.selectbox("เลือกหุ้นที่ต้องการลบ", portfolio_stocks, key="remove_symbol")
                remove_submitted = st.form_submit_button("🗑️ ลบหุ้น", type="secondary")
                
                if remove_submitted:
                    if portfolio_mgr.remove_stock(remove_symbol):
                        st.success(f"✅ ลบหุ้น {remove_symbol} สำเร็จ!")
                        st.rerun()
                    else:
                        st.error("❌ เกิดข้อผิดพลาดในการลบหุ้น")
        else:
            st.info("📭 ยังไม่มีหุ้นในพอร์ต")
    
    with col_right:
        st.subheader("📋 หุ้นในพอร์ตปัจจุบัน")
        
        portfolio = portfolio_mgr.get_portfolio()
        
        if portfolio:
            for stock in portfolio:
                with st.expander(f"📊 {stock['symbol']} - {stock['shares']:.2f} หุ้น @ ${stock['buy_price']:.2f}"):
                    st.write(f"**วันที่ซื้อ:** {stock.get('buy_date', 'N/A')}")
                    st.write(f"**ต้นทุนรวม:** ${stock['shares'] * stock['buy_price']:,.2f}")
                    st.write(f"**หมายเหตุ:** {stock.get('notes', '-')}")
                    st.write(f"**อัพเดทล่าสุด:** {stock.get('last_updated', 'N/A')}")
                    
                    st.divider()
                    
                    # Edit form
                    with st.form(f"edit_form_{stock['symbol']}"):
                        st.markdown("**แก้ไขข้อมูล**")
                        edit_shares = st.number_input("จำนวนหุ้น", min_value=0.01, value=stock['shares'], step=0.01, key=f"edit_shares_{stock['symbol']}")
                        edit_price = st.number_input("ราคาซื้อ ($)", min_value=0.01, value=stock['buy_price'], step=0.01, key=f"edit_price_{stock['symbol']}")
                        edit_notes = st.text_area("หมายเหตุ", value=stock.get('notes', ''), key=f"edit_notes_{stock['symbol']}")
                        
                        edit_submitted = st.form_submit_button("💾 บันทึกการแก้ไข")
                        
                        if edit_submitted:
                            if portfolio_mgr.update_stock(stock['symbol'], edit_shares, edit_price, edit_notes):
                                st.success(f"✅ อัพเดทข้อมูล {stock['symbol']} สำเร็จ!")
                                st.rerun()
                            else:
                                st.error("❌ เกิดข้อผิดพลาดในการอัพเดท")
            
            st.divider()
            
            # Export/Import portfolio
            import pandas as pd
            col_export, col_clear = st.columns(2)
            
            with col_export:
                st.download_button(
                    label="📥 Export Portfolio (JSON)",
                    data=pd.DataFrame(portfolio).to_json(orient='records', indent=2),
                    file_name=f"portfolio_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json"
                )
            
            with col_clear:
                if st.button("🗑️ ล้างพอร์ตทั้งหมด", type="secondary"):
                    if st.button("⚠️ ยืนยันการล้างข้อมูล", type="primary"):
                        if portfolio_mgr.clear_portfolio():
                            st.success("✅ ล้างพอร์ตสำเร็จ!")
                            st.rerun()
        else:
            st.info("📭 ยังไม่มีหุ้นในพอร์ต กรุณาเพิ่มหุ้นด้านซ้าย")

# PAGE 3: Stock Analysis (Original Content)
elif st.session_state.current_page == "วิเคราะห์หุ้น":
    st.header("📈 วิเคราะห์หุ้น")
    
    # Display summary info if stocks selected
    if selected_stocks:
        col_summary1, col_summary2, col_summary3 = st.columns(3)
        with col_summary1:
            st.metric("📊 จำนวนหุ้นที่วิเคราะห์", len(selected_stocks))
        with col_summary2:
            st.metric("📅 ช่วงเวลา", period)
        with col_summary3:
            st.metric("🎯 ความมั่นใจขั้นต่ำ", f"{min_confidence}%")
        
        st.divider()
        
        # Tabs for stock analysis (5 tabs)
        tab0, tab1, tab2, tab3, tab4 = st.tabs(
            ["📈 การวิเคราะห์ทั้งหมด", "💚 สัญญาณซื้อ", "📉 สัญญาณขาย", "🔥 หุ้นฮอต", "📊 รายละเอียดหุ้น"]
        )
        
        # Tab 0: Analysis
        with tab0:
            st.header("📈 วิเคราะห์เทคนิค")
            
            # Quick filters
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                show_chart = st.checkbox("� แสดงกราฟ", value=True)
            with col_filter2:
                sort_by = st.selectbox(
                    "เรียงลำดับ",
                    ["ตามลำดับที่เลือก", "ตามราคา (สูง→ต่ำ)", "ตามราคา (ต่ำ→สูง)", "ตาม RSI (สูง→ต่ำ)"],
                    key="sort_analysis"
                )
            
            st.divider()
            
            cols = st.columns(len(selected_stocks) if len(selected_stocks) <= 3 else 3)
            
            for idx, symbol in enumerate(selected_stocks):
                with cols[idx % len(cols)]:
                    with st.spinner(f"🔄 กำลังวิเคราะห์ {symbol}..."):
                        result = app.analyze_single_stock(symbol, period=period)
                        

                        if result:
                            technical = result['technical']
                            signals = result['signals']
                            
                            # Create metric cards with better styling and visual indicators
                            st.markdown(f"### {symbol}")
                            
                            col_price, col_rsi, col_signal = st.columns(3)
                            
                            with col_price:
                                st.metric(
                                    "💰 ราคา",
                                    f"${technical['latest_price']:.2f}",
                                    delta=None
                                )
                            
                            with col_rsi:
                                rsi_value = technical['rsi']
                                rsi_status = "〽️ ขายมาก" if rsi_value > 70 else \
                                            "✅ ซื้อมาก" if rsi_value < 30 else \
                                            "🆗 ปกติ"
                                st.metric("〽️ RSI", f"{rsi_value:.1f}", delta=rsi_status)
                            
                            with col_signal:
                                if signals['buy']:
                                    signal_display = '✅ ซื้อ'
                                elif signals['sell']:
                                    signal_display = '⛔ ขาย'
                                else:
                                    signal_display = '⏸️ คงตำแหน่ง'
                                st.metric("📈 สัญญาณ", signal_display, delta=f"{signals['confidence']:.1%}")
                            
                            st.divider()
                            
                            # Price levels in expandable section
                            with st.expander("📋 ตัวชี้วัดเพิ่มเติม"):
                                col_left, col_right = st.columns(2)
                                with col_left:
                                    st.write("**📈 Moving Averages:**")
                                    st.write(f"  📍 SMA20: ${technical['sma_20']:.2f}")
                                    st.write(f"  📍 SMA50: ${technical['sma_50']:.2f}")
                                    st.write(f"  📍 SMA200: ${technical['sma_200']:.2f}")
                                
                                with col_right:
                                    st.write("**⚡ Volatility & Momentum:**")
                                    st.write(f"  📈 ATR: {technical['atr']:.4f}")
                                    st.write(f"  📊 MACD: {technical['macd']:.6f}")
                                
                                # Reasons
                                st.write("**🎯 เหตุผลสัญญาณ:**")
                                for i, reason in enumerate(signals['reasons'][:3], 1):
                                    st.write(f"  {i}. {reason}")
                            
                            st.divider()
                        else:
                            st.error(f"❌ ไม่สามารถดึงข้อมูล {symbol} - อาจเป็นหุ้นที่ delisted หรือสัญลักษณ์ไม่ถูกต้อง")
        
        # Tab 2: Buy Signals
        with tab1:
            st.header("💚 โอกาสในการซื้อ")
            
            # Filter options
            col_filter_buy1, col_filter_buy2 = st.columns(2)
            with col_filter_buy1:
                min_confidence_buy = st.slider(
                    "ความมั่นใจขั้นต่ำ",
                    min_value=30,
                    max_value=100,
                    value=min_confidence,
                    step=5,
                    key="buy_confidence_filter"
                )
            with col_filter_buy2:
                max_price_buy = st.number_input(
                    "ราคาสูงสุด ($)",
                    min_value=0.0,
                    value=1000.0,
                    step=10.0,
                    key="buy_price_filter"
                )
            
            st.divider()
            
            buy_opps = app.find_buy_opportunities(selected_stocks, min_confidence_buy / 100)
            
            if buy_opps:
                # Display as cards
                num_cols = min(len(buy_opps), 3)
                cols = st.columns(num_cols)
                
                for idx, opp in enumerate(buy_opps):
                    with cols[idx % num_cols]:
                        with st.container(border=True):
                            # Header with signal emoji
                            st.markdown(f"## 💸 {opp['symbol']}")
                            
                            # Confidence bar
                            confidence_pct = opp['confidence']
                            st.progress(confidence_pct, text=f"ความมั่นใจ: {confidence_pct:.1%}")
                            
                            # Key metrics in columns
                            metric_col1, metric_col2 = st.columns(2)
                            with metric_col1:
                                st.metric("ราคาเข้า", f"${opp.get('entry_price', opp.get('latest_price', 0)):.2f}")
                            with metric_col2:
                                st.metric("Target", f"${opp.get('target_price', 0):.2f}")
                            
                            # Stop Loss
                            st.metric("Stop Loss", f"${opp.get('stop_loss', 0):.2f}")
                            
                            # Reason with icon
                            reason_text = ", ".join(opp.get('reasons', []))
                            st.info(f"📌 **เหตุผล:** {reason_text}")
            else:
                st.info("ℹ️ ยังไม่มีสัญญาณซื้อในขณะนี้")
        
        # Tab 3: Sell Signals
        with tab2:
            st.header("📉 โอกาสในการขาย")
            
            # Filter options
            col_filter_sell1, col_filter_sell2 = st.columns(2)
            with col_filter_sell1:
                min_confidence_sell = st.slider(
                    "ความมั่นใจขั้นต่ำ",
                    min_value=30,
                    max_value=100,
                    value=min_confidence,
                    step=5,
                    key="sell_confidence_filter"
                )
            with col_filter_sell2:
                max_loss_sell = st.number_input(
                    "ขาดทุนสูงสุด (%)",
                    min_value=0.0,
                    value=100.0,
                    step=5.0,
                    key="sell_loss_filter"
                )
            
            st.divider()
            
            sell_opps = app.find_sell_opportunities(selected_stocks, min_confidence_sell / 100)
            
            if sell_opps:
                # Display as cards
                num_cols = min(len(sell_opps), 3)
                cols = st.columns(num_cols)
                
                for idx, opp in enumerate(sell_opps):
                    with cols[idx % num_cols]:
                        with st.container(border=True):
                            # Header with signal emoji
                            st.markdown(f"## 🔴 {opp['symbol']}")
                            
                            # Confidence bar
                            confidence_pct = opp['confidence']
                            st.progress(confidence_pct, text=f"ความมั่นใจ: {confidence_pct:.1%}")
                            
                            # Key metrics in columns
                            metric_col1, metric_col2 = st.columns(2)
                            with metric_col1:
                                st.metric("ราคาปัจจุบัน", f"${opp.get('latest_price', 0):.2f}")
                            with metric_col2:
                                st.metric("ราคาออก", f"${opp.get('exit_price', 0):.2f}")
                            
                            # Target and Stop Loss
                            metric_col3, metric_col4 = st.columns(2)
                            with metric_col3:
                                st.metric("Target ขาย", f"${opp.get('target_price', 0):.2f}")
                            with metric_col4:
                                st.metric("Stop Loss", f"${opp.get('stop_loss', 0):.2f}")
                            
                            # Reason with warning style
                            reason_text = ", ".join(opp.get('reasons', []))
                            st.warning(f"📌 **เหตุผล:** {reason_text}")
            else:
                st.info("ℹ️ ยังไม่มีสัญญาณขายในขณะนี้")
        
        # Tab 4: Hot Stocks
        with tab3:
            st.header("🔥 หุ้นฮอต")
            st.write("สรุปภาพรวมสัญญาณการซื้อขาย")
            
            try:
                hot = app.get_hot_stocks(selected_stocks)
                
                # แสดงเฉพาะสถิติสรุป
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("💸 ซื้อแรง", len(hot.get('strong_buys', [])))
                    if hot.get('strong_buys'):
                        st.caption(", ".join([s['symbol'] for s in hot['strong_buys']]))
                
                with col2:
                    st.metric("� ซื้อ", len(hot.get('buys', [])))
                    if hot.get('buys'):
                        st.caption(", ".join([s['symbol'] for s in hot['buys']]))
                
                with col3:
                    st.metric("📉 ขาย", len(hot.get('sells', [])))
                    if hot.get('sells'):
                        st.caption(", ".join([s['symbol'] for s in hot['sells']]))
                
                with col4:
                    st.metric("🔴 ขายแรง", len(hot.get('strong_sells', [])))
                    if hot.get('strong_sells'):
                        st.caption(", ".join([s['symbol'] for s in hot['strong_sells']]))
                
                st.divider()
                
                st.info("💡 **คำแนะนำ:** ดูรายละเอียดสัญญาณซื้อที่แถบ '💚 สัญญาณซื้อ' และสัญญาณขายที่แถบ '📉 สัญญาณขาย'")
                
            except Exception as e:
                st.error(f"⚠️ เกิดข้อผิดพลาด: {str(e)}")
        
        # Tab 5: Stock Details
        with tab4:
            st.header("📊 รายละเอียดหุ้นแบบละเอียด")
            
            # Select stock for details
            detail_stock = st.selectbox(
                "เลือกหุ้นเพื่อดูรายละเอียด",
                selected_stocks,
                key="detail_stock_select"
            )
            
            if detail_stock:
                provider = StockDetailsProvider()
                widget = StockInfoWidget()
                
                # Get stock details
                with st.spinner(f"🔄 กำลังดึงข้อมูล {detail_stock}..."):
                    details = provider.get_enhanced_stock_info(detail_stock)
                    historical_data = provider.get_historical_data(detail_stock, period='1y')
                    price_change = provider.calculate_price_change(detail_stock, period='1y')
                
                if details:
                    # Create tabs for different sections
                    detail_tab1, detail_tab2, detail_tab3, detail_tab4, detail_tab5 = st.tabs([
                        "📋 พื้นฐาน", 
                        "💹 มูลค่า", 
                        "📊 การเงิน", 
                        "📈 กราฟ",
                        "🎯 การวิเคราะห์"
                    ])
                    
                    # Tab 1: Basic Information
                    with detail_tab1:
                        st.subheader("📋 ข้อมูลพื้นฐาน")
                        widget.display_stock_fundamentals(detail_stock)
                        
                        st.divider()
                        
                        st.subheader("🏢 จำแนกธุรกิจ")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.info(f"**ส่วนชั้น (Sector)**: {details.get('sector', 'ไม่ทราบ')}")
                            st.warning(f"**อุตสาหกรรม (Industry)**: {details.get('industry', 'ไม่ทราบ')}")
                        
                        with col2:
                            market_cap = details.get('market_cap', 'ไม่ทราบ')
                            market_category = provider.get_market_category(market_cap)
                            st.success(f"**หมวดหมู่ตลาด**: {market_category}")
                            st.metric("Market Cap", provider.format_market_cap(market_cap))
                        
                        st.divider()
                        
                        st.subheader("📝 รายละเอียดธุรกิจ")
                        st.write(details.get('description', 'ไม่มีข้อมูล'))
                    
                    # Tab 2: Valuation
                    with detail_tab2:
                        widget.display_valuation_analysis(detail_stock)
                        
                        st.divider()
                        
                        st.subheader("💰 ราคา & ผลงาน")
                        
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                "ราคาปัจจุบัน",
                                f"${details.get('current_price', 'N/A')}",
                                "LIVE"
                            )
                        
                        with col2:
                            st.metric(
                                "ราคาปิดก่อนหน้า",
                                f"${details.get('previous_close', 'N/A')}"
                            )
                        
                        with col3:
                            if price_change:
                                st.metric(
                                    "เปลี่ยนแปลง 1 ปี",
                                    f"{price_change['change_percent']:.2f}%"
                                )
                        
                        with col4:
                            avg_vol = details.get('avg_volume', 0)
                            if isinstance(avg_vol, (int, float)) and avg_vol != 0:
                                avg_vol_display = f"{int(avg_vol):,.0f}"
                            else:
                                avg_vol_display = "N/A"
                            st.metric(
                                "ปริมาณหุ้น (เฉลี่ย)",
                                avg_vol_display
                            )
                        
                        st.divider()
                        
                        st.subheader("📈 ช่วง 52 สัปดาห์")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric(
                                "ราคาสูงสุด",
                                f"${details.get('fifty_two_week_high', 'N/A')}"
                            )
                        
                        with col2:
                            st.metric(
                                "ราคาต่ำสุด",
                                f"${details.get('fifty_two_week_low', 'N/A')}"
                            )
                    
                    # Tab 3: Financial Health
                    with detail_tab3:
                        widget.display_financial_health(detail_stock)
                    
                    # Tab 4: Charts
                    with detail_tab4:
                        if historical_data is not None and not historical_data.empty:
                            st.subheader("📈 กราฟราคาประวัติศาสตร์ (1 ปี)")
                            
                            # Create candlestick chart
                            fig = go.Figure(data=[go.Candlestick(
                                x=historical_data.index,
                                open=historical_data['Open'],
                                high=historical_data['High'],
                                low=historical_data['Low'],
                                close=historical_data['Close']
                            )])
                            
                            fig.update_layout(
                                title=f"กราฟราคา {detail_stock} (1 ปี)",
                                yaxis_title="ราคา (USD)",
                                xaxis_title="วันที่",
                                template="plotly_dark",
                                height=500,
                                xaxis_rangeslider_visible=False
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Volume chart
                            fig_volume = go.Figure(data=[go.Bar(
                                x=historical_data.index,
                                y=historical_data['Volume'],
                                name='ปริมาณ',
                                marker=dict(color='rgba(0, 150, 200, 0.7)')
                            )])
                            
                            fig_volume.update_layout(
                                title=f"ปริมาณการซื้อขาย {detail_stock}",
                                yaxis_title="ปริมาณหุ้น",
                                xaxis_title="วันที่",
                                template="plotly_dark",
                                height=300,
                                showlegend=False
                            )
                            
                            st.plotly_chart(fig_volume, use_container_width=True)
                            
                            st.divider()
                            
                            # Moving Averages
                            historical_data['SMA20'] = historical_data['Close'].rolling(window=20).mean()
                            historical_data['SMA50'] = historical_data['Close'].rolling(window=50).mean()
                            historical_data['SMA200'] = historical_data['Close'].rolling(window=200).mean()
                            
                            fig_ma = go.Figure()
                            
                            fig_ma.add_trace(go.Scatter(
                                x=historical_data.index,
                                y=historical_data['Close'],
                                name='ราคาปิด',
                                line=dict(color='white', width=2)
                            ))
                            
                            fig_ma.add_trace(go.Scatter(
                                x=historical_data.index,
                                y=historical_data['SMA20'],
                                name='SMA20',
                                line=dict(color='cyan', width=1, dash='dash')
                            ))
                            
                            fig_ma.add_trace(go.Scatter(
                                x=historical_data.index,
                                y=historical_data['SMA50'],
                                name='SMA50',
                                line=dict(color='yellow', width=1, dash='dash')
                            ))
                            
                            fig_ma.add_trace(go.Scatter(
                                x=historical_data.index,
                                y=historical_data['SMA200'],
                                name='SMA200',
                                line=dict(color='red', width=1, dash='dash')
                            ))
                            
                            fig_ma.update_layout(
                                title=f"ค่าเฉลี่ยเคลื่อนที่ {detail_stock}",
                                yaxis_title="ราคา (USD)",
                                xaxis_title="วันที่",
                                template="plotly_dark",
                                height=400,
                                hovermode='x unified'
                            )
                            
                            st.plotly_chart(fig_ma, use_container_width=True)
                        else:
                            st.warning("ไม่สามารถดึงข้อมูลราคาประวัติศาสตร์ได้")
                    
                    # Tab 5: Analysis & Recommendation
                    with detail_tab5:
                        widget.display_valuation_recommendation(detail_stock)
                        
                        st.divider()
                        
                        st.subheader("📚 ความหมายของตัวชี้วัด")
                        
                        with st.expander("💡 P/E Ratio คืออะไร?"):
                            st.write("""
                            **P/E Ratio = ราคา / กำไรต่อหุ้น**
                            
                            - แสดงว่านักลงทุนยินดีจ่ายกี่เท่าของกำไรต่อหุ้น
                            - ยิ่งต่ำยิ่งดี (ราคาถูก) แต่ต้องดู growth ด้วย
                            - ใช้เปรียบเทียบหุ้นในอุตสาหกรรมเดียวกัน
                            """)
                        
                        with st.expander("💡 ROE คืออะไร?"):
                            st.write("""
                            **ROE = กำไรสุทธิ / ส่วนของผู้ถือหุ้น**
                            
                            - แสดงว่าบริษัทใช้เงินของผู้ถือหุ้นได้มีประสิทธิภาพเพียงใด
                            - ยิ่งสูงยิ่งดี (> 15% ถือว่าดี)
                            - ใช้ดูความสามารถในการหารายได้
                            """)
                        
                        with st.expander("💡 Debt-to-Equity คืออะไร?"):
                            st.write("""
                            **Debt-to-Equity = หนี้สิน / ส่วนของผู้ถือหุ้น**
                            
                            - แสดงสัดส่วนหนี้สินเมื่อเทียบกับเงินทุน
                            - ยิ่งต่ำยิ่งดี (< 1.0 ถือว่าปลอดภัย)
                            - บริษัทที่มีหนี้สินสูง มีความเสี่ยง
                            """)
                        
                        with st.expander("💡 Dividend Yield คืออะไร?"):
                            st.write("""
                            **Dividend Yield = เงินปันผลประจำปี / ราคาหุ้น**
                            
                            - แสดงผลตอบแทนจากเงินปันผล
                            - ยิ่งสูงยิ่งดี (> 3% ถือว่าดี)
                            - แต่ต้องตรวจสอบว่าบริษัทสามารถจ่ายอย่างต่อเนื่องได้
                            """)
        
        # Display message if no stocks selected
    else:
        st.info("👈 กรุณาเลือกหุ้นจากเมนูด้านซ้าย หรือเลือกเมนู Dashboard/Portfolio")
    
# Display message if not in Stock Analysis page
else:
    pass  # Dashboard and Portfolio pages are already handled above

# Footer
st.divider()
st.markdown("""
---
**ข้อปฏิเสธ**: นี่คือเพื่อวัตถุประสงค์ทางการศึกษาเท่านั้น ไม่ใช่คำแนะนำทางการเงิน  
อัปเดตล่าสุด: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


