# Start Backend Server
Write-Host "Starting backend server..." -ForegroundColor Green

# Navigate to backend directory
Set-Location "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

# Activate virtual environment
& ".\env\Scripts\Activate.ps1"

# Start server
Write-Host "Server starting at http://localhost:6543" -ForegroundColor Yellow
pserve development.ini --reload
