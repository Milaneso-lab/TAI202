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

