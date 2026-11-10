import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Leer la configuración desde el archivo .env
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", "3306"))
db_name = os.getenv("DB_NAME")

# Crear la conexión solamente si existe la configuración
engine = None
SessionLocal = None

if db_user and db_password and db_name:
    database_url = URL.create(
        drivername="mysql+pymysql",
        username=db_user,
        password=db_password,
        host=db_host,
        port=db_port,
        database=db_name
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        echo=False
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "La conexión a la base de datos no está configurada."
        )

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()