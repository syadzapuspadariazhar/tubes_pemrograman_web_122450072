# Test script to verify server is running and endpoints work
Write-Host "=== Testing Backend Server ===" -ForegroundColor Yellow

# Wait a bit for server to start
Start-Sleep -Seconds 2

# Check if port 6543 is listening
Write-Host "Checking if server is listening on port 6543..." -ForegroundColor Cyan
$listening = Get-NetTCPConnection -LocalPort 6543 -State Listen -ErrorAction SilentlyContinue

if ($listening) {
    Write-Host "✅ Server is listening on port 6543" -ForegroundColor Green
    
    # Test GET categories
    Write-Host "`nTesting GET /api/categories..." -ForegroundColor Cyan
    try {
        $getResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 10
        Write-Host "✅ GET /api/categories: SUCCESS" -ForegroundColor Green
        Write-Host "   Response: $($getResponse | ConvertTo-Json -Compress)" -ForegroundColor White
    } catch {
        Write-Host "❌ GET /api/categories: FAILED" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
    }
    
    # Test POST categories
    Write-Host "`nTesting POST /api/categories..." -ForegroundColor Cyan
    try {
        $postData = @{ nama = "Test Category from Script" }
        $postBody = $postData | ConvertTo-Json
        $headers = @{ "Content-Type" = "application/json" }
        
        $postResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -Body $postBody -Headers $headers -TimeoutSec 10
        Write-Host "✅ POST /api/categories: SUCCESS" -ForegroundColor Green
        Write-Host "   Response: $($postResponse | ConvertTo-Json -Compress)" -ForegroundColor White
        
        # If successful, this should fix the frontend issue
        Write-Host "`n🎉 SUCCESS! The frontend should now be able to add categories." -ForegroundColor Green
        
    } catch {
        Write-Host "❌ POST /api/categories: FAILED" -ForegroundColor Red
        Write-Host "   Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        Write-Host "   Error: $($_.Exception.Message)" -ForegroundColor Red
        
        # Get more details about the error
        if ($_.Exception.Response) {
            $responseStream = $_.Exception.Response.GetResponseStream()
            $reader = New-Object System.IO.StreamReader($responseStream)
            $responseBody = $reader.ReadToEnd()
            Write-Host "   Response Body: $responseBody" -ForegroundColor Red
        }
    }
    
} else {
    Write-Host "❌ Server is NOT listening on port 6543" -ForegroundColor Red
    Write-Host "   Make sure the server is running first" -ForegroundColor Yellow
    
    # Check if any Python processes are running
    $pythonProcesses = Get-Process -Name "*python*" -ErrorAction SilentlyContinue
    if ($pythonProcesses) {
        Write-Host "   Found Python processes:" -ForegroundColor Yellow
        $pythonProcesses | ForEach-Object { Write-Host "     PID: $($_.Id), Name: $($_.ProcessName)" -ForegroundColor White }
    } else {
        Write-Host "   No Python processes found" -ForegroundColor Yellow
    }
}

Write-Host "`n=== Test Complete ===" -ForegroundColor Yellow
