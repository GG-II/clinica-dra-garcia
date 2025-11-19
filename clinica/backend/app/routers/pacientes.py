from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import date, datetime
from pathlib import Path
import uuid
from pydantic import BaseModel, EmailStr, validator

# Importar desde create_simple_tables
from create_simple_tables import (
    Paciente, 
    GeneroEnum, 
    EstadoCivilEnum, 
    TipoSangreEnum,
    ArchivosPaciente,
    CategoriaArchivoEnum
)

# ============================================================================
# CONFIGURACIÓN DE RUTAS DE ARCHIVOS
# ============================================================================

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent / "clinica-archivos"
PACIENTES_PATH = BASE_PATH / "pacientes"

# Crear directorios si no existen
PACIENTES_PATH.mkdir(parents=True, exist_ok=True)
for categoria in ["fotos", "laboratorios", "imagenes", "recetas", "ekg", "videos", "otros"]:
    (PACIENTES_PATH / categoria).mkdir(exist_ok=True)

# Límites de tamaño
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50 MB
MAX_DOC_SIZE = 5 * 1024 * 1024  # 5 MB

# ============================================================================
# SCHEMAS PYDANTIC
# ============================================================================

class PacienteBase(BaseModel):
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    genero: GeneroEnum
    dpi: str
    telefono_principal: str
    telefono_secundario: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: str
    municipio: Optional[str] = None
    departamento: Optional[str] = None
    estado_civil: Optional[EstadoCivilEnum] = None
    religion: Optional[str] = None
    ocupacion: Optional[str] = None
    tipo_sangre: Optional[TipoSangreEnum] = None
    tiene_igss: bool = False
    numero_igss: Optional[str] = None
    tiene_seguro_privado: bool = False
    nombre_seguro: Optional[str] = None
    emergencia_nombre: str
    emergencia_telefono: str
    emergencia_parentesco: Optional[str] = None
    observaciones: Optional[str] = None

    @validator('dpi')
    def validar_dpi(cls, v):
        if not v.isdigit():
            raise ValueError('DPI debe contener solo números')
        if len(v) != 13:
            raise ValueError('DPI debe tener exactamente 13 dígitos')
        return v

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(BaseModel):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[GeneroEnum] = None
    dpi: Optional[str] = None
    telefono_principal: Optional[str] = None
    telefono_secundario: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: Optional[str] = None
    municipio: Optional[str] = None
    departamento: Optional[str] = None
    estado_civil: Optional[EstadoCivilEnum] = None
    religion: Optional[str] = None
    ocupacion: Optional[str] = None
    tipo_sangre: Optional[TipoSangreEnum] = None
    tiene_igss: Optional[bool] = None
    numero_igss: Optional[str] = None
    tiene_seguro_privado: Optional[bool] = None
    nombre_seguro: Optional[str] = None
    emergencia_nombre: Optional[str] = None
    emergencia_telefono: Optional[str] = None
    emergencia_parentesco: Optional[str] = None
    observaciones: Optional[str] = None
    activo: Optional[bool] = None

class PacienteResponse(PacienteBase):
    id: int
    activo: bool
    foto_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ArchivoResponse(BaseModel):
    id: int
    paciente_id: int
    categoria: CategoriaArchivoEnum
    nombre_archivo: str
    ruta_archivo: str
    tipo_mime: str
    tamano_bytes: int
    descripcion: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class EstadisticasPacientes(BaseModel):
    total_pacientes: int
    pacientes_activos: int
    pacientes_inactivos: int
    nuevos_este_mes: int
    por_genero: dict
    por_tipo_sangre: dict

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/pacientes",
    tags=["Pacientes"]
)

# ============================================================================
# ENDPOINTS CRUD BÁSICO
# ============================================================================

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo paciente"""
    
    # Verificar que el DPI no esté registrado
    paciente_existente = db.query(Paciente).filter(Paciente.dpi == paciente.dpi).first()
    if paciente_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un paciente registrado con este DPI"
        )
    
    # Crear paciente
    db_paciente = Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    db.refresh(db_paciente)
    
    return db_paciente

@router.get("/", response_model=List[PacienteResponse])
def listar_pacientes(
    skip: int = 0,
    limit: int = 100,
    buscar: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Listar todos los pacientes con búsqueda opcional"""
    
    query = db.query(Paciente).filter(Paciente.activo == True)
    
    # Búsqueda por nombre, apellido o DPI
    if buscar:
        buscar_lower = f"%{buscar.lower()}%"
        query = query.filter(
            (Paciente.nombres.ilike(buscar_lower)) |
            (Paciente.apellidos.ilike(buscar_lower)) |
            (Paciente.dpi.ilike(buscar_lower))
        )
    
    pacientes = query.offset(skip).limit(limit).all()
    return pacientes

@router.get("/estadisticas", response_model=EstadisticasPacientes)
def obtener_estadisticas_pacientes(db: Session = Depends(get_db)):
    """Obtener estadísticas generales de pacientes"""
    from sqlalchemy import func, extract
    
    # Total de pacientes
    total = db.query(Paciente).count()
    activos = db.query(Paciente).filter(Paciente.activo == True).count()
    inactivos = total - activos
    
    # Nuevos este mes
    hoy = datetime.now()
    nuevos_mes = db.query(Paciente).filter(
        extract('year', Paciente.created_at) == hoy.year,
        extract('month', Paciente.created_at) == hoy.month
    ).count()
    
    # Por género
    por_genero = {}
    generos = db.query(
        Paciente.genero,
        func.count(Paciente.id)
    ).group_by(Paciente.genero).all()
    
    for genero, count in generos:
        por_genero[genero.value if genero else "No especificado"] = count
    
    # Por tipo de sangre
    por_tipo_sangre = {}
    tipos = db.query(
        Paciente.tipo_sangre,
        func.count(Paciente.id)
    ).group_by(Paciente.tipo_sangre).all()
    
    for tipo, count in tipos:
        por_tipo_sangre[tipo.value if tipo else "No especificado"] = count
    
    return {
        "total_pacientes": total,
        "pacientes_activos": activos,
        "pacientes_inactivos": inactivos,
        "nuevos_este_mes": nuevos_mes,
        "por_genero": por_genero,
        "por_tipo_sangre": por_tipo_sangre
    }

@router.get("/{paciente_id}", response_model=PacienteResponse)
def obtener_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener un paciente por ID"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    return paciente

@router.put("/{paciente_id}", response_model=PacienteResponse)
def actualizar_paciente(
    paciente_id: int,
    paciente_update: PacienteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un paciente"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    # Actualizar solo los campos enviados
    update_data = paciente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(paciente, field, value)
    
    db.commit()
    db.refresh(paciente)
    
    return paciente

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Desactivar un paciente (borrado lógico)"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    paciente.activo = False
    db.commit()
    
    return None

# ============================================================================
# ENDPOINTS DE ARCHIVOS
# ============================================================================

@router.post("/{paciente_id}/foto", response_model=ArchivoResponse)
async def subir_foto_paciente(
    paciente_id: int,
    foto: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Subir foto del paciente"""
    
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Validar tipo de archivo
    if not foto.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
    
    # Validar tamaño
    contenido = await foto.read()
    if len(contenido) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="La imagen no puede ser mayor a 5 MB")
    
    # Generar nombre único
    extension = Path(foto.filename).suffix
    nombre_unico = f"{uuid.uuid4()}{extension}"
    
    # Guardar archivo
    ruta_carpeta = PACIENTES_PATH / "fotos" / str(paciente_id)
    ruta_carpeta.mkdir(parents=True, exist_ok=True)
    ruta_archivo = ruta_carpeta / nombre_unico
    
    with open(ruta_archivo, "wb") as f:
        f.write(contenido)
    
    # Actualizar foto_url del paciente
    paciente.foto_url = str(ruta_archivo.relative_to(BASE_PATH))
    
    # Guardar registro en BD
    archivo_db = ArchivosPaciente(
        paciente_id=paciente_id,
        categoria=CategoriaArchivoEnum.foto,
        nombre_archivo=foto.filename,
        ruta_archivo=str(ruta_archivo.relative_to(BASE_PATH)),
        tipo_mime=foto.content_type,
        tamano_bytes=len(contenido)
    )
    
    db.add(archivo_db)
    db.commit()
    db.refresh(archivo_db)
    
    return archivo_db

@router.post("/{paciente_id}/archivos", response_model=ArchivoResponse)
async def subir_archivo_paciente(
    paciente_id: int,
    categoria: CategoriaArchivoEnum,
    archivo: UploadFile = File(...),
    descripcion: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Subir documento del paciente (laboratorio, imagen, receta, EKG, video)"""
    
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Validar tamaño según tipo
    contenido = await archivo.read()
    
    if categoria == CategoriaArchivoEnum.video:
        if len(contenido) > MAX_VIDEO_SIZE:
            raise HTTPException(status_code=400, detail="El video no puede ser mayor a 50 MB")
    else:
        if len(contenido) > MAX_DOC_SIZE:
            raise HTTPException(status_code=400, detail="El archivo no puede ser mayor a 5 MB")
    
    # Generar nombre único
    extension = Path(archivo.filename).suffix
    nombre_unico = f"{uuid.uuid4()}{extension}"
    
    # Determinar carpeta según categoría
    carpeta_map = {
        CategoriaArchivoEnum.laboratorio: "laboratorios",
        CategoriaArchivoEnum.imagen: "imagenes",
        CategoriaArchivoEnum.receta: "recetas",
        CategoriaArchivoEnum.ekg: "ekg",
        CategoriaArchivoEnum.video: "videos",
        CategoriaArchivoEnum.otro: "otros"
    }
    
    carpeta = carpeta_map.get(categoria, "otros")
    
    # Guardar archivo
    ruta_carpeta = PACIENTES_PATH / carpeta / str(paciente_id)
    ruta_carpeta.mkdir(parents=True, exist_ok=True)
    ruta_archivo = ruta_carpeta / nombre_unico
    
    with open(ruta_archivo, "wb") as f:
        f.write(contenido)
    
    # Guardar registro en BD
    archivo_db = ArchivosPaciente(
        paciente_id=paciente_id,
        categoria=categoria,
        nombre_archivo=archivo.filename,
        ruta_archivo=str(ruta_archivo.relative_to(BASE_PATH)),
        tipo_mime=archivo.content_type,
        tamano_bytes=len(contenido),
        descripcion=descripcion
    )
    
    db.add(archivo_db)
    db.commit()
    db.refresh(archivo_db)
    
    return archivo_db

@router.get("/{paciente_id}/archivos", response_model=List[ArchivoResponse])
def listar_archivos_paciente(
    paciente_id: int,
    categoria: Optional[CategoriaArchivoEnum] = None,
    db: Session = Depends(get_db)
):
    """Listar archivos del paciente, opcionalmente filtrados por categoría"""
    
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    query = db.query(ArchivosPaciente).filter(ArchivosPaciente.paciente_id == paciente_id)
    
    if categoria:
        query = query.filter(ArchivosPaciente.categoria == categoria)
    
    archivos = query.order_by(ArchivosPaciente.created_at.desc()).all()
    return archivos

@router.delete("/{paciente_id}/archivos/{archivo_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_archivo_paciente(
    paciente_id: int,
    archivo_id: int,
    db: Session = Depends(get_db)
):
    """Eliminar un archivo del paciente"""
    
    archivo = db.query(ArchivosPaciente).filter(
        ArchivosPaciente.id == archivo_id,
        ArchivosPaciente.paciente_id == paciente_id
    ).first()
    
    if not archivo:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    
    # Eliminar archivo físico
    ruta_completa = BASE_PATH / archivo.ruta_archivo
    if ruta_completa.exists():
        ruta_completa.unlink()
    
    # Eliminar registro de BD
    db.delete(archivo)
    db.commit()
    
    return None