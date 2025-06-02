# Quick test to verify POST timeout fix
Write-Host "🔧 TESTING POST TIMEOUT FIX" -ForegroundColor Yellow
Write-Host "=" * 40

# Start server if not running
Write-Host "1. Starting server..." -ForegroundColor Cyan
Start-Process -FilePath "start_server_debug.bat" -WindowStyle Minimized

# Wait for startup
Write-Host "2. Waiting for server startup..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Test endpoints
Write-Host "3. Testing GET endpoint..." -ForegroundColor Cyan
try {
    $getResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 5
    Write-Host "   ✅ GET works: $($getResponse | ConvertTo-Json -Compress)" -ForegroundColor Green
} catch {
    Write-Host "   ❌ GET failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "4. Testing POST endpoint..." -ForegroundColor Cyan
try {
    $postData = @{ nama = "test_timeout_fix" } | ConvertTo-Json
    $postResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -ContentType "application/json" -Body $postData -TimeoutSec 15
    Write-Host "   ✅ POST works: $($postResponse | ConvertTo-Json -Compress)" -ForegroundColor Green
    
    # Verify the category was added
    $verifyResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 5
    Write-Host "   ✅ Verification: $($verifyResponse | ConvertTo-Json -Compress)" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "🎉 SUCCESS: POST timeout has been FIXED!" -ForegroundColor Green
    Write-Host "The React frontend should now be able to add categories." -ForegroundColor Green
    
} catch {
    if ($_.Exception.Message -like "*timeout*") {
        Write-Host "   ❌ POST still timing out" -ForegroundColor Red
        Write-Host "   Need to investigate further..." -ForegroundColor Yellow
    } else {
        Write-Host "   ❌ POST failed: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Next step: Test the React frontend to see if it can now add categories successfully." -ForegroundColor Cyan
