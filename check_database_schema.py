#!/usr/bin/env python3
"""
Check database schema for transactions table
"""

import sqlite3
import os

def check_database_schema():
    print("=== Checking Database Schema ===\n")
    
    db_path = "backend/budget.db"
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tables in database: {[t[0] for t in tables]}")
        
        # Check transactions table schema
        if ('transactions',) in tables:
            print("\n📊 Transactions table schema:")
            cursor.execute("PRAGMA table_info(transactions)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]}) - PK: {col[5]}, Not Null: {col[3]}, Default: {col[4]}")
            
            # Check if there are any transactions
            cursor.execute("SELECT COUNT(*) FROM transactions")
            count = cursor.fetchone()[0]
            print(f"\n📈 Total transactions in database: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM transactions ORDER BY id DESC LIMIT 3")
                transactions = cursor.fetchall()
                print("\n📝 Last 3 transactions:")
                for trans in transactions:
                    print(f"  ID: {trans[0]}, Desc: '{trans[1]}', Amount: {trans[2]}")
        else:
            print("❌ Transactions table not found!")
        
        # Check categories table for comparison
        if ('categories',) in tables:
            print("\n📊 Categories table schema:")
            cursor.execute("PRAGMA table_info(categories)")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]}) - PK: {col[5]}, Not Null: {col[3]}, Default: {col[4]}")
            
            cursor.execute("SELECT COUNT(*) FROM categories")
            count = cursor.fetchone()[0]
            print(f"\n📈 Total categories in database: {count}")
            
            if count > 0:
                cursor.execute("SELECT * FROM categories ORDER BY id DESC LIMIT 3")
                categories = cursor.fetchall()
                print("\n📝 Last 3 categories:")
                for cat in categories:
                    print(f"  ID: {cat[0]}, Name: '{cat[1]}'")
        
        # Test auto-increment manually
        print("\n🧪 Testing auto-increment manually:")
        try:
            cursor.execute("INSERT INTO transactions (deskripsi, jumlah, jenis, tanggal, kategori_id) VALUES (?, ?, ?, ?, ?)",
                         ("Manual Test", 1000, "pengeluaran", "2025-06-02", 1))
            conn.commit()
            
            # Get the ID of the inserted row
            cursor.execute("SELECT last_insert_rowid()")
            new_id = cursor.fetchone()[0]
            print(f"✅ Manual insert successful, new ID: {new_id}")
            
            # Clean up
            cursor.execute("DELETE FROM transactions WHERE id = ?", (new_id,))
            conn.commit()
            print("✅ Test transaction cleaned up")
            
        except Exception as e:
            print(f"❌ Manual insert failed: {e}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database check failed: {e}")

if __name__ == "__main__":
    check_database_schema()
