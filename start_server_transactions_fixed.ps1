# Start the backend server with transaction API fixes
Write-Host "Starting backend server with transaction persistence fixes..."

Set-Location "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

# Activate virtual environment
& ".\env\Scripts\Activate.ps1"

# Start the server
python start_server_fixed.py
