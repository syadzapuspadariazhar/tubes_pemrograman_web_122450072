@echo off
echo === PERSISTENCE FIX TEST ===
cd /d "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

echo Current directory: %CD%

echo Activating virtual environment...
call .\env\Scripts\activate.bat

echo Starting server in background...
start /b python -m waitress --port=6543 --call app:main > server.log 2>&1

echo Waiting for server to start...
timeout /t 8 /nobreak > nul

echo Testing GET endpoint...
curl -s http://localhost:6543/api/categories
echo.

echo Testing POST endpoint...
curl -s -X POST -H "Content-Type: application/json" -d "{\"nama\":\"Test Category\"}" http://localhost:6543/api/categories
echo.

echo Waiting a moment...
timeout /t 2 /nobreak > nul

echo Testing GET after POST...
curl -s http://localhost:6543/api/categories
echo.

echo Stopping server...
taskkill /f /im python.exe 2>nul

echo Test complete.
pause
