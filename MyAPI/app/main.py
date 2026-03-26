#importaciones
from fastapi import FastAPI
from app.router import usuario


#Instancia del servidor
app = FastAPI(
    title= "Mi primer API",
    description= "Antonio Madriz",
    version="1.0"
)

app.include_router(usuario.router)