# PowerShell script to start backend with CORS fix
Write-Host "Starting Backend Server with CORS Fix..." -ForegroundColor Yellow

# Change to backend directory
Set-Location backend

# Activate virtual environment
& ..\env\Scripts\Activate.ps1

# Start the server
Write-Host "Starting pserve..." -ForegroundColor Green
pserve development.ini --reload
