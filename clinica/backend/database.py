from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

# Configuración de la base de datos
DB_USER = "postgres"
DB_PASSWORD = "admin"  # Tu contraseña
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "clinica_db"

# Codificar la contraseña para evitar problemas con caracteres especiales
password_encoded = quote_plus(DB_PASSWORD)

# Construir URL de conexión
SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{password_encoded}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Crear engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
    connect_args={"client_encoding": "utf8"}  # Forzar UTF-8
)

# Crear SessionLocal
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

# Dependency para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()