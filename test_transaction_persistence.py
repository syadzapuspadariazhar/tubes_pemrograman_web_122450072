#!/usr/bin/env python3
"""
Test script to verify transaction persistence is working correctly.
This tests the complete transaction API flow: POST -> GET -> PUT -> GET -> DELETE -> GET
"""

import requests
import json
import time
from datetime import datetime, date

BASE_URL = "http://localhost:6543"

def test_transaction_persistence():
    print("=== Testing Transaction Persistence ===\n")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    try:
        # Step 1: Get initial transaction count
        print("1. Getting initial transactions...")
        response = requests.get(f"{BASE_URL}/api/transactions")
        if response.status_code != 200:
            print(f"❌ Failed to get transactions: {response.status_code}")
            return False
        
        initial_transactions = response.json()
        initial_count = len(initial_transactions)
        print(f"✅ Initial transaction count: {initial_count}")
        
        # Step 2: Create a test transaction
        print("\n2. Creating a test transaction...")
        test_transaction = {
            "deskripsi": "Test Transaction for Persistence",
            "jumlah": 50000,
            "jenis": "pengeluaran",
            "tanggal": datetime.now().date().isoformat(),
            "kategori_id": 1  # Assuming category 1 exists
        }
        
        response = requests.post(f"{BASE_URL}/api/transactions", 
                               json=test_transaction,
                               headers={'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            print(f"❌ Failed to create transaction: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        create_result = response.json()
        transaction_id = create_result.get('id')
        print(f"✅ Transaction created with ID: {transaction_id}")
        
        if not transaction_id:
            print("❌ No ID returned from creation")
            return False
        
        # Step 3: Verify transaction appears in GET request
        print("\n3. Verifying transaction persists in GET request...")
        time.sleep(1)  # Brief pause to ensure session cleanup
        
        response = requests.get(f"{BASE_URL}/api/transactions")
        if response.status_code != 200:
            print(f"❌ Failed to get transactions after creation: {response.status_code}")
            return False
        
        current_transactions = response.json()
        current_count = len(current_transactions)
        print(f"✅ Current transaction count: {current_count}")
        
        # Find our transaction
        our_transaction = None
        for trans in current_transactions:
            if trans['id'] == transaction_id:
                our_transaction = trans
                break
        
        if not our_transaction:
            print(f"❌ Created transaction (ID: {transaction_id}) not found in GET response")
            print(f"Available transaction IDs: {[t.get('id') for t in current_transactions]}")
            return False
        
        print(f"✅ Transaction found: {our_transaction['deskripsi']}")
        
        # Step 4: Update the transaction
        print("\n4. Testing transaction update...")
        updated_data = {
            "deskripsi": "Updated Test Transaction",
            "jumlah": 75000,
            "jenis": "pengeluaran",
            "tanggal": datetime.now().date().isoformat(),
            "kategori_id": 1
        }
        
        response = requests.put(f"{BASE_URL}/api/transactions/{transaction_id}",
                              json=updated_data,
                              headers={'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            print(f"❌ Failed to update transaction: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print("✅ Transaction updated successfully")
        
        # Step 5: Verify update persists
        print("\n5. Verifying update persists...")
        time.sleep(1)
        
        response = requests.get(f"{BASE_URL}/api/transactions")
        if response.status_code != 200:
            print(f"❌ Failed to get transactions after update: {response.status_code}")
            return False
        
        updated_transactions = response.json()
        updated_transaction = None
        for trans in updated_transactions:
            if trans['id'] == transaction_id:
                updated_transaction = trans
                break
        
        if not updated_transaction:
            print(f"❌ Updated transaction not found")
            return False
        
        if updated_transaction['deskripsi'] != "Updated Test Transaction":
            print(f"❌ Update not persisted. Description: {updated_transaction['deskripsi']}")
            return False
        
        if updated_transaction['jumlah'] != 75000:
            print(f"❌ Amount update not persisted. Amount: {updated_transaction['jumlah']}")
            return False
        
        print("✅ Update persisted correctly")
        
        # Step 6: Delete the transaction
        print("\n6. Testing transaction deletion...")
        response = requests.delete(f"{BASE_URL}/api/transactions/{transaction_id}")
        
        if response.status_code != 200:
            print(f"❌ Failed to delete transaction: {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        print("✅ Transaction deleted successfully")
        
        # Step 7: Verify deletion persists
        print("\n7. Verifying deletion persists...")
        time.sleep(1)
        
        response = requests.get(f"{BASE_URL}/api/transactions")
        if response.status_code != 200:
            print(f"❌ Failed to get transactions after deletion: {response.status_code}")
            return False
        
        final_transactions = response.json()
        final_count = len(final_transactions)
        
        # Check transaction is gone
        deleted_transaction = None
        for trans in final_transactions:
            if trans['id'] == transaction_id:
                deleted_transaction = trans
                break
        
        if deleted_transaction:
            print(f"❌ Transaction still exists after deletion: {deleted_transaction}")
            return False
        
        if final_count != initial_count:
            print(f"❌ Transaction count mismatch. Initial: {initial_count}, Final: {final_count}")
            return False
        
        print("✅ Deletion persisted correctly")
        print(f"✅ Final transaction count matches initial: {final_count}")
        
        print("\n🎉 ALL TRANSACTION PERSISTENCE TESTS PASSED! 🎉")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure the backend is running on http://localhost:6543")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_transaction_persistence()
    if success:
        print("\n✅ Transaction API is working correctly with proper persistence!")
    else:
        print("\n❌ Transaction API has persistence issues.")
    
    exit(0 if success else 1)
