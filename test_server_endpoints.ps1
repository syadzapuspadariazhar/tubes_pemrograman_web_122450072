# Test if server is running and test endpoints
Write-Host "Testing backend server..." -ForegroundColor Yellow

# Test if port 6543 is listening
$port = Get-NetTCPConnection -LocalPort 6543 -ErrorAction SilentlyContinue
if ($port) {
    Write-Host "✓ Server is listening on port 6543" -ForegroundColor Green
} else {
    Write-Host "✗ Server is NOT listening on port 6543" -ForegroundColor Red
    Write-Host "Starting server..." -ForegroundColor Yellow
    
    # Start server in background
    Set-Location backend
    & .\env\Scripts\Activate.ps1
    Start-Job -ScriptBlock { 
        Set-Location "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
        & .\env\Scripts\Activate.ps1
        pserve development.ini 
    }
    
    Write-Host "Waiting for server to start..." -ForegroundColor Yellow
    Start-Sleep -Seconds 10
}

# Test GET categories
try {
    $response = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 10
    Write-Host "✓ GET /api/categories works" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ GET /api/categories failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test POST categories
try {
    $body = @{ nama = "Test Category" } | ConvertTo-Json
    $response = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -Body $body -ContentType "application/json" -TimeoutSec 10
    Write-Host "✓ POST /api/categories works!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Cyan
} catch {
    Write-Host "✗ POST /api/categories failed: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "Test complete!" -ForegroundColor Yellow
