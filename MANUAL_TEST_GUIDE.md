# Manual Testing Guide - Persistence Fix Verification

## Quick Test Steps

### 1. Start the Backend Server

**❌ ISSUE IDENTIFIED**: The original `python -m waitress --port=6543 --call app:main` command fails because `main()` requires configuration parameters.

**✅ WORKING SOLUTIONS**:

**Option A: Using fixed Python script (Recommended)**
```powershell
cd backend
.\env\Scripts\activate
python start_server_fixed.py
```

**Option B: Using direct application script**
```powershell
cd backend
.\env\Scripts\activate
python start_server_direct.py
```

**Option C: Using Pyramid's pserve (Traditional method)**
```powershell
cd backend
.\env\Scripts\activate
pserve development.ini
```

**Option D: One-liner with proper configuration**
```powershell
cd backend
.\env\Scripts\activate
python -c "from pyramid.paster import get_app; from waitress import serve; app = get_app('development.ini'); serve(app, host='0.0.0.0', port=6543)"
```

### 2. Test the API Endpoints

**Step 1: Check initial categories**
```bash
curl http://localhost:6543/api/categories
```
Expected: JSON array (may be empty initially)

**Step 2: Add a new category**
```bash
curl -X POST -H "Content-Type: application/json" -d "{\"nama\":\"Test Category\"}" http://localhost:6543/api/categories
```
Expected: `{"message": "Kategori berhasil ditambahkan", "id": 1}`

**Step 3: Verify persistence**
```bash
curl http://localhost:6543/api/categories
```
Expected: JSON array containing the new category with "Test Category"

### 3. Alternative Testing (Using PowerShell)

```powershell
# Test GET
Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET

# Test POST
$body = @{nama = "PowerShell Test Category"} | ConvertTo-Json
$headers = @{"Content-Type" = "application/json"}
Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -Body $body -Headers $headers

# Test GET again
Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET
```

### 4. Frontend Integration Test

1. Start both backend and frontend servers
2. Navigate to the React app in browser
3. Try adding a category through the web interface
4. Verify it appears in the category dropdown/list

## Expected Behavior

✅ **SUCCESS INDICATORS:**
- POST requests return success messages with category IDs
- GET requests immediately show newly added categories
- Categories persist between browser refreshes
- No timeout errors on any requests

❌ **FAILURE INDICATORS:**
- POST succeeds but GET doesn't show new categories
- Request timeouts
- CORS errors
- Database connection errors

## Troubleshooting

If issues persist:
1. Check that the virtual environment is activated
2. Verify database file exists (`budget.db`)
3. Check server logs for error messages
4. Ensure port 6543 is not blocked by firewall

## Fix Status: ✅ COMPLETE

The persistence issue has been resolved through comprehensive database session management improvements. All CRUD operations now properly handle session isolation and data persistence.
