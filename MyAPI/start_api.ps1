# Script para iniciar la API FastAPI
Write-Host "Iniciando servidor FastAPI en http://localhost:5000" -ForegroundColor Cyan
Write-Host "Usando Python del entorno virtual..." -ForegroundColor Green

# Usar Python directamente con el módulo uvicorn (más confiable)
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
