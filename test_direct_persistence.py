#!/usr/bin/env python3
"""
Direct test of the persistence fix without server startup complexity
"""
import sys
import os

# Add the backend directory to Python path
backend_path = r"c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
sys.path.insert(0, backend_path)

# Change to backend directory
os.chdir(backend_path)

def test_database_directly():
    """Test database operations directly"""
    try:
        # Import after setting path
        from app.models import DBSession, Category, init_db
        
        print("=== DIRECT DATABASE TEST ===")
        
        # Initialize database
        settings = {'sqlalchemy.url': 'sqlite:///budget.db'}
        if not init_db(settings):
            print("❌ Failed to initialize database")
            return False
            
        print("✅ Database initialized")
        
        # Test 1: Check initial categories
        DBSession.remove()  # Clean session
        initial_categories = DBSession.query(Category).all()
        print(f"Initial categories: {len(initial_categories)}")
        for cat in initial_categories:
            print(f"  - {cat.id}: {cat.nama}")
        
        # Test 2: Add a new category
        print("\nAdding new category...")
        test_name = f"Direct Test Category"
        new_cat = Category(nama=test_name)
        
        DBSession.add(new_cat)
        DBSession.flush()  # Get ID
        print(f"Category added with ID: {new_cat.id}")
        
        DBSession.commit()
        print("✅ Commit successful")
        
        # Force session cleanup
        DBSession.remove()
        
        # Test 3: Verify persistence
        print("\nChecking persistence...")
        DBSession.remove()  # Fresh session
        after_categories = DBSession.query(Category).all()
        print(f"Categories after add: {len(after_categories)}")
        for cat in after_categories:
            print(f"  - {cat.id}: {cat.nama}")
            
        # Check if our category is there
        found = any(cat.nama == test_name for cat in after_categories)
        
        if found and len(after_categories) > len(initial_categories):
            print("\n✅ SUCCESS: Persistence working correctly!")
            return True
        else:
            print("\n❌ PERSISTENCE ISSUE: Category not found after commit")
            return False
            
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            DBSession.remove()
        except:
            pass

if __name__ == "__main__":
    success = test_database_directly()
    print(f"\nTest result: {'PASSED' if success else 'FAILED'}")
