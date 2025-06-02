import sqlite3
import os

# Check if database file exists and what's in it
db_path = "backend/budget.db"

print("=== DATABASE INVESTIGATION ===")
print(f"Database file: {db_path}")

if os.path.exists(db_path):
    print(f"✅ Database file exists ({os.path.getsize(db_path)} bytes)")
    
    # Connect and check tables
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if categories table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories';")
        table_exists = cursor.fetchone()
        
        if table_exists:
            print("✅ Categories table exists")
            
            # Check table structure
            cursor.execute("PRAGMA table_info(categories);")
            columns = cursor.fetchall()
            print(f"Table structure: {columns}")
            
            # Check data in table
            cursor.execute("SELECT * FROM categories;")
            categories = cursor.fetchall()
            print(f"Categories in database: {categories}")
            
            if categories:
                print(f"✅ Found {len(categories)} categories in database")
                for cat in categories:
                    print(f"   ID: {cat[0]}, Name: {cat[1]}")
            else:
                print("❌ No categories found in database")
                
        else:
            print("❌ Categories table does not exist")
            
        # List all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"All tables: {[table[0] for table in tables]}")
        
    except Exception as e:
        print(f"❌ Database error: {e}")
    finally:
        conn.close()
        
else:
    print("❌ Database file does not exist")

print("\n=== TESTING API ENDPOINTS ===")

# Test the API endpoints
import requests

try:
    # Test GET
    print("Testing GET /api/categories...")
    response = requests.get("http://localhost:6543/api/categories", timeout=5)
    print(f"GET Status: {response.status_code}")
    print(f"GET Response: {response.text}")
    
    # Test POST
    print("\nTesting POST /api/categories...")
    response = requests.post(
        "http://localhost:6543/api/categories",
        headers={"Content-Type": "application/json"},
        json={"nama": "debug_category"},
        timeout=10
    )
    print(f"POST Status: {response.status_code}")
    print(f"POST Response: {response.text}")
    
    # Test GET again
    print("\nTesting GET after POST...")
    response = requests.get("http://localhost:6543/api/categories", timeout=5)
    print(f"GET Status: {response.status_code}")
    print(f"GET Response: {response.text}")
    
except Exception as e:
    print(f"❌ API Error: {e}")
