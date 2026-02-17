#IMPORTACIONES 
from fastapi import FastAPI,status,HTTPException
import asyncio
from typing import Optional


#INSTANCIA DEL SERVIDOR
app = FastAPI(
    title ="Mi primer API",
    description = "Jose Antonio Flores Madriz",
    version="1.0"
)

#TB ficticia
USUARIO = [
    {"id":1, "nombre":"Fany", "edad": 21},
    {"id":2, "nombre":"Aly", "edad": 21},
    {"id":3, "nombre":"Dulce", "edad": 21},
]

#ENDPOINTS
#classroom
@app.get("/")
async def holamundo():
    return {"mensaje" : "Hola Mundo FastAPI"}

@app.get("bienvenido")
async def bienvenido():
    await asyncio.sleep(5)
    return {
        "mensaje":"Bienvenido a FastAPI",
        "estatus":"200",
    }

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultauno(id:int):
    return {"mensaje":"Usuario encontrado",
            "Usuario":id, 
            "status":"200"}

@app.get(f"/v1/parametroOp/", tags=['Parametro Opcional'])
async def consultados(id:Optional[int]=None):
        if id is not None:
            for usuarioK in USUARIO:
                if usuarioK["id"] == id:
                    return{"mensaje":"Usuario encontrado", "usuario":usuarioK}
            return{"mensaje":"Usuario no encontrado","status":"200"}
        else:
            return{"mensaje":"No se proporciono id","status":"200"}


#clase 
@app.get("/v1/usuarios/", tags=['HTTP CRUD'])
async def leer_usuarios():
    return{
        "total":len(USUARIO),
        "usuarios":USUARIO,
        "estatus": "200"
    }

@app.post("/v1/usuarios/", tags=['HTTP CRUD'])
async def agregar_usuarios(usuario:dict):
    for usr in USUARIO:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El usuario ya existe"
            )
    USUARIO.append(usuario)
    return{
        "mensaje":"Usuario Agregado Correctamente",
        "Datos Nuevos": usuario
    }

#TAREA DE COMPLETAR LOS METODOS HTTP
@app.put("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_completo(id:int, usuario:dict):
    for i, usr in enumerate(USUARIO):
        if usr["id"] == id:
            usuario["id"] = id  
            USUARIO[i] = usuario
            return{
                "mensaje":"Usuario actualizado completamente",
                "Usuario Actualizado": usuario,
                "estatus": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.patch("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def actualizar_usuario_parcial(id:int, usuario:dict):
    for i, usr in enumerate(USUARIO):
        if usr["id"] == id:
            for key, value in usuario.items():
                if key != "id":  
                    USUARIO[i][key] = value
            return{
                "mensaje":"Usuario actualizado parcialmente",
                "Usuario Actualizado": USUARIO[i],
                "estatus": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

@app.delete("/v1/usuarios/{id}", tags=['HTTP CRUD'])
async def eliminar_usuario(id:int):
    for i, usr in enumerate(USUARIO):
        if usr["id"] == id:
            usuario_eliminado = USUARIO.pop(i)
            return{
                "mensaje":"Usuario eliminado correctamente",
                "Usuario Eliminado": usuario_eliminado,
                "estatus": "200"
            }
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )
