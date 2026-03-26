from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

#1. Definimos la URL de conexión
DATABASE_URL= os.getenv(
    "DATABASE_URL",
    "sqlite:///./db_miapi.sqlite3"
)

#2. Creamos el motor de la conexión
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    # SQLite necesita este argumento en apps con múltiples hilos.
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

#3. Preparamos el gestionador de sesiones
SessionLocal= sessionmaker(
    autocommit= False,
    autoflush= False,
    bind= engine
)

#4. Base declarativa del modelo
Base= declarative_base()

#5. Obtener sesiones de cada petición
def get_db():
    db= SessionLocal()
    try:
        yield db #imprimir o mandar lo que tiene db en ese momento
    finally:
        db.close()