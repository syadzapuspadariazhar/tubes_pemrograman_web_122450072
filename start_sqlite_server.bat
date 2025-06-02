@echo off
echo Starting Backend Server with SQLite...
echo.

cd backend
call env\Scripts\activate.bat

echo Testing Python and imports...
python -c "print('Python is working'); import app; print('App imported successfully')"

echo.
echo Starting server...
echo Server will be available at http://localhost:6543
echo Press Ctrl+C to stop the server
echo.

pserve development.ini --reload

pause
