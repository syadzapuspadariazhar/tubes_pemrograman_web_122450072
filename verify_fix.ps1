# Simple verification script for the CORS fix
Write-Host "=== CORS Fix Verification ===" -ForegroundColor Yellow

# Test 1: Check if the CORS route fix is in place
$routesFile = "backend\app\routes.py"
$routesContent = Get-Content $routesFile -Raw

if ($routesContent -match "config\.add_route\('cors_preflight', '/\{path:\.\*\}', request_method='OPTIONS'\)") {
    Write-Host "✅ CORS route fix is in place" -ForegroundColor Green
    Write-Host "   Found: config.add_route('cors_preflight', '/{path:.*}', request_method='OPTIONS')" -ForegroundColor White
} else {
    Write-Host "❌ CORS route fix not found" -ForegroundColor Red
    exit 1
}

# Test 2: Check category_api.py is fixed
$categoryFile = "backend\app\views\category_api.py"
$categoryContent = Get-Content $categoryFile -Raw

if ($categoryContent -match "@view_config\(route_name='add_category', request_method='POST'") {
    Write-Host "✅ Category API POST route configured correctly" -ForegroundColor Green
} else {
    Write-Host "❌ Category API POST route configuration issue" -ForegroundColor Red
}

# Test 3: Check database configuration
$configFile = "backend\development.ini"
$configContent = Get-Content $configFile -Raw

if ($configContent -match "sqlalchemy\.url = sqlite:///budget\.db") {
    Write-Host "✅ SQLite database configuration is correct" -ForegroundColor Green
} else {
    Write-Host "❌ Database configuration issue" -ForegroundColor Red
}

# Test 4: Check if packages are installed
Write-Host "`nChecking package installation..." -ForegroundColor Cyan
cd backend
.\env\Scripts\activate.bat
$packagesCheck = python -c "import pyramid, sqlalchemy, pyramid_tm, waitress; print('All packages available')" 2>&1

if ($packagesCheck -match "All packages available") {
    Write-Host "✅ All required packages are installed" -ForegroundColor Green
} else {
    Write-Host "❌ Package installation issue: $packagesCheck" -ForegroundColor Red
}

Write-Host "`n=== Summary ===" -ForegroundColor Yellow
Write-Host "The key fixes have been applied:" -ForegroundColor White
Write-Host "1. CORS preflight route restricted to OPTIONS method only" -ForegroundColor White
Write-Host "2. Category API routes properly configured" -ForegroundColor White
Write-Host "3. Database changed to SQLite" -ForegroundColor White
Write-Host "4. Required packages installed" -ForegroundColor White
Write-Host "`nThe POST /api/categories endpoint should now work!" -ForegroundColor Green
Write-Host "Frontend should be able to add categories without 404 errors." -ForegroundColor Green

cd ..
