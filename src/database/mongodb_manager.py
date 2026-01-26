"""
MongoDB Manager
จัดการการเชื่อมต่อและดำเนินการกับ MongoDB Atlas
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, DuplicateKeyError
import pandas as pd
from dotenv import load_dotenv

# โหลด environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBManager:
    """จัดการ MongoDB Atlas สำหรับ Stock Analyzer"""
    
    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize MongoDB connection
        
        Args:
            connection_string: MongoDB Atlas connection string
                              ถ้าไม่ระบุจะดึงจาก environment variable MONGODB_URI
        """
        # ใช้ connection string จาก parameter หรือ environment
        self.connection_string = connection_string or os.getenv('MONGODB_URI')
        
        if not self.connection_string:
            raise ValueError(
                "MongoDB connection string not found. "
                "Please set MONGODB_URI in .env file or pass as parameter"
            )
        
        try:
            # เชื่อมต่อ MongoDB
            self.client = MongoClient(self.connection_string)
            
            # ทดสอบการเชื่อมต่อ
            self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB Atlas successfully")
            
            # เลือก Database
            self.db = self.client['stock_analyzer']
            
            # กำหนด Collections
            self.stocks_collection = self.db['stocks']  # ข้อมูลหุ้นทั่วไป
            self.prices_collection = self.db['prices']  # ราคาย้อนหลัง (Time Series)
            self.signals_collection = self.db['signals']  # สัญญาณซื้อขาย
            self.backtest_collection = self.db['backtests']  # ผลลัพธ์ Backtest
            self.portfolio_collection = self.db['portfolio']  # Portfolio
            self.users_collection = self.db['users']  # ข้อมูลผู้ใช้ (สำหรับอนาคต)
            
            # สร้าง Indexes
            self._create_indexes()
            
        except ConnectionFailure as e:
            logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
            raise
    
    def _create_indexes(self):
        """สร้าง indexes สำหรับ query ที่เร็วขึ้น"""
        try:
            # Index สำหรับ stocks
            self.stocks_collection.create_index([("symbol", ASCENDING)], unique=True)
            
            # Index สำหรับ prices (Time Series)
            self.prices_collection.create_index([
                ("symbol", ASCENDING),
                ("date", DESCENDING)
            ])
            
            # Index สำหรับ signals
            self.signals_collection.create_index([
                ("symbol", ASCENDING),
                ("date", DESCENDING),
                ("signal_type", ASCENDING)
            ])
            
            # Index สำหรับ backtests
            self.backtest_collection.create_index([("created_at", DESCENDING)])
            
            logger.info("✅ Created database indexes")
            
        except Exception as e:
            logger.warning(f"⚠️ Error creating indexes: {str(e)}")
    
    # ==================== STOCK DATA ====================
    
    def save_stock_info(self, symbol: str, stock_data: Dict[str, Any]):
        """
        บันทึกข้อมูลหุ้น
        
        Args:
            symbol: รหัสหุ้น
            stock_data: ข้อมูลหุ้น (dict)
        """
        try:
            stock_data['symbol'] = symbol
            stock_data['updated_at'] = datetime.now()
            
            # Update หรือ Insert
            self.stocks_collection.update_one(
                {'symbol': symbol},
                {'$set': stock_data},
                upsert=True
            )
            logger.info(f"✅ Saved stock info for {symbol}")
            
        except Exception as e:
            logger.error(f"❌ Error saving stock info for {symbol}: {str(e)}")
            raise
    
    def get_stock_info(self, symbol: str) -> Optional[Dict[str, Any]]:
        """
        ดึงข้อมูลหุ้น
        
        Args:
            symbol: รหัสหุ้น
            
        Returns:
            Dict ของข้อมูลหุ้น หรือ None ถ้าไม่พบ
        """
        try:
            stock = self.stocks_collection.find_one({'symbol': symbol})
            if stock:
                stock.pop('_id', None)  # ลบ MongoDB ObjectId
            return stock
            
        except Exception as e:
            logger.error(f"❌ Error getting stock info for {symbol}: {str(e)}")
            return None
    
    # ==================== PRICE DATA (Time Series) ====================
    
    def save_price_data(self, symbol: str, price_df: pd.DataFrame):
        """
        บันทึกข้อมูลราคาหุ้น
        
        Args:
            symbol: รหัสหุ้น
            price_df: DataFrame ของราคา (columns: Date, Open, High, Low, Close, Volume)
        """
        try:
            # แปลง DataFrame เป็น list of dicts
            records = []
            for date, row in price_df.iterrows():
                record = {
                    'symbol': symbol,
                    'date': pd.to_datetime(date).to_pydatetime(),
                    'open': float(row.get('Open', 0)),
                    'high': float(row.get('High', 0)),
                    'low': float(row.get('Low', 0)),
                    'close': float(row.get('Close', 0)),
                    'volume': int(row.get('Volume', 0)),
                    'updated_at': datetime.now()
                }
                records.append(record)
            
            # Bulk insert (เร็วกว่า insert ทีละ record)
            if records:
                # ลบข้อมูลเก่าของหุ้นนี้ก่อน
                self.prices_collection.delete_many({'symbol': symbol})
                
                # Insert ข้อมูลใหม่
                self.prices_collection.insert_many(records, ordered=False)
                logger.info(f"✅ Saved {len(records)} price records for {symbol}")
            
        except Exception as e:
            logger.error(f"❌ Error saving price data for {symbol}: {str(e)}")
            raise
    
    def get_price_data(self, symbol: str, start_date: Optional[datetime] = None, 
                       end_date: Optional[datetime] = None) -> pd.DataFrame:
        """
        ดึงข้อมูลราคาหุ้น
        
        Args:
            symbol: รหัสหุ้น
            start_date: วันเริ่มต้น (optional)
            end_date: วันสิ้นสุด (optional)
            
        Returns:
            DataFrame ของราคา
        """
        try:
            # สร้าง query
            query = {'symbol': symbol}
            
            if start_date or end_date:
                query['date'] = {}
                if start_date:
                    query['date']['$gte'] = start_date
                if end_date:
                    query['date']['$lte'] = end_date
            
            # Query จาก MongoDB
            cursor = self.prices_collection.find(query).sort('date', ASCENDING)
            
            # แปลงเป็น DataFrame
            records = list(cursor)
            if not records:
                return pd.DataFrame()
            
            df = pd.DataFrame(records)
            df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
            df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            df.set_index('Date', inplace=True)
            
            logger.info(f"✅ Retrieved {len(df)} price records for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"❌ Error getting price data for {symbol}: {str(e)}")
            return pd.DataFrame()
    
    # ==================== SIGNALS ====================
    
    def save_signal(self, symbol: str, signal_data: Dict[str, Any]):
        """
        บันทึกสัญญาณซื้อขาย
        
        Args:
            symbol: รหัสหุ้น
            signal_data: ข้อมูลสัญญาณ (buy/sell, confidence, reasons, etc.)
        """
        try:
            signal_data['symbol'] = symbol
            signal_data['date'] = signal_data.get('date', datetime.now())
            signal_data['created_at'] = datetime.now()
            
            # Insert สัญญาณใหม่
            self.signals_collection.insert_one(signal_data)
            logger.info(f"✅ Saved signal for {symbol}: {signal_data.get('signal_type')}")
            
        except Exception as e:
            logger.error(f"❌ Error saving signal for {symbol}: {str(e)}")
            raise
    
    def get_signals(self, symbol: Optional[str] = None, 
                    signal_type: Optional[str] = None,
                    days: int = 30) -> List[Dict[str, Any]]:
        """
        ดึงสัญญาณซื้อขาย
        
        Args:
            symbol: รหัสหุ้น (optional)
            signal_type: ประเภทสัญญาณ 'buy' หรือ 'sell' (optional)
            days: จำนวนวันย้อนหลัง
            
        Returns:
            List of signal dicts
        """
        try:
            # สร้าง query
            query = {}
            
            if symbol:
                query['symbol'] = symbol
            
            if signal_type:
                query['signal_type'] = signal_type
            
            # กรองตามวันที่
            start_date = datetime.now() - timedelta(days=days)
            query['date'] = {'$gte': start_date}
            
            # Query จาก MongoDB
            cursor = self.signals_collection.find(query).sort('date', DESCENDING)
            
            signals = []
            for doc in cursor:
                doc.pop('_id', None)
                signals.append(doc)
            
            logger.info(f"✅ Retrieved {len(signals)} signals")
            return signals
            
        except Exception as e:
            logger.error(f"❌ Error getting signals: {str(e)}")
            return []
    
    # ==================== BACKTESTING ====================
    
    def save_backtest_result(self, backtest_data: Dict[str, Any]) -> str:
        """
        บันทึกผลลัพธ์ Backtest
        
        Args:
            backtest_data: ข้อมูล backtest (symbols, period, results, etc.)
            
        Returns:
            Backtest ID
        """
        try:
            backtest_data['created_at'] = datetime.now()
            
            # Insert
            result = self.backtest_collection.insert_one(backtest_data)
            backtest_id = str(result.inserted_id)
            
            logger.info(f"✅ Saved backtest result: {backtest_id}")
            return backtest_id
            
        except Exception as e:
            logger.error(f"❌ Error saving backtest result: {str(e)}")
            raise
    
    def get_backtest_results(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        ดึงผลลัพธ์ Backtest ล่าสุด
        
        Args:
            limit: จำนวนผลลัพธ์สูงสุด
            
        Returns:
            List of backtest results
        """
        try:
            cursor = self.backtest_collection.find().sort('created_at', DESCENDING).limit(limit)
            
            results = []
            for doc in cursor:
                doc['_id'] = str(doc['_id'])  # แปลง ObjectId เป็น string
                results.append(doc)
            
            logger.info(f"✅ Retrieved {len(results)} backtest results")
            return results
            
        except Exception as e:
            logger.error(f"❌ Error getting backtest results: {str(e)}")
            return []
    
    # ==================== PORTFOLIO ====================
    
    def save_portfolio(self, user_id: str, portfolio_data: Dict[str, Any]):
        """
        บันทึก Portfolio
        
        Args:
            user_id: รหัสผู้ใช้
            portfolio_data: ข้อมูล portfolio
        """
        try:
            portfolio_data['user_id'] = user_id
            portfolio_data['updated_at'] = datetime.now()
            
            # Update หรือ Insert
            self.portfolio_collection.update_one(
                {'user_id': user_id},
                {'$set': portfolio_data},
                upsert=True
            )
            logger.info(f"✅ Saved portfolio for user {user_id}")
            
        except Exception as e:
            logger.error(f"❌ Error saving portfolio: {str(e)}")
            raise
    
    def get_portfolio(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        ดึง Portfolio
        
        Args:
            user_id: รหัสผู้ใช้
            
        Returns:
            Portfolio data หรือ None
        """
        try:
            portfolio = self.portfolio_collection.find_one({'user_id': user_id})
            if portfolio:
                portfolio.pop('_id', None)
            return portfolio
            
        except Exception as e:
            logger.error(f"❌ Error getting portfolio: {str(e)}")
            return None
    
    # ==================== UTILITY ====================
    
    def get_database_stats(self) -> Dict[str, Any]:
        """
        ดึงสถิติของ Database
        
        Returns:
            Dict ของสถิติ (จำนวน documents ในแต่ละ collection)
        """
        try:
            stats = {
                'stocks': self.stocks_collection.count_documents({}),
                'prices': self.prices_collection.count_documents({}),
                'signals': self.signals_collection.count_documents({}),
                'backtests': self.backtest_collection.count_documents({}),
                'portfolio': self.portfolio_collection.count_documents({}),
            }
            
            logger.info(f"✅ Database stats: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"❌ Error getting database stats: {str(e)}")
            return {}
    
    def close(self):
        """ปิดการเชื่อมต่อ MongoDB"""
        try:
            self.client.close()
            logger.info("✅ Closed MongoDB connection")
        except Exception as e:
            logger.error(f"❌ Error closing MongoDB connection: {str(e)}")


# ==================== HELPER FUNCTIONS ====================

def get_mongodb_manager() -> MongoDBManager:
    """
    สร้าง MongoDBManager instance (singleton pattern)
    
    Returns:
        MongoDBManager instance
    """
    if not hasattr(get_mongodb_manager, 'instance'):
        get_mongodb_manager.instance = MongoDBManager()
    
    return get_mongodb_manager.instance
