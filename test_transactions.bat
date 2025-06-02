@echo off
echo Testing Transaction Persistence...
echo.

REM Start in the root directory
cd /d "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072"

REM Test the transaction API
python test_transaction_persistence.py

echo.
echo Test completed. Press any key to exit...
pause >nul
