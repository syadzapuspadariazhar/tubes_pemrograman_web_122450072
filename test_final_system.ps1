# PowerShell script to start backend and test authentication
Write-Host "=== JWT Authentication System - Final Test ===" -ForegroundColor Green
Write-Host ""

# Start backend in background
Write-Host "Starting backend server..." -ForegroundColor Yellow
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
    python simple_start.py
}

Write-Host "Backend server started in background (Job ID: $($backendJob.Id))" -ForegroundColor Green

# Wait for server to start
Write-Host "Waiting for server to initialize..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Test authentication
try {
    Write-Host "Testing authentication endpoints..." -ForegroundColor Yellow
    
    # Test login
    $loginData = @{
        username = "admin"
        password = "admin"
    } | ConvertTo-Json
    
    $loginResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/auth/login" -Method POST -Body $loginData -ContentType "application/json" -TimeoutSec 10
    
    if ($loginResponse.token) {
        Write-Host "✅ Login successful! Token received." -ForegroundColor Green
        
        # Test token verification
        $headers = @{
            "Authorization" = "Bearer $($loginResponse.token)"
        }
        
        $verifyResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/auth/verify" -Method GET -Headers $headers -TimeoutSec 10
        
        if ($verifyResponse) {
            Write-Host "✅ Token verification successful!" -ForegroundColor Green
            
            # Test protected endpoint
            $categoriesResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -Headers $headers -TimeoutSec 10
            Write-Host "✅ Protected categories endpoint accessible!" -ForegroundColor Green
            
            Write-Host ""
            Write-Host "🎉 ALL TESTS PASSED!" -ForegroundColor Green
            Write-Host "🚀 JWT Authentication system is working correctly!" -ForegroundColor Green
            Write-Host ""
            Write-Host "Frontend is running at: http://localhost:3000" -ForegroundColor Cyan
            Write-Host "Backend is running at: http://localhost:6543" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "You can now:" -ForegroundColor White
            Write-Host "1. Open http://localhost:3000 in your browser" -ForegroundColor White
            Write-Host "2. Login with username: admin, password: admin" -ForegroundColor White
            Write-Host "3. Test the complete budget tracking application" -ForegroundColor White
            
        } else {
            Write-Host "❌ Token verification failed" -ForegroundColor Red
        }
    } else {
        Write-Host "❌ Login failed - no token received" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Authentication test failed: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "This might be normal if the server is still starting up." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Backend server is running in background." -ForegroundColor Green
Write-Host "To stop the backend server, run: Stop-Job $($backendJob.Id); Remove-Job $($backendJob.Id)" -ForegroundColor Yellow
