# Cómo ejecutar la API FastAPI

## Requisitos previos
- Python 3.12+ instalado
- Entorno virtual creado (ya está creado en `venv/`)

## Pasos para ejecutar la API

### Opción 1: Usando PowerShell (Recomendado)
```powershell
# 1. Navegar a la carpeta MyAPI
cd MyAPI

# 2. Activar el entorno virtual
.\venv\Scripts\Activate.ps1

# 3. Ir al directorio app
cd app

# 4. Ejecutar uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

### Opción 2: Usando el script PowerShell
```powershell
cd MyAPI
.\start_api.ps1
```

### Opción 3: Usando el script Batch (CMD)
```cmd
cd MyAPI
start_api.bat
```

### Opción 4: Usando Python directamente
```powershell
cd MyAPI
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 5000
```

## Verificar que funciona
Una vez iniciado, abre tu navegador en:
- **API**: http://localhost:5000
- **Documentación interactiva**: http://localhost:5000/docs
- **Documentación alternativa**: http://localhost:5000/redoc

## Solución de problemas

### Error: "No se puede ejecutar el script porque la ejecución de scripts está deshabilitada"
Ejecuta en PowerShell como administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "uvicorn no se reconoce como comando"
Asegúrate de que el entorno virtual esté activado y las dependencias instaladas:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Error: "No se encuentra el archivo especificado"
Asegúrate de estar en el directorio correcto (`MyAPI`) antes de ejecutar los comandos.
