# UNIO Backend Quick Start Script for Windows PowerShell

Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "UNIO Backend Setup Script" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "Checking Python installation..." -ForegroundColor Yellow
python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if (-not (Test-Path ".env")) {
    Write-Host ""
    Write-Host "Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "Please update .env file with your OAuth credentials" -ForegroundColor Green
}

# Run migrations
Write-Host ""
Write-Host "Running database migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

# Create superuser prompt
Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Create Admin User" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
$createSuperuser = Read-Host "Do you want to create a superuser now? (y/n)"
if ($createSuperuser -eq "y" -or $createSuperuser -eq "Y") {
    python manage.py createsuperuser
}

# Collect static files
Write-Host ""
Write-Host "Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "To start the development server, run:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "For WebSocket support (recommended), run:" -ForegroundColor Yellow
Write-Host "  daphne -b 0.0.0.0 -p 8000 unio_backend.asgi:application" -ForegroundColor White
Write-Host ""
Write-Host "Access the admin panel at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/admin" -ForegroundColor White
Write-Host ""
Write-Host "API documentation at:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/api/" -ForegroundColor White
Write-Host ""
