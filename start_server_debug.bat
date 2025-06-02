@echo off
echo Starting Backend Server with Timeout Fix...
cd backend
call env\Scripts\activate.bat
echo.
echo Server starting on http://localhost:6543
echo Press Ctrl+C to stop
echo.
pserve development.ini --reload
