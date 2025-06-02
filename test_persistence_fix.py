#!/usr/bin/env python3
"""
Quick test script to start server and test the persistence fix
"""
import subprocess
import time
import requests
import json
import os
import signal
import sys

def start_server():
    """Start the backend server"""
    print("Starting backend server...")
    os.chdir(r"c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend")
    
    # Activate virtual environment and start server
    cmd = r".\env\Scripts\activate.bat && python -m waitress --port=6543 --call app:main"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(5)
    
    return process

def test_persistence():
    """Test the data persistence fix"""
    SERVER_URL = "http://localhost:6543"
    
    try:
        # Test 1: GET initial categories
        print("\n1. Getting initial categories...")
        response = requests.get(f"{SERVER_URL}/api/categories", timeout=10)
        print(f"Status: {response.status_code}")
        initial_categories = response.json() if response.status_code == 200 else []
        print(f"Initial categories: {initial_categories}")
        
        # Test 2: Add a new category
        print("\n2. Adding new category...")
        test_name = f"Test Category {int(time.time())}"
        data = {"nama": test_name}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(f"{SERVER_URL}/api/categories", 
                               json=data, headers=headers, timeout=10)
        print(f"POST Status: {response.status_code}")
        post_result = response.json() if response.status_code == 200 else None
        print(f"POST Response: {post_result}")
        
        if not post_result:
            print("❌ POST failed!")
            return False
            
        # Test 3: GET categories after POST
        print("\n3. Getting categories after POST...")
        time.sleep(1)  # Small delay to ensure consistency
        response = requests.get(f"{SERVER_URL}/api/categories", timeout=10)
        print(f"Status: {response.status_code}")
        after_categories = response.json() if response.status_code == 200 else []
        print(f"Categories after POST: {after_categories}")
        
        # Analysis
        print("\n=== ANALYSIS ===")
        print(f"Initial count: {len(initial_categories)}")
        print(f"After POST count: {len(after_categories)}")
        
        if len(after_categories) > len(initial_categories):
            print("✅ SUCCESS: Category persisted and visible in GET request!")
            
            # Check if our specific category is there
            found = any(cat.get('nama') == test_name for cat in after_categories)
            if found:
                print("✅ Our test category is present in the list!")
                return True
            else:
                print("⚠️  Category count increased but our test category not found")
                return False
        else:
            print("❌ PERSISTENCE ISSUE: Category not visible in GET request")
            return False
            
    except requests.exceptions.ConnectError:
        print("❌ Cannot connect to server. Is it running?")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def main():
    """Main test function"""
    print("=== PERSISTENCE FIX TEST ===")
    
    # Start server
    server_process = start_server()
    
    try:
        # Test persistence
        success = test_persistence()
        
        if success:
            print("\n🎉 PERSISTENCE FIX SUCCESSFUL!")
        else:
            print("\n❌ PERSISTENCE ISSUE STILL EXISTS")
            
    finally:
        # Clean up server process
        print("\nShutting down server...")
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            server_process.kill()

if __name__ == "__main__":
    main()
