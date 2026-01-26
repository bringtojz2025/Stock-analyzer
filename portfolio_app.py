"""
Portfolio Dashboard Application
หน้า Dashboard และ Portfolio Management แยกต่างหาก
"""

import streamlit as st
from datetime import datetime
import sys
import os
import plotly.graph_objects as go
import yfinance as yf
import pandas as pd

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.portfolio.manager import PortfolioManager
from src.utils.exchange_rate import ExchangeRateFetcher

# ตั้งค่าเพจ
st.set_page_config(
    page_title="Portfolio Dashboard - Stock Analyzer",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
page = st.sidebar.radio(
    "📊 เลือกหน้า",
    ["🏠 Dashboard", "💼 Portfolio Management"],
    key="portfolio_nav"
)

st.sidebar.divider()
st.sidebar.markdown("### 💡 คำแนะนำ")
if page == "🏠 Dashboard":
    st.sidebar.info("""
    **Dashboard** แสดง:
    - ภาพรวมพอร์ต
    - มูลค่า USD + THB
    - กราฟวิเคราะห์
    - ตารางรายละเอียด
    """)
else:
    st.sidebar.info("""
    **Portfolio Management** สำหรับ:
    - เพิ่มหุ้นใหม่
    - แก้ไขข้อมูล
    - ลบหุ้น
    - Export ข้อมูล
    """)

# Initialize managers
portfolio_mgr = PortfolioManager()
fx_fetcher = ExchangeRateFetcher()

# ===========================
# Page 1: Dashboard
# ===========================
if page == "🏠 Dashboard":
    st.title("🏠 Portfolio Dashboard")
    st.markdown("### ภาพรวมพอร์ตการลงทุนของคุณ")
    
    # Fetch real-time exchange rate
    with st.spinner("🔄 กำลังดึงอัตราแลกเปลี่ยนแบบ Real-time..."):
        fx_data = fx_fetcher.get_rate_with_source()
        usd_to_thb = fx_data['rate']
    
    # Display exchange rate info
    col_fx1, col_fx2, col_fx3 = st.columns([2, 1, 1])
    with col_fx1:
        st.metric(
            "💱 อัตราแลกเปลี่ยน Real-time",
            f"฿{usd_to_thb:.4f}/USD",
            delta="Live" if fx_data['is_live'] else "Default"
        )
    with col_fx2:
        st.info(f"📡 {fx_data['source']}")
    with col_fx3:
        st.caption(f"🕐 {fx_data['timestamp']}")
    
    st.divider()
    
    portfolio_stocks = portfolio_mgr.get_symbols()
    
    if not portfolio_stocks:
        st.info("📭 ยังไม่มีหุ้นในพอร์ต กรุณาไปที่ 'Portfolio Management' เพื่อเพิ่มหุ้น")
    else:
        # Fetch current prices
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
        
        # Display summary metrics
        st.markdown("#### 📊 สรุปภาพรวม")
        
        # Calculate THB values
        total_value_thb = portfolio_data['total_value'] * usd_to_thb
        total_cost_thb = portfolio_data['total_cost'] * usd_to_thb
        total_profit_loss_thb = portfolio_data['total_profit_loss'] * usd_to_thb
        
        # USD Row
        st.markdown("##### 💵 สกุลเงินดอลลาร์ (USD)")
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
        st.markdown(f"##### 💰 สกุลเงินบาท (THB) - อัตรา {usd_to_thb:.4f}")
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
        
        # Display individual stocks
        st.markdown("#### 📋 รายละเอียดหุ้นแต่ละตัว")
        
        # Create DataFrame for better display
        df_stocks = pd.DataFrame(portfolio_data['stocks'])
        
        # Format columns with BOTH USD and THB
        df_display = df_stocks.copy()
        df_display['shares'] = df_display['shares'].apply(lambda x: f"{x:.2f}")
        
        # Buy Price - USD + THB
        df_display['buy_price_usd'] = df_display['buy_price'].apply(lambda x: f"${x:.2f}")
        df_display['buy_price_thb'] = df_display['buy_price'].apply(lambda x: f"฿{x*usd_to_thb:,.2f}")
        
        # Current Price - USD + THB
        df_display['current_price_usd'] = df_display['current_price'].apply(lambda x: f"${x:.2f}")
        df_display['current_price_thb'] = df_display['current_price'].apply(lambda x: f"฿{x*usd_to_thb:,.2f}")
        
        # Cost - USD + THB
        df_display['cost_usd'] = df_display['cost'].apply(lambda x: f"${x:,.2f}")
        df_display['cost_thb'] = df_display['cost'].apply(lambda x: f"฿{x*usd_to_thb:,.2f}")
        
        # Value - USD + THB
        df_display['value_usd'] = df_display['value'].apply(lambda x: f"${x:,.2f}")
        df_display['value_thb'] = df_display['value'].apply(lambda x: f"฿{x*usd_to_thb:,.2f}")
        
        # Profit/Loss - USD + THB
        df_display['profit_loss_usd'] = df_display.apply(
            lambda row: f"{'🟢' if row['profit_loss'] >= 0 else '🔴'} ${abs(row['profit_loss']):,.2f}",
            axis=1
        )
        df_display['profit_loss_thb'] = df_display.apply(
            lambda row: f"{'🟢' if row['profit_loss'] >= 0 else '🔴'} ฿{abs(row['profit_loss']*usd_to_thb):,.2f}",
            axis=1
        )
        
        df_display['profit_loss_pct'] = df_display.apply(
            lambda row: f"{'↗️' if row['profit_loss_pct'] >= 0 else '↘️'} {abs(row['profit_loss_pct']):.2f}%",
            axis=1
        )
        
        # Rename columns to Thai
        df_display = df_display.rename(columns={
            'symbol': 'รหัสหุ้น',
            'shares': 'จำนวน',
            'buy_price_usd': 'ราคาซื้อ (USD)',
            'buy_price_thb': 'ราคาซื้อ (THB)',
            'current_price_usd': 'ราคาปัจจุบัน (USD)',
            'current_price_thb': 'ราคาปัจจุบัน (THB)',
            'cost_usd': 'ต้นทุน (USD)',
            'cost_thb': 'ต้นทุน (THB)',
            'value_usd': 'มูลค่า (USD)',
            'value_thb': 'มูลค่า (THB)',
            'profit_loss_usd': 'กำไร/ขาดทุน (USD)',
            'profit_loss_thb': 'กำไร/ขาดทุน (THB)',
            'profit_loss_pct': '% เปลี่ยนแปลง'
        })
        
        st.dataframe(
            df_display[[
                'รหัสหุ้น', 'จำนวน',
                'ราคาซื้อ (USD)', 'ราคาซื้อ (THB)',
                'ราคาปัจจุบัน (USD)', 'ราคาปัจจุบัน (THB)',
                'ต้นทุน (USD)', 'ต้นทุน (THB)',
                'มูลค่า (USD)', 'มูลค่า (THB)',
                'กำไร/ขาดทุน (USD)', 'กำไร/ขาดทุน (THB)',
                '% เปลี่ยนแปลง'
            ]],
            use_container_width=True,
            hide_index=True
        )
        
        # Portfolio composition chart
        st.markdown("#### 📊 สัดส่วนการลงทุน")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            fig1 = go.Figure(data=[go.Pie(
                labels=[s['symbol'] for s in portfolio_data['stocks']],
                values=[s['value'] for s in portfolio_data['stocks']],
                hole=.3,
                textinfo='label+percent',
                textposition='auto'
            )])
            
            fig1.update_layout(
                title="สัดส่วนมูลค่าหุ้นในพอร์ต (USD)",
                height=400
            )
            
            st.plotly_chart(fig1, use_container_width=True)
        
        with col_chart2:
            # Performance chart
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

# ===========================
# Page 2: Portfolio Management
# ===========================
elif page == "💼 Portfolio Management":
    st.title("💼 Portfolio Management")
    st.markdown("### เพิ่ม แก้ไข หรือลบหุ้นในพอร์ต")
    
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

# Footer
st.divider()
st.caption("💡 Portfolio Dashboard - Stock Analyzer © 2026")
