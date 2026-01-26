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
        
        pe_ratio = details.get('pe_ratio')
        peg_ratio = details.get('peg_ratio')
        forward_pe = details.get('forward_pe')
        
        col1, col2, col3 = st.columns(3)
        
        # P/E Analysis
        with col1:
            if pe_ratio is not None:
                st.metric("P/E Ratio", f"{pe_ratio:.2f}")
                
                if pe_ratio < 15:
                    st.success("✅ ถูก (Undervalued)")
                elif pe_ratio < 25:
                    st.info("⚠️ ปกติ (Fair)")
                else:
                    st.warning("⚠️ แพง (Overvalued)")
            else:
                st.metric("P/E Ratio", "N/A")
        
        # PEG Analysis
        with col2:
            if peg_ratio is not None:
                st.metric("PEG Ratio", f"{peg_ratio:.2f}")
                
                if peg_ratio < 1:
                    st.success("✅ ดี (Good value)")
                elif peg_ratio < 2:
                    st.info("⚠️ ปกติ")
                else:
                    st.warning("⚠️ แพง")
            else:
                st.metric("PEG Ratio", "N/A")
        
        # Forward P/E
        with col3:
            if forward_pe is not None:
                st.metric("Forward P/E", f"{forward_pe:.2f}")
            else:
                st.metric("Forward P/E", "N/A")
        
        # Additional metrics
        col1, col2 = st.columns(2)
        
        with col1:
            pb_ratio = details.get('price_to_book')
            if pb_ratio is not None:
                st.metric("P/B Ratio", f"{pb_ratio:.2f}")
            else:
                st.metric("P/B Ratio", "N/A")
            
            ps_ratio = details.get('price_to_sales')
            if ps_ratio is not None:
                st.metric("P/S Ratio", f"{ps_ratio:.2f}")
            else:
                st.metric("P/S Ratio", "N/A")
        
        with col2:
            div_yield = details.get('dividend_yield')
            if div_yield is not None:
                div_pct = div_yield * 100
                st.metric("Dividend Yield", f"{div_pct:.2f}%")
            else:
                st.metric("Dividend Yield", "N/A")
            
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
            
            roe = details.get('roe')
            if roe is not None:
                roe_pct = roe * 100
                st.metric("ROE", f"{roe_pct:.2f}%")
                if roe_pct > 15:
                    st.success("✅ ดีมาก")
                elif roe_pct > 10:
                    st.info("✅ ดี")
                elif roe_pct > 0:
                    st.warning("⚠️ ปานกลาง")
                else:
                    st.error("❌ ขาดทุน")
            else:
                st.metric("ROE", "N/A")
            
            roa = details.get('roa')
            if roa is not None:
                roa_pct = roa * 100
                st.metric("ROA", f"{roa_pct:.2f}%")
            else:
                st.metric("ROA", "N/A")
            
            profit_margin = details.get('profit_margin')
            if profit_margin is not None:
                profit_pct = profit_margin * 100
                st.metric("Profit Margin", f"{profit_pct:.2f}%")
            else:
                st.metric("Profit Margin", "N/A")
        
        # Leverage
        with col2:
            st.write("**ความเสี่ยงทางการเงิน**")
            de_ratio = details.get('debt_to_equity')
            
            if de_ratio is not None:
                # debt_to_equity from yfinance is already a ratio
                if de_ratio > 100:  # If it's in percentage form
                    de_ratio = de_ratio / 100
                st.metric("Debt-to-Equity", f"{de_ratio:.2f}")
                
                if de_ratio < 0.5:
                    st.success("✅ ต่ำ (Low Risk)")
                elif de_ratio < 1.5:
                    st.info("⚠️ ปกติ")
                else:
                    st.warning("⚠️ สูง (High Risk)")
            else:
                st.metric("Debt-to-Equity", "N/A")
            
            current_ratio = details.get('current_ratio')
            if current_ratio is not None:
                st.metric("Current Ratio", f"{current_ratio:.2f}")
                if current_ratio > 2:
                    st.success("✅ สภาพคล่องดี")
                elif current_ratio > 1:
                    st.info("✅ ปกติ")
                else:
                    st.warning("⚠️ สภาพคล่องต่ำ")
            else:
                st.metric("Current Ratio", "N/A")
        
        # Other
        with col3:
            st.write("**อื่นๆ**")
            
            beta = details.get('beta')
            if beta is not None:
                st.metric("Beta", f"{beta:.2f}")
                if beta > 1.5:
                    st.warning("⚠️ ความผันผวนสูง")
                elif beta > 1:
                    st.info("⚠️ ผันผวนปานกลาง")
                else:
                    st.success("✅ ผันผวนต่ำ")
            else:
                st.metric("Beta", "N/A")
            
            high_52w = details.get('fifty_two_week_high')
            if high_52w is not None and high_52w != 'N/A':
                st.metric("52W High", f"${high_52w:.2f}")
            else:
                st.metric("52W High", "N/A")
            
            low_52w = details.get('fifty_two_week_low')
            if low_52w is not None and low_52w != 'N/A':
                st.metric("52W Low", f"${low_52w:.2f}")
            else:
                st.metric("52W Low", "N/A")
    
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
        pe_ratio = details.get('pe_ratio')
        roe = details.get('roe')
        de_ratio = details.get('debt_to_equity')
        dividend = details.get('dividend_yield')
        
        # P/E Check
        if pe_ratio is not None:
            if pe_ratio < 15:
                recommendations.append(f"✅ มูลค่าดูถูก เทียบกับกำไร (P/E = {pe_ratio:.2f})")
            elif pe_ratio > 30:
                recommendations.append(f"⚠️ ราคาค่อนข้างแพง (P/E = {pe_ratio:.2f})")
            else:
                recommendations.append(f"ℹ️ P/E Ratio อยู่ในระดับปกติ ({pe_ratio:.2f})")
        
        # ROE Check
        if roe is not None:
            roe_pct = roe * 100
            if roe_pct > 15:
                recommendations.append(f"✅ ทำกำไรได้ดีมาก (ROE = {roe_pct:.2f}%)")
            elif roe_pct > 10:
                recommendations.append(f"✅ ทำกำไรได้ดี (ROE = {roe_pct:.2f}%)")
            elif roe_pct > 0:
                recommendations.append(f"ℹ️ ทำกำไรได้ปานกลาง (ROE = {roe_pct:.2f}%)")
            else:
                recommendations.append(f"⚠️ ขาดทุน (ROE = {roe_pct:.2f}%)")
        
        # Debt Check
        if de_ratio is not None:
            # Handle both percentage and ratio formats
            de_value = de_ratio / 100 if de_ratio > 100 else de_ratio
            
            if de_value < 0.5:
                recommendations.append(f"✅ หนี้สินต่ำ เสี่ยงต่ำ (D/E = {de_value:.2f})")
            elif de_value > 2:
                recommendations.append(f"⚠️ หนี้สินสูง เสี่ยงสูง (D/E = {de_value:.2f})")
            else:
                recommendations.append(f"ℹ️ หนี้สินอยู่ในระดับปกติ (D/E = {de_value:.2f})")
        
        # Dividend Check
        if dividend is not None:
            div_pct = dividend * 100
            if div_pct > 3:
                recommendations.append(f"✅ ได้เงินปันผลสูง {div_pct:.2f}%")
            elif div_pct > 0:
                recommendations.append(f"ℹ️ ได้เงินปันผล {div_pct:.2f}%")
        
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
