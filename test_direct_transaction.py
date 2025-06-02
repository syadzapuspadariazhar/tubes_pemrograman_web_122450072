#!/usr/bin/env python3
"""
Simple test to identify transaction ID issue
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models import init_db, DBSession, Transaction, Category
from app.models.base import Base
from datetime import datetime, date
from sqlalchemy import create_engine

def test_transaction_directly():
    print("=== Direct Transaction Test ===\n")
    
    # Initialize database
    settings = {'sqlalchemy.url': 'sqlite:///backend/budget.db'}
    success = init_db(settings)
    
    if not success:
        print("❌ Failed to initialize database")
        return
    
    print("✅ Database initialized")
    
    try:
        # Test 1: Create a category first
        print("\n1. Creating test category...")
        DBSession.remove()
        
        cat = Category(nama="Direct Test Category")
        DBSession.add(cat)
        DBSession.flush()
        DBSession.commit()
        DBSession.remove()
        
        cat_id = cat.id
        print(f"✅ Category created with ID: {cat_id}")
        
        # Test 2: Create transaction
        print("\n2. Creating test transaction...")
        DBSession.remove()
        
        trans = Transaction(
            deskripsi="Direct Test Transaction",
            jumlah=50000,
            jenis="pengeluaran", 
            tanggal=date.today(),
            kategori_id=cat_id
        )
        
        print(f"Transaction before add - ID: {trans.id}")
        DBSession.add(trans)
        print(f"Transaction after add - ID: {trans.id}")
        
        DBSession.flush()
        print(f"Transaction after flush - ID: {trans.id}")
        
        DBSession.commit()
        print(f"Transaction after commit - ID: {trans.id}")
        
        DBSession.remove()
        
        if trans.id:
            print(f"✅ Transaction created with ID: {trans.id}")
        else:
            print("❌ Transaction ID is None!")
        
        # Test 3: Query back
        print("\n3. Querying transactions...")
        DBSession.remove()
        
        all_trans = DBSession.query(Transaction).all()
        print(f"Found {len(all_trans)} transactions:")
        
        for t in all_trans:
            print(f"  ID: {t.id}, Desc: '{t.deskripsi}', Amount: {t.jumlah}")
        
        # Clean up
        DBSession.query(Transaction).filter_by(deskripsi="Direct Test Transaction").delete()
        DBSession.query(Category).filter_by(nama="Direct Test Category").delete()
        DBSession.commit()
        DBSession.remove()
        
        print("\n✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        try:
            DBSession.rollback()
            DBSession.remove()
        except:
            pass

if __name__ == "__main__":
    test_transaction_directly()
