from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import Consulta, Paciente, Usuario, Cita

# ============================================================================
# SCHEMAS
# ============================================================================

class ConsultaBase(BaseModel):
    paciente_id: int
    medico_id: int
    cita_id: Optional[int] = None
    motivo_consulta: str
    historia_enfermedad_actual: Optional[str] = None
    
    # Signos vitales
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    frecuencia_cardiaca: Optional[int] = None
    temperatura: Optional[float] = None
    saturacion_oxigeno: Optional[int] = None
    frecuencia_respiratoria: Optional[int] = None
    peso: Optional[float] = None
    talla: Optional[float] = None
    
    # Evaluación
    examen_fisico: Optional[str] = None
    diagnostico: Optional[str] = None
    plan_tratamiento: Optional[str] = None
    observaciones: Optional[str] = None

class ConsultaCreate(ConsultaBase):
    pass

class ConsultaUpdate(BaseModel):
    motivo_consulta: Optional[str] = None
    historia_enfermedad_actual: Optional[str] = None
    presion_sistolica: Optional[int] = None
    presion_diastolica: Optional[int] = None
    frecuencia_cardiaca: Optional[int] = None
    temperatura: Optional[float] = None
    saturacion_oxigeno: Optional[int] = None
    frecuencia_respiratoria: Optional[int] = None
    peso: Optional[float] = None
    talla: Optional[float] = None
    examen_fisico: Optional[str] = None
    diagnostico: Optional[str] = None
    plan_tratamiento: Optional[str] = None
    observaciones: Optional[str] = None

class ConsultaResponse(ConsultaBase):
    id: int
    fecha_hora: datetime
    created_at: datetime
    
    # IMC calculado
    imc: Optional[float] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/consultas",
    tags=["Consultas"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=ConsultaResponse, status_code=status.HTTP_201_CREATED)
def crear_consulta(consulta: ConsultaCreate, db: Session = Depends(get_db)):
    """Crear una nueva consulta médica"""
    
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == consulta.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar que el médico existe
    medico = db.query(Usuario).filter(Usuario.id == consulta.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    # Crear consulta
    db_consulta = Consulta(**consulta.model_dump())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    
    # Calcular IMC si hay peso y talla
    response = ConsultaResponse.model_validate(db_consulta)
    if db_consulta.peso and db_consulta.talla and db_consulta.talla > 0:
        response.imc = round(db_consulta.peso / ((db_consulta.talla / 100) ** 2), 2)
    
    return response

@router.get("/", response_model=List[ConsultaResponse])
def listar_consultas(
    skip: int = 0,
    limit: int = 100,
    paciente_id: Optional[int] = None,
    medico_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar consultas con filtros opcionales"""
    
    query = db.query(Consulta)
    
    if paciente_id:
        query = query.filter(Consulta.paciente_id == paciente_id)
    
    if medico_id:
        query = query.filter(Consulta.medico_id == medico_id)
    
    consultas = query.order_by(Consulta.fecha_hora.desc()).offset(skip).limit(limit).all()
    
    # Agregar IMC calculado
    result = []
    for consulta in consultas:
        response = ConsultaResponse.model_validate(consulta)
        if consulta.peso and consulta.talla and consulta.talla > 0:
            response.imc = round(consulta.peso / ((consulta.talla / 100) ** 2), 2)
        result.append(response)
    
    return result

@router.get("/{consulta_id}", response_model=ConsultaResponse)
def obtener_consulta(consulta_id: int, db: Session = Depends(get_db)):
    """Obtener una consulta por ID"""
    
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    response = ConsultaResponse.model_validate(consulta)
    if consulta.peso and consulta.talla and consulta.talla > 0:
        response.imc = round(consulta.peso / ((consulta.talla / 100) ** 2), 2)
    
    return response

@router.put("/{consulta_id}", response_model=ConsultaResponse)
def actualizar_consulta(
    consulta_id: int,
    consulta_update: ConsultaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una consulta"""
    
    consulta = db.query(Consulta).filter(Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(status_code=404, detail="Consulta no encontrada")
    
    update_data = consulta_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(consulta, field, value)
    
    db.commit()
    db.refresh(consulta)
    
    response = ConsultaResponse.model_validate(consulta)
    if consulta.peso and consulta.talla and consulta.talla > 0:
        response.imc = round(consulta.peso / ((consulta.talla / 100) ** 2), 2)
    
    return response

@router.get("/paciente/{paciente_id}/historial", response_model=List[ConsultaResponse])
def obtener_historial_paciente(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener historial completo de consultas de un paciente"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    consultas = db.query(Consulta).filter(
        Consulta.paciente_id == paciente_id
    ).order_by(Consulta.fecha_hora.desc()).all()
    
    result = []
    for consulta in consultas:
        response = ConsultaResponse.model_validate(consulta)
        if consulta.peso and consulta.talla and consulta.talla > 0:
            response.imc = round(consulta.peso / ((consulta.talla / 100) ** 2), 2)
        result.append(response)
    
    return result