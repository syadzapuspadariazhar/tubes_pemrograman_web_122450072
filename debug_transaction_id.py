#!/usr/bin/env python3
"""
Debug transaction ID assignment issue
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:6543"

def debug_transaction_id():
    print("=== Debugging Transaction ID Assignment ===\n")
    
    # Wait for server to be ready
    time.sleep(3)
    
    try:
        # Test 1: Check if categories work (known working)
        print("1. Testing category creation (should work)...")
        cat_data = {"nama": "Debug Category"}
        response = requests.post(f"{BASE_URL}/api/categories", 
                               json=cat_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            cat_result = response.json()
            print(f"✅ Category created: {cat_result}")
            cat_id = cat_result.get('id')
            if cat_id:
                print(f"✅ Category ID assigned: {cat_id}")
            else:
                print("❌ Category ID is null")
        else:
            print(f"❌ Category creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # Test 2: Create transaction using the category ID
        print("\n2. Testing transaction creation...")
        trans_data = {
            "deskripsi": "Debug Transaction Test",
            "jumlah": 25000,
            "jenis": "pengeluaran",
            "tanggal": datetime.now().date().isoformat(),
            "kategori_id": cat_id
        }
        
        print(f"Sending transaction data: {trans_data}")
        
        response = requests.post(f"{BASE_URL}/api/transactions", 
                               json=trans_data,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code == 200:
            trans_result = response.json()
            print(f"📝 Transaction response: {trans_result}")
            trans_id = trans_result.get('id')
            if trans_id:
                print(f"✅ Transaction ID assigned: {trans_id}")
            else:
                print("❌ Transaction ID is null!")
        else:
            print(f"❌ Transaction creation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return
        
        # Test 3: Immediately check if transaction appears
        print("\n3. Checking if transaction appears in GET request...")
        time.sleep(1)
        
        response = requests.get(f"{BASE_URL}/api/transactions")
        if response.status_code == 200:
            transactions = response.json()
            print(f"📋 Found {len(transactions)} transactions")
            
            if transactions:
                for i, trans in enumerate(transactions):
                    print(f"  Transaction {i+1}: ID={trans.get('id')}, Desc='{trans.get('deskripsi')}'")
                    
                # Look for our transaction
                our_trans = None
                for trans in transactions:
                    if trans.get('deskripsi') == "Debug Transaction Test":
                        our_trans = trans
                        break
                
                if our_trans:
                    print(f"✅ Found our transaction: {our_trans}")
                else:
                    print("❌ Our transaction not found in GET response")
            else:
                print("❌ No transactions returned")
        else:
            print(f"❌ GET transactions failed: {response.status_code}")
        
        # Test 4: Check database directly
        print("\n4. Checking database file directly...")
        try:
            import sqlite3
            import os
            
            db_path = "backend/budget.db"
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Check transactions table
                cursor.execute("SELECT id, deskripsi, jumlah FROM transactions ORDER BY id DESC LIMIT 5")
                rows = cursor.fetchall()
                
                print(f"📊 Last 5 transactions in database:")
                for row in rows:
                    print(f"  ID: {row[0]}, Desc: '{row[1]}', Amount: {row[2]}")
                
                # Check if our transaction is there
                cursor.execute("SELECT * FROM transactions WHERE deskripsi = ?", ("Debug Transaction Test",))
                debug_trans = cursor.fetchone()
                
                if debug_trans:
                    print(f"✅ Debug transaction found in DB: ID={debug_trans[0]}")
                else:
                    print("❌ Debug transaction not found in database")
                
                conn.close()
            else:
                print("❌ Database file not found")
                
        except Exception as e:
            print(f"❌ Database check failed: {e}")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure backend is running.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_transaction_id()
