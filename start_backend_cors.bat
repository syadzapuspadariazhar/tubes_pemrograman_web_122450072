@echo off
title Backend Server - Budget App (CORS Fixed)
color 0A

echo ========================================
echo   BACKEND SERVER - BUDGET APP
echo   CORS CONFIGURATION UPDATED
echo ========================================
echo.
echo [INFO] Starting backend server with CORS fix...
echo [INFO] Server will be available at: http://localhost:6543
echo [INFO] Press Ctrl+C to stop the server
echo [INFO] CORS headers configured for frontend access
echo.

REM Kill any existing processes
echo [INFO] Stopping existing backend processes...
taskkill /f /im pserve.exe 2>nul
taskkill /f /im python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [INFO] Activating virtual environment...
cd backend
call ..\env\Scripts\activate.bat

echo [INFO] Testing database connection...
python -c "from app.models import init_db; print('[DB] Connection status:', 'OK' if init_db({'sqlalchemy.url': 'postgresql://postgres:Puspa123@localhost/budget_db'}) else 'FAILED')" 2>nul

echo [INFO] Starting server with CORS configuration...
echo [INFO] CORS allows requests from: http://localhost:3000
echo [INFO] Available endpoints: /api/categories, /api/transactions
pserve development.ini --reload

echo.
echo [ERROR] Server stopped unexpectedly!
pause
