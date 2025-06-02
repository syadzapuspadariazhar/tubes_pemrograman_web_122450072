#!/usr/bin/env python3
"""
Test script to diagnose the data persistence issue
"""
import requests
import json
import time
import sys

SERVER_URL = "http://localhost:6543"

def test_get_categories():
    """Test GET /api/categories"""
    try:
        response = requests.get(f"{SERVER_URL}/api/categories")
        print(f"GET /api/categories - Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"Error in GET: {e}")
        return []

def test_post_category(name):
    """Test POST /api/categories"""
    try:
        data = {"nama": name}
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{SERVER_URL}/api/categories", 
                               json=data, headers=headers)
        print(f"POST /api/categories - Status: {response.status_code}")
        print(f"Response: {response.text}")
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        print(f"Error in POST: {e}")
        return None

def check_database_directly():
    """Check database directly using SQLite"""
    import sqlite3
    import os
    
    # Try different possible database paths
    possible_paths = [
        "backend/app.db",
        "backend/budget.db", 
        "app.db",
        "budget.db"
    ]
    
    for db_path in possible_paths:
        if os.path.exists(db_path):
            print(f"\nFound database: {db_path}")
            print(f"Size: {os.path.getsize(db_path)} bytes")
            
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # List tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                print(f"Tables: {tables}")
                
                # Check categories table if it exists
                if any('categories' in str(table) for table in tables):
                    cursor.execute("SELECT * FROM categories")
                    categories = cursor.fetchall()
                    print(f"Categories in DB: {categories}")
                
                conn.close()
            except Exception as e:
                print(f"Error accessing {db_path}: {e}")
        else:
            print(f"Database not found: {db_path}")

def main():
    print("=== Data Persistence Test ===")
    
    # Check current state
    print("\n1. Initial GET request:")
    initial_categories = test_get_categories()
    
    # Add a new category
    print("\n2. Adding new category:")
    post_result = test_post_category("Test Category " + str(int(time.time())))
    
    # Check if it appears immediately
    print("\n3. GET request after POST:")
    after_post_categories = test_get_categories()
    
    # Check database directly
    print("\n4. Direct database check:")
    check_database_directly()
    
    # Analysis
    print("\n=== ANALYSIS ===")
    print(f"Initial categories count: {len(initial_categories)}")
    print(f"After POST categories count: {len(after_post_categories)}")
    print(f"POST successful: {post_result is not None}")
    
    if post_result and len(after_post_categories) <= len(initial_categories):
        print("❌ PERSISTENCE ISSUE: POST succeeded but category not visible in GET")
    elif post_result and len(after_post_categories) > len(initial_categories):
        print("✅ SUCCESS: Category persisted and visible")
    else:
        print("❌ POST FAILED: Could not add category")

if __name__ == "__main__":
    main()
