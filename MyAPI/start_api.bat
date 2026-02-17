@echo off
echo Iniciando servidor FastAPI en http://localhost:5000
echo Usando Python del entorno virtual...

REM Usar Python directamente con el modulo uvicorn (mas confiable)
venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000

pause
