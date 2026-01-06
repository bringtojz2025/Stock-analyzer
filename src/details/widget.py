"""
Enhanced Stock Information Widget
เครื่องมือแสดงข้อมูลหุ้นแบบรายละเอียดพร้อมคำแนะนำ
"""

import streamlit as st
from src.details.provider import StockDetailsProvider


class StockInfoWidget:
    """Widget สำหรับแสดงข้อมูลหุ้นแบบรายละเอียด"""
    
    @staticmethod
    def display_stock_fundamentals(symbol):
        """
        แสดงข้อมูลพื้นฐานของหุ้น
        
        Args:
            symbol: สัญลักษณ์หุ้น
        """
        provider = StockDetailsProvider()
        details = provider.get_enhanced_stock_info(symbol)
        
        if not details:
            st.error(f"ไม่สามารถดึงข้อมูล {symbol}")
            return
        
        # Create 3 columns for basic info
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write(f"**ชื่อบริษัท**")
            st.write(details.get('name', 'ไม่ทราบ'))
            st.write(f"**ประเทศ**")
            st.write(details.get('country', 'ไม่ทราบ'))
        
        with col2:
            st.write(f"**ตลาด**")
            st.write(details.get('market', 'ไม่ทราบ'))
            st.write(f"**ก่อตั้ง**")
            st.write(details.get('founded', 'ไม่ทราบ'))
        
        with col3:
            st.write(f"**จำนวนพนักงาน**")
            employees = details.get('employees', 'ไม่ทราบ')
            if isinstance(employees, int):
                st.write(f"{employees:,.0f}")
            else:
                st.write(employees)
            
            st.write(f"**เว็บไซต์**")
            website = details.get('website', 'ไม่มี')
            if website and website != 'ไม่มี':
                st.write(f"[เยี่ยมชม]({website})")
            else:
                st.write(website)
    
    @staticmethod
    def display_valuation_analysis(symbol):
        """
        แสดงการวิเคราะห์การประเมินมูลค่า
        
        Args:
            symbol: สัญลักษณ์หุ้น
        """
        provider = StockDetailsProvider()
        details = provider.get_enhanced_stock_info(symbol)
        
        if not details:
            return
        
        st.subheader("💹 การวิเคราะห์การประเมินมูลค่า")
        
        pe_ratio = details.get('pe_ratio', 'N/A')
        peg_ratio = details.get('peg_ratio', 'N/A')
        
        col1, col2, col3 = st.columns(3)
        
        # P/E Analysis
        with col1:
            st.metric("P/E Ratio", pe_ratio)
            
            if isinstance(pe_ratio, (int, float)):
                if pe_ratio < 15:
                    st.success("✅ ถูก (Undervalued)")
                elif pe_ratio < 25:
                    st.info("⚠️ ปกติ (Fair)")
                else:
                    st.warning("⚠️ แพง (Overvalued)")
        
        # PEG Analysis
        with col2:
            st.metric("PEG Ratio", peg_ratio)
            
            if isinstance(peg_ratio, (int, float)):
                if peg_ratio < 1:
                    st.success("✅ ดี (Good value)")
                elif peg_ratio < 2:
                    st.info("⚠️ ปกติ")
                else:
                    st.warning("⚠️ แพง")
        
        # Forward P/E
        with col3:
            forward_pe = details.get('forward_pe', 'N/A')
            st.metric("Forward P/E", forward_pe)
        
        # Additional metrics
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("P/B Ratio", details.get('price_to_book', 'N/A'))
            st.metric("P/S Ratio", details.get('price_to_sales', 'N/A'))
        
        with col2:
            st.metric("Dividend Yield", details.get('dividend_yield', 'N/A'))
            st.metric("Market Cap", 
                     provider.format_market_cap(details.get('market_cap', 'N/A')))
    
    @staticmethod
    def display_financial_health(symbol):
        """
        แสดงสุขภาพทางการเงิน
        
        Args:
            symbol: สัญลักษณ์หุ้น
        """
        provider = StockDetailsProvider()
        details = provider.get_enhanced_stock_info(symbol)
        
        if not details:
            return
        
        st.subheader("📊 สุขภาพทางการเงิน")
        
        col1, col2, col3 = st.columns(3)
        
        # Profitability
        with col1:
            st.write("**ความสามารถในการทำกำไร**")
            st.metric("ROE", details.get('roe', 'N/A'))
            st.metric("ROA", details.get('roa', 'N/A'))
            st.metric("Profit Margin", details.get('profit_margin', 'N/A'))
        
        # Leverage
        with col2:
            st.write("**ความเสี่ยงทางการเงิน**")
            de_ratio = details.get('debt_to_equity', 'N/A')
            st.metric("Debt-to-Equity", de_ratio)
            
            if isinstance(de_ratio, (int, float)):
                if de_ratio < 0.5:
                    st.success("✅ ต่ำ (Low Risk)")
                elif de_ratio < 1.5:
                    st.info("⚠️ ปกติ")
                else:
                    st.warning("⚠️ สูง (High Risk)")
            
            st.metric("Current Ratio", details.get('current_ratio', 'N/A'))
        
        # Other
        with col3:
            st.write("**อื่นๆ**")
            st.metric("Beta", details.get('beta', 'N/A'))
            st.metric("52W High", f"${details.get('fifty_two_week_high', 'N/A')}")
            st.metric("52W Low", f"${details.get('fifty_two_week_low', 'N/A')}")
    
    @staticmethod
    def display_valuation_recommendation(symbol):
        """
        ให้คำแนะนำเกี่ยวกับมูลค่า
        
        Args:
            symbol: สัญลักษณ์หุ้น
        """
        provider = StockDetailsProvider()
        details = provider.get_enhanced_stock_info(symbol)
        
        if not details:
            return
        
        st.subheader("🎯 คำแนะนำเบื้องต้น")
        
        recommendations = []
        pe_ratio = details.get('pe_ratio', None)
        roe = details.get('roe', None)
        de_ratio = details.get('debt_to_equity', None)
        dividend = details.get('dividend_yield', None)
        
        # P/E Check
        if isinstance(pe_ratio, (int, float)):
            if pe_ratio < 15:
                recommendations.append("✅ มูลค่าดูถูก เทียบกับกำไร")
            elif pe_ratio > 30:
                recommendations.append("⚠️ ราคาค่อนข้างแพง")
        
        # ROE Check
        if isinstance(roe, (int, float)):
            if roe > 0.15:
                recommendations.append("✅ ทำกำไรได้ดี (ROE > 15%)")
            elif roe < 0:
                recommendations.append("⚠️ ขาดทุน")
        
        # Debt Check
        if isinstance(de_ratio, (int, float)):
            if de_ratio < 0.5:
                recommendations.append("✅ หนี้สินต่ำ เสี่ยงต่ำ")
            elif de_ratio > 2:
                recommendations.append("⚠️ หนี้สินสูง เสี่ยงสูง")
        
        # Dividend Check
        if isinstance(dividend, (int, float)):
            if dividend > 0.03:
                recommendations.append(f"✅ ได้เงินปันผล {dividend*100:.2f}%")
        
        if recommendations:
            for rec in recommendations:
                st.write(rec)
        else:
            st.info("ข้อมูลไม่เพียงพอสำหรับการวิเคราะห์")


if __name__ == "__main__":
    # Test
    widget = StockInfoWidget()
    
    # Test display
    print("Testing Stock Info Widget...")
    # widget.display_stock_fundamentals("AAPL")
