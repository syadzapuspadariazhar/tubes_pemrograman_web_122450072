#!/usr/bin/env python3
"""
Complete test: recreate database, start server, test transaction
"""

import subprocess
import time
import requests
import json
import os
from datetime import datetime

def run_complete_test():
    print("=== Complete Transaction Fix Test ===\n")
    
    # Step 1: Recreate database
    print("1. Recreating database with fixed model...")
    try:
        result = subprocess.run(["python", "recreate_database.py"], 
                              capture_output=True, text=True, cwd=".")
        if result.returncode == 0:
            print("✅ Database recreated successfully")
            print(result.stdout)
        else:
            print(f"❌ Database recreation failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error recreating database: {e}")
        return False
    
    # Step 2: Start server
    print("\n2. Starting server...")
    server_process = None
    try:
        # Change to backend directory and start server
        os.chdir("backend")
        
        # Activate virtual environment and start server
        if os.name == 'nt':  # Windows
            server_process = subprocess.Popen([
                "cmd", "/c", 
                ".\\env\\Scripts\\activate.bat && python start_server_fixed.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        else:  # Unix/Linux
            server_process = subprocess.Popen([
                "bash", "-c",
                "source ./env/bin/activate && python start_server_fixed.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        print("Waiting for server to start...")
        time.sleep(5)
        
        # Go back to parent directory
        os.chdir("..")
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    try:
        # Step 3: Test transaction creation
        print("\n3. Testing transaction creation...")
        
        # First create a category
        cat_response = requests.post("http://localhost:6543/api/categories",
                                   json={"nama": "Test Category Fix"},
                                   headers={'Content-Type': 'application/json'},
                                   timeout=10)
        
        if cat_response.status_code != 200:
            print(f"❌ Category creation failed: {cat_response.status_code}")
            return False
        
        cat_result = cat_response.json()
        cat_id = cat_result.get('id')
        print(f"✅ Category created with ID: {cat_id}")
        
        # Create transaction
        trans_response = requests.post("http://localhost:6543/api/transactions",
                                     json={
                                         "deskripsi": "Fixed Model Test Transaction", 
                                         "jumlah": 75000,
                                         "jenis": "pengeluaran",
                                         "tanggal": datetime.now().date().isoformat(),
                                         "kategori_id": cat_id
                                     },
                                     headers={'Content-Type': 'application/json'},
                                     timeout=10)
        
        if trans_response.status_code != 200:
            print(f"❌ Transaction creation failed: {trans_response.status_code}")
            print(f"Response: {trans_response.text}")
            return False
        
        trans_result = trans_response.json()
        trans_id = trans_result.get('id')
        print(f"📝 Transaction response: {trans_result}")
        
        if trans_id:
            print(f"✅ Transaction created with ID: {trans_id}")
        else:
            print("❌ Transaction ID is still null!")
            return False
        
        # Step 4: Verify persistence
        print("\n4. Verifying persistence...")
        time.sleep(1)
        
        get_response = requests.get("http://localhost:6543/api/transactions", timeout=10)
        if get_response.status_code != 200:
            print(f"❌ GET request failed: {get_response.status_code}")
            return False
        
        transactions = get_response.json()
        our_transaction = None
        for trans in transactions:
            if trans.get('deskripsi') == 'Fixed Model Test Transaction':
                our_transaction = trans
                break
        
        if our_transaction:
            print(f"✅ Transaction found in GET response: {our_transaction}")
            print("\n🎉 TRANSACTION PERSISTENCE FIX SUCCESSFUL! 🎉")
            return True
        else:
            print("❌ Transaction not found in GET response")
            print(f"Available transactions: {transactions}")
            return False
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    finally:
        # Clean up server process
        if server_process:
            try:
                server_process.terminate()
                server_process.wait(timeout=5)
            except:
                server_process.kill()

if __name__ == "__main__":
    success = run_complete_test()
    if success:
        print("\n✅ All tests passed! Transaction persistence is fixed.")
    else:
        print("\n❌ Tests failed. Check the output above for details.")
