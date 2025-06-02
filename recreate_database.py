#!/usr/bin/env python3
"""
Recreate database with fixed Transaction model
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.models import init_db, DBSession
from app.models.base import Base
from sqlalchemy import create_engine

def recreate_database():
    print("=== Recreating Database with Fixed Transaction Model ===\n")
    
    # Remove existing database
    db_path = "backend/budget.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        print("✅ Removed existing database")
    
    # Initialize with corrected models
    settings = {'sqlalchemy.url': 'sqlite:///backend/budget.db'}
    
    # Create engine and recreate all tables
    engine = create_engine(settings['sqlalchemy.url'])
    Base.metadata.create_all(engine)
    
    print("✅ Database recreated with fixed Transaction model")
    print("✅ All tables created successfully")
    
    # Initialize the session
    success = init_db(settings)
    if success:
        print("✅ Database initialization completed")
    else:
        print("❌ Database initialization failed")

if __name__ == "__main__":
    recreate_database()
