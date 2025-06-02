# PowerShell script to start server and test endpoints
Write-Host "=== Backend Server Startup and Test ===" -ForegroundColor Yellow

# Change to backend directory
Set-Location "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& .\env\Scripts\Activate.ps1

# Start server in background job
Write-Host "Starting server..." -ForegroundColor Cyan
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
    & .\env\Scripts\Activate.ps1
    .\env\Scripts\pserve.exe development.ini
}

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Check if server is running
$port = Get-NetTCPConnection -LocalPort 6543 -ErrorAction SilentlyContinue
if ($port) {
    Write-Host "✅ Server is running on port 6543" -ForegroundColor Green
    
    # Test GET endpoint
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 10
        Write-Host "✅ GET /api/categories works" -ForegroundColor Green
        Write-Host "Categories: $($response | ConvertTo-Json -Compress)" -ForegroundColor White
    } catch {
        Write-Host "❌ GET /api/categories failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test POST endpoint
    try {
        $body = @{ nama = "PowerShell Test Category" } | ConvertTo-Json
        $headers = @{ "Content-Type" = "application/json" }
        $response = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -Body $body -Headers $headers -TimeoutSec 10
        Write-Host "✅ POST /api/categories works!" -ForegroundColor Green
        Write-Host "Response: $($response | ConvertTo-Json -Compress)" -ForegroundColor White
    } catch {
        Write-Host "❌ POST /api/categories failed: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "Error details: $($_.Exception)" -ForegroundColor Red
    }
    
} else {
    Write-Host "❌ Server is NOT running on port 6543" -ForegroundColor Red
    
    # Check job status
    $jobState = Get-Job $serverJob.Id
    Write-Host "Server job state: $($jobState.State)" -ForegroundColor Yellow
    
    if ($jobState.State -eq "Failed") {
        Write-Host "Server job output:" -ForegroundColor Yellow
        Receive-Job $serverJob.Id
    }
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Yellow
Write-Host "Server job ID: $($serverJob.Id)" -ForegroundColor Cyan
Write-Host "Use 'Stop-Job $($serverJob.Id)' to stop the server" -ForegroundColor Cyan
