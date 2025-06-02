@echo off
echo === Fixed Backend Server Startup ===
cd /d "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

echo Activating virtual environment...
call .\env\Scripts\activate.bat

echo Starting server with fixed startup method...
python start_server_fixed.py

pause
