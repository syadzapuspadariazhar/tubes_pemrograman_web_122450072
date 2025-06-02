# Test the backend server endpoints
Write-Host "Testing POST /api/categories..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" `
        -Method POST `
        -ContentType "application/json" `
        -Body '{"nama": "Test Category"}'
    
    Write-Host "✅ SUCCESS: POST request worked!" -ForegroundColor Green
    Write-Host "Response: $($response | ConvertTo-Json)" -ForegroundColor Green
    
} catch {
    Write-Host "❌ POST failed: $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        $statusCode = $_.Exception.Response.StatusCode
        Write-Host "Status Code: $statusCode" -ForegroundColor Red
        
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $responseBody = $reader.ReadToEnd()
            Write-Host "Response Body: $responseBody" -ForegroundColor Red
        } catch {
            Write-Host "Could not read response body" -ForegroundColor Red
        }
    }
}

Write-Host ""
Write-Host "Testing GET /api/categories..." -ForegroundColor Yellow

try {
    $response = Invoke-RestMethod -Uri "http://localhost:6543/api/categories" -Method GET
    Write-Host "✅ SUCCESS: GET request worked!" -ForegroundColor Green
    Write-Host "Categories: $($response | ConvertTo-Json)" -ForegroundColor Green
    
} catch {
    Write-Host "❌ GET failed: $($_.Exception.Message)" -ForegroundColor Red
}
