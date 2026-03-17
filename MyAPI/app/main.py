#importaciones
from fastapi import FastAPI
from app.router import usuario, tiendita


#Instancia del servidor
app = FastAPI(
    title= "Mi primer API",
    description= "Flores Madriz José Antonio",
    version="1.0"
)

app.include_router(usuario.router)
app.include_router(tiendita.tiendita)
