# PowerShell script to start the backend server correctly
Write-Host "=== Backend Server Startup ===" -ForegroundColor Yellow

# Navigate to backend directory
Set-Location "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\env\Scripts\activate.bat"

# Check if development.ini exists
if (Test-Path "development.ini") {
    Write-Host "✅ Configuration file found" -ForegroundColor Green
} else {
    Write-Host "❌ development.ini not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Starting server using pyramid pserve..." -ForegroundColor Cyan

try {
    # Start server using pserve (the proper Pyramid way)
    pserve development.ini
} catch {
    Write-Host "❌ pserve failed, trying alternative method..." -ForegroundColor Yellow
    
    # Alternative: Use Python script
    Write-Host "Starting with Python script..." -ForegroundColor Cyan
    python start_server_fixed.py
}

Write-Host "Server stopped." -ForegroundColor Yellow
