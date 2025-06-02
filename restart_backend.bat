@echo off
echo === Restarting Backend Server with CORS Fix ===

REM Kill any existing processes
taskkill /f /im pserve.exe 2>nul
taskkill /f /im python.exe 2>nul

echo Waiting for processes to stop...
timeout /t 3 /nobreak >nul

echo Starting backend server...
cd backend
call ..\env\Scripts\activate.bat
pserve development.ini --reload

pause
