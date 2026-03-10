# --- IMPORTACIONES DE LIBRERIAS
from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal

app = FastAPI()
API_BASE_URL = "http://localhost:5000"

Personas_bd = []
Citas_bd = []

class cita(BaseModel):
    id: int
    hora_reserva: datetime = Field(gt=datetime.now(hour=8, minute=0, second=0), le=datetime.now(hour=22, minute=0, second=0)) 
    num_personas: int = Field(min_length=1, max_length=10) 

class persona(BaseModel):
    nombre: str = Field(min_length=6, max_length=100)  



# --- ENDPOINTS

# CREAR CITA
@app.post("/citas", status_code=status.HTTP_201_CREATED)
def registrar_cita(cita: Citas):
    # Validar si el ID ya existe
    if any(c["id"] == cita.id for c in Citas_bd):
         raise HTTPException(status_code=400, detail="El ID de la cita ya existe.")
    
    Citas_bd.append(cita.dict())
    return {"mensaje": "Cita registrada con éxito", "cita": cita}

# LISTAR CITAS
@app.get("/citas/existentes", response_model=List[Citas])
def listar_citas():
    Citas_existentes = [cita for cita in Citas_bd]
    return Citas_existentes

# CONSULTAR POR ID DE CITA
@app.get("/citas/buscar/{id}")
def buscar_cita(id: int):
    resultados = [cita for cita in Citas_bd if id() in cita["id"]]
    if not resultados:
        raise HTTPException(status_code=404, detail="Cita no encontrado.")
    return resultados

