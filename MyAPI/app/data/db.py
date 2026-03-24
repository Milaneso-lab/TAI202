from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker, declarative_base 
import os 

#1. Definimos la URL de conexión 
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://admin:123456@postgres:5432/DB_miapi"
)

#2. Creamos el motor de la conexión
engine = create_engine(DATABASE_URL)

#3. Preparamos el gestionador de sessiones
SessionLocal = sessionmaker(
    autocommit = False, 
    autoflush = False, 
    bind = engine
)

#4. Definimos la base declarativa para los modelos 
Base = declarative_base()

#5. Obtener las sesiones de cada petición 
def get_db(): 
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close ()