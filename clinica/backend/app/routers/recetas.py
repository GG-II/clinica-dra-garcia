from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import Receta, RecetaDetalle, Consulta, Paciente, Usuario, Medicamento

# ============================================================================
# SCHEMAS
# ============================================================================

class RecetaDetalleBase(BaseModel):
    medicamento_id: Optional[int] = None
    medicamento_texto: str
    presentacion: Optional[str] = None
    dosis: str
    frecuencia: str
    duracion: str
    via_administracion: Optional[str] = None
    indicaciones: Optional[str] = None

class RecetaDetalleCreate(RecetaDetalleBase):
    pass

class RecetaDetalleResponse(RecetaDetalleBase):
    id: int
    receta_id: int

    class Config:
        from_attributes = True

class RecetaBase(BaseModel):
    consulta_id: int
    paciente_id: int
    medico_id: int
    indicaciones_generales: Optional[str] = None

class RecetaCreate(BaseModel):
    consulta_id: int
    paciente_id: int
    medico_id: int
    indicaciones_generales: Optional[str] = None
    medicamentos: List[RecetaDetalleCreate]

class RecetaResponse(RecetaBase):
    id: int
    created_at: datetime
    medicamentos: List[RecetaDetalleResponse] = []

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/recetas",
    tags=["Recetas"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=RecetaResponse, status_code=status.HTTP_201_CREATED)
def crear_receta(receta: RecetaCreate, db: Session = Depends(get_db)):
    """Crear una nueva receta con medicamentos"""
    
    # Verificar que la consulta existe
    consulta = db.query(Consulta).filter(Consulta.id == receta.consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == receta.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar médico
    medico = db.query(Usuario).filter(Usuario.id == receta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    # Crear receta
    db_receta = Receta(
        consulta_id=receta.consulta_id,
        paciente_id=receta.paciente_id,
        medico_id=receta.medico_id,
        indicaciones_generales=receta.indicaciones_generales
    )
    db.add(db_receta)
    db.flush()  # Para obtener el ID antes del commit
    
    # Agregar medicamentos
    for med in receta.medicamentos:
        detalle = RecetaDetalle(
            receta_id=db_receta.id,
            **med.model_dump()
        )
        db.add(detalle)
    
    db.commit()
    db.refresh(db_receta)
    
    # Cargar medicamentos
    medicamentos = db.query(RecetaDetalle).filter(RecetaDetalle.receta_id == db_receta.id).all()
    
    response = RecetaResponse.model_validate(db_receta)
    response.medicamentos = [RecetaDetalleResponse.model_validate(m) for m in medicamentos]
    
    return response

@router.get("/", response_model=List[RecetaResponse])
def listar_recetas(
    skip: int = 0,
    limit: int = 100,
    paciente_id: Optional[int] = None,
    medico_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar recetas con filtros opcionales"""
    
    query = db.query(Receta)
    
    if paciente_id:
        query = query.filter(Receta.paciente_id == paciente_id)
    
    if medico_id:
        query = query.filter(Receta.medico_id == medico_id)
    
    recetas = query.order_by(Receta.created_at.desc()).offset(skip).limit(limit).all()
    
    # Cargar medicamentos para cada receta
    result = []
    for receta in recetas:
        medicamentos = db.query(RecetaDetalle).filter(RecetaDetalle.receta_id == receta.id).all()
        response = RecetaResponse.model_validate(receta)
        response.medicamentos = [RecetaDetalleResponse.model_validate(m) for m in medicamentos]
        result.append(response)
    
    return result

@router.get("/{receta_id}", response_model=RecetaResponse)
def obtener_receta(receta_id: int, db: Session = Depends(get_db)):
    """Obtener una receta por ID con sus medicamentos"""
    
    receta = db.query(Receta).filter(Receta.id == receta_id).first()
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    
    medicamentos = db.query(RecetaDetalle).filter(RecetaDetalle.receta_id == receta_id).all()
    
    response = RecetaResponse.model_validate(receta)
    response.medicamentos = [RecetaDetalleResponse.model_validate(m) for m in medicamentos]
    
    return response

@router.get("/paciente/{paciente_id}/historial", response_model=List[RecetaResponse])
def obtener_recetas_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener historial de recetas de un paciente"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    recetas = db.query(Receta).filter(
        Receta.paciente_id == paciente_id
    ).order_by(Receta.created_at.desc()).all()
    
    result = []
    for receta in recetas:
        medicamentos = db.query(RecetaDetalle).filter(RecetaDetalle.receta_id == receta.id).all()
        response = RecetaResponse.model_validate(receta)
        response.medicamentos = [RecetaDetalleResponse.model_validate(m) for m in medicamentos]
        result.append(response)
    
    return result