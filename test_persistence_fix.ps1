# PowerShell script to test persistence fix
Write-Host "=== Testing Persistence Fix ===" -ForegroundColor Yellow

# Navigate to project directory
Set-Location "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"

# Start server in background
Write-Host "Starting backend server..." -ForegroundColor Green
$serverJob = Start-Job -ScriptBlock {
    Set-Location "c:\Users\DELL\OneDrive\Documents\Puspa\Kuliah\Semester 6\Pemweb\UAS_Pemweb_122450072\backend"
    & ".\env\Scripts\activate.bat"
    python -m waitress --port=6543 --call app:main
}

# Wait for server to start
Write-Host "Waiting for server to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

try {
    # Test GET
    Write-Host "`n1. Testing GET /api/categories..." -ForegroundColor Cyan
    try {
        $initialCategories = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 10
        Write-Host "Initial categories: $($initialCategories.Count)" -ForegroundColor Green
        Write-Host $initialCategories | Out-String
    } catch {
        Write-Host "Failed to GET categories: $_" -ForegroundColor Red
        throw
    }

    # Test POST
    Write-Host "`n2. Testing POST /api/categories..." -ForegroundColor Cyan
    $testName = "Test Category $(Get-Date -Format 'HHmmss')"
    $body = @{ nama = $testName } | ConvertTo-Json
    $headers = @{ "Content-Type" = "application/json" }
    
    try {
        $postResult = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method POST -Body $body -Headers $headers -TimeoutSec 10
        Write-Host "POST successful: $($postResult.message)" -ForegroundColor Green
        Write-Host "Created category ID: $($postResult.id)" -ForegroundColor Green
    } catch {
        Write-Host "Failed to POST category: $_" -ForegroundColor Red
        throw
    }

    # Test GET again
    Write-Host "`n3. Testing GET after POST..." -ForegroundColor Cyan
    Start-Sleep -Seconds 1
    try {
        $afterCategories = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET -TimeoutSec 10
        Write-Host "Categories after POST: $($afterCategories.Count)" -ForegroundColor Green
        Write-Host $afterCategories | Out-String
        
        # Check if our category is there
        $found = $afterCategories | Where-Object { $_.nama -eq $testName }
        if ($found) {
            Write-Host "`n✅ SUCCESS: Category persisted and visible!" -ForegroundColor Green
            Write-Host "Found our test category: $($found.nama) (ID: $($found.id))" -ForegroundColor Green
        } else {
            Write-Host "`n❌ PERSISTENCE ISSUE: Category not found in GET response" -ForegroundColor Red
        }
        
    } catch {
        Write-Host "Failed to GET categories after POST: $_" -ForegroundColor Red
        throw
    }

} catch {
    Write-Host "`nTest failed: $_" -ForegroundColor Red
} finally {
    # Clean up
    Write-Host "`nStopping server..." -ForegroundColor Yellow
    Stop-Job $serverJob -Force
    Remove-Job $serverJob -Force
}

Write-Host "`nTest completed. Press any key to exit..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
