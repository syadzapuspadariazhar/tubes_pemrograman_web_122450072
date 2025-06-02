@echo off
title Budget App - Startup Manager

echo ========================================================
echo            BUDGET APP STARTUP MANAGER
echo ========================================================
echo.

:: Check if PostgreSQL is running
echo Checking PostgreSQL service...
sc query postgresql-x64-16 | find "RUNNING" >NUL
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] PostgreSQL service may not be running.
    echo This might cause database connection issues.
    echo.
    pause
)

:: Check if port 6543 is available
echo Checking if port 6543 is available...
netstat -ano | find "6543" | find "LISTENING" >NUL
if %ERRORLEVEL% EQU 0 (
    echo [WARNING] Port 6543 is already in use.
    echo The backend server might not start correctly.
    echo.
    pause
)

echo All pre-flight checks completed.

:menu
cls
echo Choose an option:
echo.
echo [1] Start both Backend and Frontend
echo [2] Start Backend Only
echo [3] Start Frontend Only
echo [4] Run Database Test
echo [5] Run Backend Diagnostics
echo [6] Open Backend Test Page
echo [0] Exit
echo.

set /p choice=Enter your choice (0-6): 

if "%choice%"=="0" goto end
if "%choice%"=="1" goto both
if "%choice%"=="2" goto backend
if "%choice%"=="3" goto frontend
if "%choice%"=="4" goto dbtest
if "%choice%"=="5" goto diagnose
if "%choice%"=="6" goto testpage
goto menu

:both
echo.
echo Starting Backend and Frontend...
echo.
start cmd /k "title Budget Backend && cd backend && call env\Scripts\activate.bat && python -c \"from pyramid.paster import get_app; from waitress import serve; app = get_app('development.ini', 'main'); print('Backend server running at: http://localhost:6543'); serve(app, host='0.0.0.0', port=6543)\""
echo Backend starting...
timeout /t 5 /nobreak > nul
start cmd /k "title Budget Frontend && cd frontend && npm start"
echo Frontend starting...
echo.
echo Both servers are starting in separate windows.
echo.
pause
goto menu

:backend
echo.
echo Starting Backend...
echo.
start cmd /k "title Budget Backend && cd backend && call env\Scripts\activate.bat && python -c \"from pyramid.paster import get_app; from waitress import serve; app = get_app('development.ini', 'main'); print('Backend server running at: http://localhost:6543'); serve(app, host='0.0.0.0', port=6543)\""
echo.
echo Backend server starting in a new window.
echo.
pause
goto menu

:frontend
echo.
echo Starting Frontend...
echo.
start cmd /k "title Budget Frontend && cd frontend && npm start:standalone"
echo.
echo Frontend server starting in a new window.
echo.
pause
goto menu

:dbtest
echo.
echo Running Database Test...
echo.
call test-database.bat
goto menu

:diagnose
echo.
echo Running Backend Diagnostics...
echo.
powershell -File diagnose-backend.ps1
echo.
pause
goto menu

:testpage
echo.
echo Opening Backend Test Page...
echo.
start backend-test.html
echo.
pause
goto menu

:end
echo.
echo Thank you for using Budget App!
echo.
pause
exit
