from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import NotaMedica, TipoNotaMedicaEnum, Hospitalizacion, Usuario

# ============================================================================
# SCHEMAS
# ============================================================================

class NotaMedicaBase(BaseModel):
    hospitalizacion_id: int
    medico_id: int
    tipo: TipoNotaMedicaEnum
    contenido: str
    
    # Campos específicos de nota operatoria
    cirugia_realizada: Optional[str] = None
    cirujano_id: Optional[int] = None
    anestesiologo: Optional[str] = None
    tipo_anestesia: Optional[str] = None
    diagnostico_preoperatorio: Optional[str] = None
    diagnostico_postoperatorio: Optional[str] = None
    hallazgos: Optional[str] = None
    complicaciones: Optional[str] = None
    sangrado_estimado: Optional[str] = None
    especimenes_patologia: Optional[str] = None
    pronostico: Optional[str] = None

class NotaMedicaCreate(NotaMedicaBase):
    pass

class NotaMedicaResponse(NotaMedicaBase):
    id: int
    fecha_hora: datetime
    medico_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/notas-medicas",
    tags=["Notas Médicas"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=NotaMedicaResponse, status_code=status.HTTP_201_CREATED)
def crear_nota_medica(nota: NotaMedicaCreate, db: Session = Depends(get_db)):
    """Crear una nota médica"""
    
    # Verificar hospitalización
    hosp = db.query(Hospitalizacion).filter(Hospitalizacion.id == nota.hospitalizacion_id).first()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalización no encontrada")
    
    # Verificar médico
    medico = db.query(Usuario).filter(Usuario.id == nota.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    db_nota = NotaMedica(**nota.model_dump())
    db.add(db_nota)
    db.commit()
    db.refresh(db_nota)
    
    response = NotaMedicaResponse.model_validate(db_nota)
    response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    
    return response

@router.get("/hospitalizacion/{hospitalizacion_id}", response_model=List[NotaMedicaResponse])
def listar_notas_hospitalizacion(
    hospitalizacion_id: int,
    tipo: Optional[TipoNotaMedicaEnum] = None,
    db: Session = Depends(get_db)
):
    """Listar notas de una hospitalización"""
    
    query = db.query(NotaMedica).filter(NotaMedica.hospitalizacion_id == hospitalizacion_id)
    
    if tipo:
        query = query.filter(NotaMedica.tipo == tipo)
    
    notas = query.order_by(NotaMedica.fecha_hora.desc()).all()
    
    result = []
    for nota in notas:
        medico = db.query(Usuario).filter(Usuario.id == nota.medico_id).first()
        response = NotaMedicaResponse.model_validate(nota)
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        result.append(response)
    
    return result

@router.get("/{nota_id}", response_model=NotaMedicaResponse)
def obtener_nota(nota_id: int, db: Session = Depends(get_db)):
    """Obtener una nota médica por ID"""
    
    nota = db.query(NotaMedica).filter(NotaMedica.id == nota_id).first()
    if not nota:
        raise HTTPException(status_code=404, detail="Nota no encontrada")
    
    medico = db.query(Usuario).filter(Usuario.id == nota.medico_id).first()
    response = NotaMedicaResponse.model_validate(nota)
    if medico:
        response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    
    return response