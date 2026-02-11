#IMPORTACIONES 
from fastapi import FastAPI
import asyncio

#INSTANCIA DEL SERVIDOR
app = FastAPI()

#ENDPOINTS
@app.get("/")
async def holamundo(): 
    return {"mensaje" : "Hola Mundo FastAPI"}

@app.get("/bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje" : "Bienvenido a Fast API",
        "estatus" : "200"
    }


# /docs <- programador - documentación
# /redoc <- usuarioFinal - documentación

# Endpoint con parámetro obligatorio
@app.get("/saludo/{nombre}")
async def saludo(nombre: str):
    return {"mensaje": f"Hola, {nombre}"}

# Endpoint con parámetros opcionales 
@app.get("/perfil")
async def perfil(nombre: str = "Invitado", ciudad: str = "No especificada"):
    return {
        "nombre": nombre,
        "ciudad": ciudad,
        "mensaje": f"{nombre} está en {ciudad}"
    }



