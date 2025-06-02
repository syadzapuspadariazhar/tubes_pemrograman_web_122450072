# Simple server test script
Write-Host "Checking server status..." -ForegroundColor Yellow

# Wait for server to initialize
Start-Sleep -Seconds 8

# Check if server is listening
try {
    $connection = Test-NetConnection -ComputerName localhost -Port 6543 -WarningAction SilentlyContinue
    if ($connection.TcpTestSucceeded) {
        Write-Host "✅ Server is running on port 6543" -ForegroundColor Green
        
        # Test the endpoints
        Write-Host "`nTesting GET /api/categories..." -ForegroundColor Cyan
        try {
            $getResponse = Invoke-WebRequest -Uri "http://localhost:6543/api/categories" -Method GET -UseBasicParsing
            Write-Host "✅ GET Status: $($getResponse.StatusCode)" -ForegroundColor Green
            Write-Host "Response: $($getResponse.Content)" -ForegroundColor White
        } catch {
            Write-Host "❌ GET Failed: $($_.Exception.Message)" -ForegroundColor Red
        }
        
        Write-Host "`nTesting POST /api/categories..." -ForegroundColor Cyan
        try {
            $body = '{"nama": "Test Category"}'
            $headers = @{"Content-Type" = "application/json"}
            $postResponse = Invoke-WebRequest -Uri "http://localhost:6543/api/categories" -Method POST -Body $body -Headers $headers -UseBasicParsing
            Write-Host "✅ POST Status: $($postResponse.StatusCode)" -ForegroundColor Green
            Write-Host "Response: $($postResponse.Content)" -ForegroundColor White
        } catch {
            Write-Host "❌ POST Failed: $($_.Exception.Message)" -ForegroundColor Red
            if ($_.Exception.Response) {
                Write-Host "Status: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
            }
        }
        
    } else {
        Write-Host "❌ Server is not responding on port 6543" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Error checking server: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`nTest complete. You can now use the web interface to test further." -ForegroundColor Yellow
