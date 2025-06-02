# Run both backend and frontend servers
Write-Host "Starting both backend and frontend servers..." -ForegroundColor Green

# Start backend in a new PowerShell window
$backendCommand = @"
cd '$PSScriptRoot\backend'
.\env\Scripts\Activate.ps1
Write-Host 'Checking PostgreSQL connection...' -ForegroundColor Cyan
try {
    python -c "import psycopg2; conn=psycopg2.connect('dbname=budget_db user=postgres password=matchalatte host=localhost'); print('Database connection successful!')"
    Write-Host 'PostgreSQL connection successful!' -ForegroundColor Green
} catch {
    Write-Host 'PostgreSQL connection failed! Please check your database settings.' -ForegroundColor Red
    Write-Host 'Press any key to exit...'
    [Console]::ReadKey() | Out-Null
    exit 1
}
Write-Host 'Starting Pyramid server...' -ForegroundColor Cyan
python -c "from pyramid.paster import get_app; from waitress import serve; app = get_app('development.ini', 'main'); print('Backend server running at: http://localhost:6543'); serve(app, host='0.0.0.0', port=6543)"
"@

Start-Process powershell -ArgumentList "-NoExit -Command $backendCommand"

# Give backend a moment to start
Write-Host "Waiting for backend to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Test if backend is running
$maxRetries = 5
$retryCount = 0
$backendRunning = $false

while (-not $backendRunning -and $retryCount -lt $maxRetries) {
    try {
        $result = Test-NetConnection -ComputerName localhost -Port 6543 -ErrorAction SilentlyContinue
        if ($result.TcpTestSucceeded) {
            $backendRunning = $true
            Write-Host "Backend is running!" -ForegroundColor Green
        } else {
            Write-Host "Backend not responding yet. Retrying..." -ForegroundColor Yellow
            Start-Sleep -Seconds 2
            $retryCount++
        }
    } catch {
        Write-Host "Error checking backend: $_" -ForegroundColor Red
        Start-Sleep -Seconds 2
        $retryCount++
    }
}

if (-not $backendRunning) {
    Write-Host "Warning: Backend might not be running properly. Starting frontend anyway..." -ForegroundColor Yellow
} else {
    Write-Host "Backend available at http://localhost:6543" -ForegroundColor Green
}

# Start frontend in this window
Write-Host "Starting frontend..." -ForegroundColor Green
cd "$PSScriptRoot\frontend"
npm start
