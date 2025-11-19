import os
from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Ruta de archivos
ARCHIVOS_BASE_PATH = BASE_DIR / "clinica-archivos"
ARCHIVOS_PACIENTES_PATH = ARCHIVOS_BASE_PATH / "pacientes"

# Crear directorios si no existen
def crear_directorios():
    """Crear estructura de directorios para archivos"""
    directorios = [
        ARCHIVOS_PACIENTES_PATH / "fotos",
        ARCHIVOS_PACIENTES_PATH / "laboratorios",
        ARCHIVOS_PACIENTES_PATH / "imagenes",
        ARCHIVOS_PACIENTES_PATH / "recetas",
        ARCHIVOS_PACIENTES_PATH / "ekg",
        ARCHIVOS_PACIENTES_PATH / "videos",
    ]
    
    for directorio in directorios:
        directorio.mkdir(parents=True, exist_ok=True)
    
    print(f"✅ Directorios creados en: {ARCHIVOS_BASE_PATH}")

# Ejecutar al importar
crear_directorios()

# Configuración de base de datos
DATABASE_URL = "postgresql://postgres:tu_contraseña@localhost:5432/clinica_db"

# Configuración de JWT
SECRET_KEY = "tu_clave_secreta_super_segura_cambiar_en_produccion"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 480  # 8 horas

# Configuración de archivos
MAX_FILE_SIZE_MB = 50
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov"}
ALLOWED_DOCUMENT_EXTENSIONS = {".pdf", ".doc", ".docx"}