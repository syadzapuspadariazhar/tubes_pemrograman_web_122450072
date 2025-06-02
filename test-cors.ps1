#!/usr/bin/env powershell
Write-Host "Testing CORS preflight request to backend..." -ForegroundColor Yellow

# Wait for server to be ready
Start-Sleep -Seconds 2

try {
    # Test OPTIONS request
    $response = Invoke-WebRequest -Uri "http://localhost:6543/api/categories" -Method OPTIONS -ErrorAction Stop
    Write-Host "✅ OPTIONS request successful!" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Cyan
    Write-Host "Headers:" -ForegroundColor Cyan
    foreach ($header in $response.Headers.GetEnumerator()) {
        if ($header.Key -like "*Access-Control*") {
            Write-Host "  $($header.Key): $($header.Value)" -ForegroundColor White
        }
    }
} catch {
    Write-Host "❌ OPTIONS request failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}

try {
    # Test GET request for comparison
    $response = Invoke-WebRequest -Uri "http://localhost:6543/api/categories" -Method GET -ErrorAction Stop
    Write-Host "✅ GET request successful!" -ForegroundColor Green
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ GET request failed!" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor Red
}
