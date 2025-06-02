# Test script to verify the CORS route fix
Write-Host "=== Testing POST /api/categories Fix ===" -ForegroundColor Yellow

# Kill any existing servers
Write-Host "Stopping any existing servers..." -ForegroundColor Cyan
Stop-Process -Name "*pserve*", "*python*" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 3

# Start server
Write-Host "Starting server..." -ForegroundColor Cyan
$serverJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
    & .\env\Scripts\Activate.ps1
    pserve development.ini
}

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Cyan
$maxWait = 15
$waited = 0
$serverReady = $false

while ($waited -lt $maxWait -and -not $serverReady) {
    Start-Sleep -Seconds 1
    $waited++
    $connection = Get-NetTCPConnection -LocalPort 6543 -State Listen -ErrorAction SilentlyContinue
    if ($connection) {
        $serverReady = $true
        Write-Host "✅ Server is ready on port 6543" -ForegroundColor Green
    } else {
        Write-Host "." -NoNewline -ForegroundColor Yellow
    }
}

if (-not $serverReady) {
    Write-Host "`n❌ Server failed to start within $maxWait seconds" -ForegroundColor Red
    $jobOutput = Receive-Job $serverJob.Id
    Write-Host "Server output: $jobOutput" -ForegroundColor Red
    Stop-Job $serverJob.Id
    exit 1
}

# Test endpoints
Write-Host "`nTesting endpoints..." -ForegroundColor Cyan

# Test GET categories (should work)
try {
    $getResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 10
    Write-Host "✅ GET /api/categories: SUCCESS" -ForegroundColor Green
    Write-Host "   Categories count: $($getResponse.Count)" -ForegroundColor White
} catch {
    Write-Host "❌ GET /api/categories: FAILED - $($_.Exception.Message)" -ForegroundColor Red
}

# Test POST categories (this should now work)
try {
    $postData = @{ nama = "Test Category - $(Get-Date -Format 'HH:mm:ss')" }
    $postBody = $postData | ConvertTo-Json
    $headers = @{ 
        "Content-Type" = "application/json"
        "Accept" = "application/json"
    }
    
    Write-Host "`nSending POST request with data: $postBody" -ForegroundColor White
    $postResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -Body $postBody -Headers $headers -TimeoutSec 10
    
    Write-Host "✅ POST /api/categories: SUCCESS!" -ForegroundColor Green
    Write-Host "   Response: $($postResponse | ConvertTo-Json -Compress)" -ForegroundColor White
    Write-Host "`n🎉 FIX SUCCESSFUL! Frontend should now be able to add categories." -ForegroundColor Green
    
} catch {
    Write-Host "❌ POST /api/categories: FAILED" -ForegroundColor Red
    Write-Host "   Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
    Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    
    # Try to get response body for more details
    try {
        $responseStream = $_.Exception.Response.GetResponseStream()
        $reader = New-Object System.IO.StreamReader($responseStream)
        $responseBody = $reader.ReadToEnd()
        Write-Host "   Response Body: $responseBody" -ForegroundColor Red
    } catch {
        Write-Host "   Could not read response body" -ForegroundColor Yellow
    }
}

# Test CORS preflight (OPTIONS request)
try {
    $corsResponse = Invoke-WebRequest -Uri "http://localhost:6543/api/categories" -Method OPTIONS -UseBasicParsing -TimeoutSec 5
    Write-Host "`n✅ OPTIONS /api/categories: SUCCESS (Status: $($corsResponse.StatusCode))" -ForegroundColor Green
    $corsHeaders = $corsResponse.Headers
    if ($corsHeaders["Access-Control-Allow-Origin"]) {
        Write-Host "   CORS Origin: $($corsHeaders['Access-Control-Allow-Origin'])" -ForegroundColor White
    }
    if ($corsHeaders["Access-Control-Allow-Methods"]) {
        Write-Host "   CORS Methods: $($corsHeaders['Access-Control-Allow-Methods'])" -ForegroundColor White
    }
} catch {
    Write-Host "`n⚠️  OPTIONS /api/categories: $($_.Exception.Message)" -ForegroundColor Yellow
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Yellow
Write-Host "Server Job ID: $($serverJob.Id)" -ForegroundColor Cyan
Write-Host "To stop server: Stop-Job $($serverJob.Id)" -ForegroundColor Cyan
Write-Host "Server will continue running for frontend testing..." -ForegroundColor Cyan
