@echo off
echo.
echo =======================================================
echo Database Connection Test Tool
echo =======================================================
echo.

cd "%~dp0backend"

echo Checking PostgreSQL service...
sc query postgresql-x64-16 | find "RUNNING" >NUL
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] PostgreSQL service is not running!
    echo.
    echo Would you like to start it? (Y/N)
    set /p startPg=
    if /i "%startPg%"=="Y" (
        echo Starting PostgreSQL service...
        net start postgresql-x64-16
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to start PostgreSQL service.
            goto :end
        ) else (
            echo [SUCCESS] PostgreSQL service started.
        )
    ) else (
        echo PostgreSQL service will remain stopped.
        goto :end
    )
) else (
    echo [OK] PostgreSQL service is running.
)

echo.
echo Activating virtual environment...
call env\Scripts\activate.bat

echo.
echo Testing database connection...
python -c "import psycopg2; conn=psycopg2.connect('dbname=budget_db user=postgres password=matchalatte host=localhost'); print('[SUCCESS] Database connection successful!'); cursor=conn.cursor(); cursor.execute('SELECT COUNT(*) FROM categories'); print('Found %d categories in database.' %% cursor.fetchone()[0]); cursor.execute('SELECT COUNT(*) FROM transactions'); print('Found %d transactions in database.' %% cursor.fetchone()[0]);" 2>NUL

if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to connect to the database!
    echo.
    echo Common issues:
    echo  - PostgreSQL service is not running
    echo  - Database "budget_db" does not exist
    echo  - Incorrect username or password
    echo  - Missing tables in the database

    echo.
    echo Would you like to create the database and tables? (Y/N)
    set /p createDb=
    if /i "%createDb%"=="Y" (
        echo Creating database and tables...
        echo This might take a moment...
        
        psql -U postgres -c "CREATE DATABASE budget_db;" 2>NUL
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to create the database.
            goto :end
        )
        
        python -c "from app.models import Category, Transaction, Base; from sqlalchemy import create_engine; engine = create_engine('postgresql://postgres:matchalatte@localhost/budget_db'); Base.metadata.create_all(engine); print('[SUCCESS] Database tables created successfully!')" 2>NUL
        if %ERRORLEVEL% NEQ 0 (
            echo [ERROR] Failed to create database tables.
        ) else (
            echo [SUCCESS] Database and tables created successfully.
        )
    )
)

:end
echo.
echo Test completed.
pause
