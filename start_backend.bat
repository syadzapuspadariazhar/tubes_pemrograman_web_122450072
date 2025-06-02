@echo off
echo.
echo ===== Budget App Backend Server =====
echo.

:: Change to the backend directory
cd "%~dp0backend"

:: Activate the virtual environment
echo Activating virtual environment...
call env\Scripts\activate.bat || (
    echo Failed to activate virtual environment!
    echo Please make sure the virtual environment exists.
    pause
    exit /b 1
)

:: Check if the PostgreSQL service is running
echo Checking PostgreSQL service...
sc query postgresql-x64-16 | findstr "RUNNING" > nul
if %ERRORLEVEL% NEQ 0 (
    echo PostgreSQL service is not running!
    echo Starting PostgreSQL service...
    net start postgresql-x64-16 || (
        echo Failed to start PostgreSQL service!
        echo Please start it manually.
    )
)

:: Test database connection
echo Testing database connection...
python -c "import psycopg2; conn=psycopg2.connect('dbname=budget_db user=postgres password=matchalatte host=localhost'); print('Database connection successful!')" || (
    echo PostgreSQL connection failed!
    echo Please check your database settings in development.ini.
    pause
    exit /b 1
)

:: Check if port 6543 is already in use
echo Checking if port 6543 is available...
netstat -ano | findstr :6543 | findstr LISTENING > nul
if %ERRORLEVEL% EQU 0 (
    echo Warning: Port 6543 is already in use!
    echo Please close any other applications using this port.
    choice /M "Continue anyway"
    if %ERRORLEVEL% NEQ 1 (
        echo Aborting server startup.
        pause
        exit /b 1
    )
)

:: Start the Pyramid server
echo.
echo Starting Pyramid server...
echo Server will be available at: http://localhost:6543
echo Press Ctrl+C to stop the server.
echo.
python -c "from pyramid.paster import get_app; from waitress import serve; app = get_app('development.ini', 'main'); print('Backend server running at: http://localhost:6543'); serve(app, host='0.0.0.0', port=6543)"

pause
