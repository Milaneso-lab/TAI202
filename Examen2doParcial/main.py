# --- IMPORTACIONES DE LIBRERIAS
import datetime
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal

app = FastAPI()
API_BASE_URL = "http://localhost:5000"

Citas_bd = []
Reserva_bd = []

class cita(BaseModel):
    id: int
    fecha_reserva: Literal["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"] = "Sin fecha de reserva"
    num_personas: int = Field(gt=1, le=10) 

class persona(BaseModel):
    nombre: str = Field(min_length=6, max_length=100)  

class reserva(BaseModel):
    id_cita: int
    usuario: persona

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Faltan datos o el formato es inválido.", "errores": exc.errors()},
    )


# --- ENDPOINTS

# CREAR CITA
@app.post("/citas", status_code=status.HTTP_201_CREATED)
def registrar_cita(cita : cita):
    # Validar si el ID ya existe
    if any(c["id"] == cita.id for c in Citas_bd):
         raise HTTPException(status_code=400, detail="El ID de la cita ya existe.")
    
    Citas_bd.append(cita.dict())
    return {"mensaje": "Cita registrada con éxito", "cita": cita}

# LISTAR CITAS
@app.get("/citas/existentes", response_model=List[cita])
def listar_citas():
    Citas_existentes = [cita for cita in Citas_bd]
    return Citas_existentes

# CONSULTAR POR ID DE CITA
@app.get("/citas/buscar/{id}")
def buscar_cita(id: int):
    resultados = [cita for cita in Citas_bd if id.lower in cita["id"].lower]
    if not resultados:
        raise HTTPException(status_code=404, detail="Cita no encontrada.")
    return resultados

# CONFIRMAR RESERVA
@app.post("/reservas")
def registrar_reserva(reserva : reserva):
    # Buscar reserva
    cita_index = next((index for (index, l) in enumerate(Citas_bd) if l["id"] == reserva.id_cita), None)
    
    if cita_index is None:
        raise HTTPException(status_code=400, detail="La reserva no existe.")

    # REGISTRA RESERVA
    Citas_bd[cita_index]
    Reserva_bd.append(reserva.dict())
    return {"mensaje": "Reserva registrada exitosamente."}

# CANCELAR RESERVA
@app.delete("/reservas/{id_cita}")
def eliminar_reserva(id_cita: int):
    cita_index = next((index for (index, r) in enumerate(Citas_bd) if r["id_cita"] == id_cita), None)
    
    if cita_index is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registro de reserva no encontrada.")
    
    Reserva_bd.pop(cita_index)
    return {"mensaje": "Reserva Cancelada."}

