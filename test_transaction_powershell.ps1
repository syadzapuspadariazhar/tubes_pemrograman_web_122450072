# Test Transaction API Persistence
Write-Host "=== Testing Transaction Persistence ===" -ForegroundColor Yellow
Write-Host ""

# Check if database exists
$dbPath = "backend\budget.db"
if (Test-Path $dbPath) {
    Write-Host "✅ Database file found: $dbPath" -ForegroundColor Green
} else {
    Write-Host "❌ Database file not found: $dbPath" -ForegroundColor Red
}

# Check if server is running
try {
    $response = Invoke-WebRequest -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 5
    Write-Host "✅ Server is responding" -ForegroundColor Green
    
    # Test transaction creation
    Write-Host "Testing transaction creation..." -ForegroundColor Cyan
    
    $transactionData = @{
        deskripsi = "PowerShell Test Transaction"
        jumlah = 25000
        jenis = "pengeluaran"
        tanggal = "2025-06-02"
        kategori_id = 1
    } | ConvertTo-Json
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    try {
        $createResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/transactions" -Method POST -Body $transactionData -Headers $headers
        Write-Host "📝 Transaction Creation Response:" -ForegroundColor Cyan
        Write-Host ($createResponse | ConvertTo-Json) -ForegroundColor White
        
        $transactionId = $createResponse.id
        if ($transactionId) {
            Write-Host "✅ Transaction ID: $transactionId" -ForegroundColor Green
        } else {
            Write-Host "❌ Transaction ID is null!" -ForegroundColor Red
        }
        
        # Test getting transactions
        Start-Sleep -Seconds 1
        $getResponse = Invoke-RestMethod -Uri "http://localhost:6543/api/transactions" -Method GET
        Write-Host "📋 All Transactions:" -ForegroundColor Cyan
        Write-Host ($getResponse | ConvertTo-Json -Depth 3) -ForegroundColor White
        
        # Check if our transaction appears
        $ourTransaction = $getResponse | Where-Object { $_.deskripsi -eq "PowerShell Test Transaction" }
        if ($ourTransaction) {
            Write-Host "✅ Our transaction found in GET response" -ForegroundColor Green
        } else {
            Write-Host "❌ Our transaction NOT found in GET response" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "❌ Transaction creation failed: $($_.Exception.Message)" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Server not responding. Starting server..." -ForegroundColor Red
    
    # Try to start server
    Set-Location "backend"
    & ".\env\Scripts\Activate.ps1"
    Start-Process python -ArgumentList "start_server_fixed.py" -NoNewWindow
    
    Write-Host "Server starting... Please wait and try again." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Test completed." -ForegroundColor Yellow
