from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal

# --- CREAMOS NUESTRA API PARA LA ACTIVIDAD
app = FastAPI(title="API-Biblioteca Digital")

# --- SIMULACIÓN DE BASE DE DATOS POR MEDIO DE UN ARREGLO 
libros_db = []
prestamos_db = []

# --- MODELOS PYDANTIC VALIDACIONES 

# --- VALIDACIONES PARA EL LIBRE (PRESENTADAS EN EL DOCUMENTO)
class Libro(BaseModel):
    id: int
    # Longitud mínima y máxima (entre 2 y 100)
    nombre: str = Field(min_length=2, max_length=100) 
    # Mayor a 1450 y menor o igual al año actual
    anio: int = Field(gt=1450, le=2026) 
    # Entero positivo mayor a 1
    paginas: int = Field(gt=1) 
    # Estado del libro
    estado: Literal["disponible", "prestado"] = "disponible" 

# --- VALIDACIONES PARA LOS USUARIOS (ATENCIÓN EN EL FORMATO DEL CORREO) 
class Usuario(BaseModel):
    nombre: str
    correo: EmailStr # Valida que sea un correo válido

# --- VALIDACIONES PARA LOS PRESTAMOS REGISTRADOS POR USUARIOS
class Prestamo(BaseModel):
    id_libro: int
    usuario: Usuario

# --- MANEJO DE ERRORES PERSONALIZADO 
# 1. error 400 si faltan datos o el nombre no es válido
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Faltan datos o el formato es inválido.", "errores": exc.errors()},
    )

# --- ENDPOINTS 
# a. Registrar un libro
# - se implementa la validación Num. 201
@app.post("/libros", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    # Validar si el ID ya existe
    if any(l["id"] == libro.id for l in libros_db):
         raise HTTPException(status_code=400, detail="El ID del libro ya existe.")
    
    libros_db.append(libro.dict())
    return {"mensaje": "Libro registrado con éxito", "libro": libro}

# b. Listar todos los libros disponibles
@app.get("/libros/disponibles", response_model=List[Libro])
def listar_libros_disponibles():
    disponibles = [libro for libro in libros_db if libro["estado"] == "disponible"]
    return disponibles

# c. Buscar un libro por su nombre
@app.get("/libros/buscar/{nombre}")
def buscar_libro(nombre: str):
    resultados = [libro for libro in libros_db if nombre.lower() in libro["nombre"].lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="Libro no encontrado.")
    return resultados

# d. Registrar el préstamo de un libro a un usuario
@app.post("/prestamos")
def registrar_prestamo(prestamo: Prestamo):
    # Buscar el libro
    libro_index = next((index for (index, l) in enumerate(libros_db) if l["id"] == prestamo.id_libro), None)
    
    if libro_index is None:
        raise HTTPException(status_code=400, detail="El libro no existe.")
    
    if libros_db[libro_index]["estado"] == "prestado":
        # validación con el código 409 si el libro ya está prestado
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro ya está prestado.")
    
    # Actualizar estado y registrar préstamo
    libros_db[libro_index]["estado"] = "prestado"
    prestamos_db.append(prestamo.dict())
    return {"mensaje": "Préstamo registrado exitosamente."}

# e. Marcar un libro como devuelto
# validación con el código 200 al devolver un libro
@app.post("/devoluciones/{id_libro}", status_code=status.HTTP_200_OK)
def devolver_libro(id_libro: int):
    # Buscar el libro
    libro_index = next((index for (index, l) in enumerate(libros_db) if l["id"] == id_libro), None)
    
    if libro_index is None:
        raise HTTPException(status_code=400, detail="El libro no existe.")
    
    if libros_db[libro_index]["estado"] == "disponible":
        # validación - 409 si el registro de préstamo ya no existe
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El libro no está prestado actualmente.")
    
    # Actualizar estado
    libros_db[libro_index]["estado"] = "disponible"
    return {"mensaje": "Libro devuelto con éxito."}

# f. Eliminar el registro de un préstamo
@app.delete("/prestamos/{id_libro}")
def eliminar_prestamo(id_libro: int):
    prestamo_index = next((index for (index, p) in enumerate(prestamos_db) if p["id_libro"] == id_libro), None)
    
    if prestamo_index is None:
        # validación - 409 para recordar que el prestamo del libro dejo de existir
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Registro de préstamo no encontrado.")
    
    prestamos_db.pop(prestamo_index)
    return {"mensaje": "Registro de préstamo eliminado."}