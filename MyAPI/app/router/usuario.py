from fastapi import APIRouter, status, HTTPException, Depends
from app.models.usuario import crear_usuario
from app.data.database import usuarios
from app.security.auth import verificar_peticion

router = APIRouter(
    prefix="/v1/usuarios",
    tags=["HTTP CRUD"]
)

# USUARIO CRED
# GET: Lee los usuarios mostrados en la lista en memoria
@router.get("/")
async def leer_usuarios():
    return {
        "total": len(usuarios),
        "usuarios": usuarios,
        "status": "200"
    }

# GET por ID: Obtiene un usuario de la lista en memoria
@router.get("/{id}", status_code=status.HTTP_200_OK)
async def leer_usuario_por_id(id: int):
    for usr in usuarios:
        if usr["id"] == id:
            return {
                "usuario": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )

# POST: Crea usuario en la lista verificando que no exista el ID
@router.post("/", status_code=status.HTTP_201_CREATED)
async def crear_usuario_endpoint(usuarioP: crear_usuario):
    for usr in usuarios:
        if usr["id"] == usuarioP.id:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese id"
            )

    nuevo = {
        "id": usuarioP.id,
        "nombre": usuarioP.nombre,
        "edad": usuarioP.edad,
    }
    usuarios.append(nuevo)

    return {
        "mensaje": "Usuario Agregado",
        "Usuario": nuevo
    }

# PUT: Actualizar un usuario completo (Reemplaza todos los datos)
@router.put("/{id}")
async def actualizar_usuario(id: int, usuario_actualizado: dict):
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            # Nos aseguramos que el ID del objeto coincida con el de la URL
            usuario_actualizado["id"] = id
            # Reemplazamos el objeto completo en la lista
            usuarios[index] = usuario_actualizado
            return {
                "mensaje": "Usuario actualizado correctamente",
                "datos_anteriores": usr,
                "datos_nuevos": usuario_actualizado,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado para actualizar"
    )

# PATCH: Actualización parcial (Solo modifica los campos enviados)
@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def actualizar_parcial_usuario(id: int, usuario_parcial: dict):
    for usr in usuarios:
        if usr["id"] == id:
            # El método .update() de python actualiza solo las llaves que vienen en el dict
            usr.update(usuario_parcial)
            # Aseguramos que el ID no cambie aunque lo envíen en el body
            usr["id"] = id
            return {
                "mensaje": "Usuario modificado parcialmente",
                "datos_nuevos": usr,
                "status": "200"
            }
            
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado para modificar"
    )

# DELETE: Eliminar un usuario
@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id: int, usuarioAuth: str = Depends(verificar_peticion)):
    for usr in usuarios:
        if usr["id"] == id:
            usuarios.remove(usr)
            return {
                "mensaje": "Usuario eliminado exitosamente",
                "usuario_eliminado": usr,
                "status": "200"
            }

    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado para eliminar"
    )