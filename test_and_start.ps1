# Test indentation fix and start server
Write-Host "=== Testing Indentation Fix ===" -ForegroundColor Yellow

Set-Location backend

Write-Host "Testing Python syntax..." -ForegroundColor Cyan
$syntaxTest = python -m py_compile "app/__init__.py" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Syntax check passed" -ForegroundColor Green
} else {
    Write-Host "❌ Syntax error: $syntaxTest" -ForegroundColor Red
    exit 1
}

Write-Host "Testing app import..." -ForegroundColor Cyan
$importTest = python -c "from app import main; print('Import successful')" 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Import successful: $importTest" -ForegroundColor Green
} else {
    Write-Host "❌ Import failed: $importTest" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 INDENTATION ERROR FIXED!" -ForegroundColor Green
Write-Host "Starting server..." -ForegroundColor Yellow

# Start server
python simple_start.py
