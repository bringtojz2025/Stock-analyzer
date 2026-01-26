"""
ทดสอบ MongoDB Connection แบบง่าย (ไม่ใช้ MongoDBManager)
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables
load_dotenv()

# Get MongoDB URI
mongodb_uri = os.getenv('MONGODB_URI')

if not mongodb_uri:
    print("❌ ERROR: MONGODB_URI not found in .env file")
    exit(1)

print("=" * 60)
print("Simple MongoDB Connection Test")
print("=" * 60)
print(f"\n📡 Connection String: {mongodb_uri[:50]}...")

try:
    # Create client with ServerApi
    print("\n1️⃣ Creating MongoClient with ServerApi...")
    client = MongoClient(
        mongodb_uri,
        server_api=ServerApi('1'),
        serverSelectionTimeoutMS=10000,  # 10 seconds timeout
        connectTimeoutMS=10000
    )
    
    # Test connection with ping
    print("2️⃣ Testing connection with ping...")
    result = client.admin.command('ping')
    
    if result.get('ok') == 1.0:
        print("✅ SUCCESS: Connected to MongoDB Atlas!")
        
        # Get database list
        print("\n3️⃣ Getting database list...")
        db_list = client.list_database_names()
        print(f"   Available databases: {db_list}")
        
        # Test write operation
        print("\n4️⃣ Testing write operation...")
        db = client['stock_analyzer']
        collection = db['test_connection']
        
        test_doc = {'test': 'connection', 'timestamp': 'now'}
        insert_result = collection.insert_one(test_doc)
        print(f"   ✅ Inserted document with ID: {insert_result.inserted_id}")
        
        # Test read operation
        print("\n5️⃣ Testing read operation...")
        found_doc = collection.find_one({'test': 'connection'})
        print(f"   ✅ Found document: {found_doc}")
        
        # Clean up
        print("\n6️⃣ Cleaning up test data...")
        collection.delete_one({'_id': insert_result.inserted_id})
        print("   ✅ Test document deleted")
        
        print("\n" + "=" * 60)
        print("🎉 ALL TESTS PASSED! MongoDB Atlas is working!")
        print("=" * 60)
        
    else:
        print(f"❌ Ping failed: {result}")
        
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   Message: {str(e)}")
    
    print("\n🔧 Troubleshooting:")
    print("   1. Check MongoDB Atlas cluster status (must be 'Available')")
    print("   2. Verify user credentials are correct")
    print("   3. Check Network Access allows your IP (0.0.0.0/0)")
    print("   4. Try restarting the cluster from Atlas dashboard")
    print("   5. Wait 2-3 minutes if cluster was just created/restarted")
    
finally:
    try:
        client.close()
        print("\n🔌 Connection closed")
    except:
        pass
