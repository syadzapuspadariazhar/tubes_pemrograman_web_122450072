import os
import sys
import subprocess
import time

def run_test():
    """Run comprehensive test"""
    print("=== COMPREHENSIVE PERSISTENCE TEST ===")
    
    # Change to backend directory
    backend_dir = r"c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
    os.chdir(backend_dir)
    
    # Test 1: Check if database file exists
    db_files = ["budget.db", "app.db"]
    for db_file in db_files:
        if os.path.exists(db_file):
            size = os.path.getsize(db_file)
            print(f"✅ Database found: {db_file} ({size} bytes)")
        else:
            print(f"❌ Database not found: {db_file}")
    
    # Test 2: Try to start server and test endpoints
    print("\n=== STARTING SERVER TEST ===")
    
    try:
        # Start server
        print("Starting server...")
        activate_cmd = r".\env\Scripts\activate.bat"
        server_cmd = "python -m waitress --port=6543 --call app:main"
        
        # Use subprocess to start server
        process = subprocess.Popen(
            f"{activate_cmd} && {server_cmd}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=backend_dir
        )
        
        # Wait for server to start
        time.sleep(8)
        
        # Test endpoints with curl
        print("Testing GET endpoint...")
        get_result = subprocess.run(
            ["curl", "-s", "http://localhost:6543/api/categories"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if get_result.returncode == 0:
            print(f"✅ GET successful: {get_result.stdout}")
        else:
            print(f"❌ GET failed: {get_result.stderr}")
        
        # Test POST endpoint
        print("Testing POST endpoint...")
        post_data = '{"nama":"Test Category from Script"}'
        post_result = subprocess.run([
            "curl", "-s", "-X", "POST",
            "-H", "Content-Type: application/json",
            "-d", post_data,
            "http://localhost:6543/api/categories"
        ], capture_output=True, text=True, timeout=10)
        
        if post_result.returncode == 0:
            print(f"✅ POST successful: {post_result.stdout}")
        else:
            print(f"❌ POST failed: {post_result.stderr}")
        
        # Test GET again
        print("Testing GET after POST...")
        time.sleep(2)
        get_after_result = subprocess.run(
            ["curl", "-s", "http://localhost:6543/api/categories"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if get_after_result.returncode == 0:
            print(f"✅ GET after POST: {get_after_result.stdout}")
            
            # Simple check for persistence
            if "Test Category from Script" in get_after_result.stdout:
                print("\n🎉 SUCCESS: PERSISTENCE WORKING!")
            else:
                print("\n❌ PERSISTENCE ISSUE: Category not found in GET")
        else:
            print(f"❌ GET after POST failed: {get_after_result.stderr}")
        
    except Exception as e:
        print(f"❌ Server test failed: {e}")
    finally:
        # Cleanup
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass
        print("\nServer stopped.")

if __name__ == "__main__":
    run_test()
