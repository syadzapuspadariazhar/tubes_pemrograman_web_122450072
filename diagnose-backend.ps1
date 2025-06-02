# diagnose-backend.ps1
# Script to diagnose backend connectivity issues

Write-Host "Backend Diagnostics Tool" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Check if PostgreSQL is running
Write-Host "Checking PostgreSQL service..." -ForegroundColor Yellow
$pgService = Get-Service -Name "postgresql*" -ErrorAction SilentlyContinue
if ($pgService) {
    Write-Host "PostgreSQL service found: $($pgService.Name) - Status: $($pgService.Status)" -ForegroundColor Green
    if ($pgService.Status -ne "Running") {
        Write-Host "PostgreSQL service is not running. Starting the service..." -ForegroundColor Red
        try {
            Start-Service $pgService.Name
            Write-Host "PostgreSQL service started successfully." -ForegroundColor Green
        }
        catch {
            Write-Host "Failed to start PostgreSQL service. You may need to start it manually." -ForegroundColor Red
        }
    }
} else {
    Write-Host "PostgreSQL service not found. Is PostgreSQL installed?" -ForegroundColor Red
}

# Check if Python and virtual environment are working
Write-Host ""
Write-Host "Checking Python virtual environment..." -ForegroundColor Yellow
$pythonPath = ".\backend\env\Scripts\python.exe"
if (Test-Path $pythonPath) {
    Write-Host "Python virtual environment found." -ForegroundColor Green
    try {
        $pythonVersion = & $pythonPath --version
        Write-Host "Python version: $pythonVersion" -ForegroundColor Green
    }
    catch {
        Write-Host "Failed to get Python version." -ForegroundColor Red
    }
} else {
    Write-Host "Python virtual environment not found at $pythonPath" -ForegroundColor Red
}

# Check if database connection works
Write-Host ""
Write-Host "Testing database connection..." -ForegroundColor Yellow
try {
    $dbTestResult = & $pythonPath -c "import psycopg2; conn=psycopg2.connect('dbname=budget_db user=postgres password=matchalatte host=localhost'); print('Connected successfully!')"
    Write-Host $dbTestResult -ForegroundColor Green
}
catch {
    Write-Host "Database connection test failed:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Check if port 6543 is available
Write-Host ""
Write-Host "Checking if port 6543 is in use..." -ForegroundColor Yellow
$portInUse = Get-NetTCPConnection -LocalPort 6543 -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Host "Port 6543 is already in use by process ID: $($portInUse.OwningProcess)" -ForegroundColor Red
    try {
        $process = Get-Process -Id $portInUse.OwningProcess -ErrorAction SilentlyContinue
        if ($process) {
            Write-Host "Process using port 6543: $($process.Name)" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "Could not identify the process using port 6543." -ForegroundColor Red
    }
} else {
    Write-Host "Port 6543 is available." -ForegroundColor Green
}

# Try to start backend server as a test
Write-Host ""
Write-Host "Trying to start backend server..." -ForegroundColor Yellow
Write-Host "This will start the server for 5 seconds to test if it launches correctly." -ForegroundColor Yellow

$backendStartCommand = @"
cd .\backend
.\env\Scripts\Activate.ps1
python -c "from pyramid.paster import get_app; from waitress import serve; import threading; import time; app = get_app('development.ini', 'main'); print('Backend test: Server started successfully!'); threading.Timer(5, lambda: exit()).start(); serve(app, host='0.0.0.0', port=6543)" 2>&1
"@

try {
    $startResult = Invoke-Expression $backendStartCommand
    Write-Host $startResult -ForegroundColor Green
    Write-Host "Backend server test completed." -ForegroundColor Green
}
catch {
    Write-Host "Failed to start backend server:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
}

# Summary and recommendations
Write-Host ""
Write-Host "Diagnostics Complete" -ForegroundColor Cyan
Write-Host "=================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Recommendations:" -ForegroundColor Yellow
Write-Host "1. Make sure PostgreSQL service is running" -ForegroundColor White
Write-Host "2. Verify the database 'budget_db' exists with proper credentials" -ForegroundColor White
Write-Host "3. Confirm no other application is using port 6543" -ForegroundColor White
Write-Host "4. Try running the start_backend.bat script" -ForegroundColor White
Write-Host "5. Check the network settings and firewall rules" -ForegroundColor White
Write-Host ""
Write-Host "To start the complete application, run: ./start_app.ps1" -ForegroundColor Green