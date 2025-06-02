#!/usr/bin/env python3
"""
Direct comparison test between category and transaction creation
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:6543"

def compare_category_vs_transaction():
    print("=== Comparing Category vs Transaction Creation ===\n")
    
    # Wait for server
    time.sleep(2)
    
    try:
        print("1. Testing Category Creation (Known Working)...")
        cat_response = requests.post(f"{BASE_URL}/api/categories", 
                                   json={"nama": "Compare Test Category"},
                                   headers={'Content-Type': 'application/json'})
        
        if cat_response.status_code == 200:
            cat_result = cat_response.json()
            print(f"✅ Category Response: {cat_result}")
            cat_id = cat_result.get('id')
            print(f"Category ID: {cat_id} (type: {type(cat_id)})")
        else:
            print(f"❌ Category failed: {cat_response.status_code} - {cat_response.text}")
            return
        
        print("\n2. Testing Transaction Creation...")
        trans_response = requests.post(f"{BASE_URL}/api/transactions", 
                                     json={
                                         "deskripsi": "Compare Test Transaction",
                                         "jumlah": 15000,
                                         "jenis": "pengeluaran", 
                                         "tanggal": "2025-06-02",
                                         "kategori_id": cat_id
                                     },
                                     headers={'Content-Type': 'application/json'})
        
        if trans_response.status_code == 200:
            trans_result = trans_response.json()
            print(f"📝 Transaction Response: {trans_result}")
            trans_id = trans_result.get('id')
            print(f"Transaction ID: {trans_id} (type: {type(trans_id)})")
            
            if trans_id is None:
                print("❌ ISSUE CONFIRMED: Transaction ID is None!")
            else:
                print(f"✅ Transaction ID assigned: {trans_id}")
        else:
            print(f"❌ Transaction failed: {trans_response.status_code} - {trans_response.text}")
            return
        
        print("\n3. Checking Persistence...")
        
        # Check categories
        cat_get = requests.get(f"{BASE_URL}/api/categories")
        if cat_get.status_code == 200:
            categories = cat_get.json()
            our_cat = [c for c in categories if c.get('nama') == 'Compare Test Category']
            print(f"Categories found: {len(our_cat)} matching")
        
        # Check transactions  
        trans_get = requests.get(f"{BASE_URL}/api/transactions")
        if trans_get.status_code == 200:
            transactions = trans_get.json()
            our_trans = [t for t in transactions if t.get('deskripsi') == 'Compare Test Transaction']
            print(f"Transactions found: {len(our_trans)} matching")
            
            if our_trans:
                print(f"Found transaction: {our_trans[0]}")
            else:
                print("❌ Transaction not found in GET request")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    compare_category_vs_transaction()
