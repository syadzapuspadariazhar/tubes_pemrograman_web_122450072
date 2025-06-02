Write-Host "=== POST TIMEOUT DIAGNOSIS ===" -ForegroundColor Yellow
Write-Host ""

# Check if server is running
Write-Host "1. Checking server status..." -ForegroundColor Cyan
$port = Get-NetTCPConnection -LocalPort 6543 -ErrorAction SilentlyContinue
if ($port) {
    Write-Host "   ✅ Server is listening on port 6543" -ForegroundColor Green
} else {
    Write-Host "   ❌ Server is NOT listening on port 6543" -ForegroundColor Red
    Write-Host "   Please start the server first!" -ForegroundColor Red
    exit
}

# Test GET endpoint
Write-Host ""
Write-Host "2. Testing GET endpoint..." -ForegroundColor Cyan
try {
    $getStart = Get-Date
    $getResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 5
    $getDuration = ((Get-Date) - $getStart).TotalSeconds
    Write-Host "   ✅ GET successful in $([math]::Round($getDuration, 2))s" -ForegroundColor Green
    Write-Host "   Response: $($getResponse | ConvertTo-Json -Compress)" -ForegroundColor White
} catch {
    Write-Host "   ❌ GET failed: $($_.Exception.Message)" -ForegroundColor Red
}

# Test POST endpoint with monitoring
Write-Host ""
Write-Host "3. Testing POST endpoint (watching for timeout)..." -ForegroundColor Cyan
try {
    $postStart = Get-Date
    Write-Host "   Sending POST request..." -ForegroundColor White
    
    $postResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" `
        -Method POST `
        -ContentType "application/json" `
        -Body '{"nama":"test_from_powershell"}' `
        -TimeoutSec 15
    
    $postDuration = ((Get-Date) - $postStart).TotalSeconds
    Write-Host "   ✅ POST successful in $([math]::Round($postDuration, 2))s" -ForegroundColor Green
    Write-Host "   Response: $($postResponse | ConvertTo-Json -Compress)" -ForegroundColor White
    
} catch {
    $postDuration = ((Get-Date) - $postStart).TotalSeconds
    if ($_.Exception.Message -like "*timeout*") {
        Write-Host "   ❌ POST TIMEOUT after $([math]::Round($postDuration, 2))s" -ForegroundColor Red
        Write-Host "   This means the server received the request but didn't respond" -ForegroundColor Yellow
        Write-Host "   LIKELY CAUSE: Database transaction hanging or server process stuck" -ForegroundColor Yellow
    } else {
        Write-Host "   ❌ POST failed after $([math]::Round($postDuration, 2))s: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== DIAGNOSIS COMPLETE ===" -ForegroundColor Yellow

# Check database files
Write-Host ""
Write-Host "4. Checking database files..." -ForegroundColor Cyan
$dbFiles = Get-ChildItem "backend\budget.db*" -ErrorAction SilentlyContinue
if ($dbFiles) {
    foreach ($file in $dbFiles) {
        Write-Host "   Found: $($file.Name) ($($file.Length) bytes)" -ForegroundColor White
        if ($file.Name -like "*journal*") {
            Write-Host "   ⚠️  Journal file present - might indicate database lock" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "   No database files found" -ForegroundColor White
}

Write-Host ""
Write-Host "If POST is timing out:" -ForegroundColor Yellow
Write-Host "1. Stop the server process" -ForegroundColor White
Write-Host "2. Delete budget.db* files" -ForegroundColor White
Write-Host "3. Restart the server" -ForegroundColor White
