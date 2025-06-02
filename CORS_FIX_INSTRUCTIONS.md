# CORS Fix Instructions - Manual Steps

## 🎯 Current Status
The CORS configuration has been updated in the backend code, but the server needs to be restarted for changes to take effect.

## 📋 Manual Steps to Fix CORS Issue

### Step 1: Start Backend Server Manually
1. Open a new PowerShell window
2. Navigate to the project directory:
   ```powershell
   cd "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072"
   ```
3. Change to backend directory and activate virtual environment:
   ```powershell
   cd backend
   ..\env\Scripts\Activate.ps1
   ```
4. Start the server:
   ```powershell
   pserve development.ini --reload
   ```

### Step 2: Test CORS Fix
1. Open `cors-test.html` in your browser
2. Click "Run All Tests" to verify CORS is working
3. Or manually test with browser developer tools

### Step 3: Test Frontend Connection
1. Go to the Categories page in your React app
2. Click "Test Connection" button
3. Try adding a new category

## 🔧 What Was Fixed

### Backend Changes Made:
1. **Enhanced CORS Handler** (`backend/app/views/cors.py`):
   - Added proper OPTIONS request handling
   - Added multiple fallback handlers
   - Improved CORS headers

2. **Updated Routes** (`backend/app/routes.py`):
   - Added comprehensive CORS route matching
   - Added global catchall for missed routes

3. **Frontend Improvements** (`frontend/src/contexts/AppContext.jsx`):
   - Better CORS error detection
   - Enhanced error messages

## 🚀 Quick Test Commands

### Test Backend Status:
```powershell
# Check if server is running
netstat -an | findstr :6543

# Test API directly
curl http://localhost:6543/api/categories
```

### Test CORS Specifically:
```powershell
# Test OPTIONS request
curl -X OPTIONS -v http://localhost:6543/api/categories
```

## ✅ Expected Results After Fix

1. **No CORS errors** in browser console
2. **OPTIONS requests return 200 OK** with proper headers
3. **POST requests work** for adding categories
4. **Frontend shows "Backend connected"** status

## 🔍 Troubleshooting

If CORS issues persist:

1. **Clear browser cache** completely
2. **Restart both frontend and backend**
3. **Check browser developer tools** for exact error messages
4. **Use cors-test.html** for isolated testing

## 📱 Alternative: Use Chrome with CORS Disabled

For testing purposes only:
```cmd
chrome.exe --user-data-dir="C:\temp" --disable-web-security --disable-features=VizDisplayCompositor
```

⚠️ **Warning**: Only use this for development testing!

---

The CORS issue should be resolved once you manually restart the backend server with the updated configuration. The enhanced CORS handlers will properly respond to preflight requests and allow the frontend to communicate with the backend.
