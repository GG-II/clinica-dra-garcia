from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import Interconsulta, EstadoInterconsultaEnum, Paciente, Usuario, Consulta, Hospitalizacion

# ============================================================================
# SCHEMAS
# ============================================================================

class InterconsultaBase(BaseModel):
    paciente_id: int
    consulta_id: Optional[int] = None
    hospitalizacion_id: Optional[int] = None
    medico_solicitante_id: int
    especialidad_solicitada: str
    motivo: str
    medico_consultor_id: Optional[int] = None
    hallazgos: Optional[str] = None
    recomendaciones: Optional[str] = None

class InterconsultaCreate(InterconsultaBase):
    pass

class InterconsultaUpdate(BaseModel):
    medico_consultor_id: Optional[int] = None
    hallazgos: Optional[str] = None
    recomendaciones: Optional[str] = None
    estado: Optional[EstadoInterconsultaEnum] = None

class InterconsultaResponse(InterconsultaBase):
    id: int
    estado: EstadoInterconsultaEnum
    fecha_solicitud: datetime
    fecha_respuesta: Optional[datetime]
    solicitante_nombre: Optional[str] = None
    consultor_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/interconsultas",
    tags=["Interconsultas"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=InterconsultaResponse, status_code=status.HTTP_201_CREATED)
def crear_interconsulta(interconsulta: InterconsultaCreate, db: Session = Depends(get_db)):
    """Solicitar una interconsulta"""
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == interconsulta.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar médico solicitante
    solicitante = db.query(Usuario).filter(Usuario.id == interconsulta.medico_solicitante_id).first()
    if not solicitante:
        raise HTTPException(status_code=404, detail="Médico solicitante no encontrado")
    
    db_interconsulta = Interconsulta(**interconsulta.model_dump())
    db.add(db_interconsulta)
    db.commit()
    db.refresh(db_interconsulta)
    
    response = InterconsultaResponse.model_validate(db_interconsulta)
    response.solicitante_nombre = f"{solicitante.nombres} {solicitante.apellidos}"
    
    return response

@router.get("/", response_model=List[InterconsultaResponse])
def listar_interconsultas(
    paciente_id: Optional[int] = None,
    estado: Optional[EstadoInterconsultaEnum] = None,
    medico_consultor_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar interconsultas"""
    
    query = db.query(Interconsulta)
    
    if paciente_id:
        query = query.filter(Interconsulta.paciente_id == paciente_id)
    
    if estado:
        query = query.filter(Interconsulta.estado == estado)
    
    if medico_consultor_id:
        query = query.filter(Interconsulta.medico_consultor_id == medico_consultor_id)
    
    interconsultas = query.order_by(Interconsulta.fecha_solicitud.desc()).all()
    
    result = []
    for ic in interconsultas:
        solicitante = db.query(Usuario).filter(Usuario.id == ic.medico_solicitante_id).first()
        response = InterconsultaResponse.model_validate(ic)
        if solicitante:
            response.solicitante_nombre = f"{solicitante.nombres} {solicitante.apellidos}"
        
        if ic.medico_consultor_id:
            consultor = db.query(Usuario).filter(Usuario.id == ic.medico_consultor_id).first()
            if consultor:
                response.consultor_nombre = f"{consultor.nombres} {consultor.apellidos}"
        
        result.append(response)
    
    return result

@router.get("/{interconsulta_id}", response_model=InterconsultaResponse)
def obtener_interconsulta(interconsulta_id: int, db: Session = Depends(get_db)):
    """Obtener una interconsulta por ID"""
    
    ic = db.query(Interconsulta).filter(Interconsulta.id == interconsulta_id).first()
    if not ic:
        raise HTTPException(status_code=404, detail="Interconsulta no encontrada")
    
    solicitante = db.query(Usuario).filter(Usuario.id == ic.medico_solicitante_id).first()
    response = InterconsultaResponse.model_validate(ic)
    if solicitante:
        response.solicitante_nombre = f"{solicitante.nombres} {solicitante.apellidos}"
    
    if ic.medico_consultor_id:
        consultor = db.query(Usuario).filter(Usuario.id == ic.medico_consultor_id).first()
        if consultor:
            response.consultor_nombre = f"{consultor.nombres} {consultor.apellidos}"
    
    return response

@router.put("/{interconsulta_id}", response_model=InterconsultaResponse)
def responder_interconsulta(
    interconsulta_id: int,
    update: InterconsultaUpdate,
    db: Session = Depends(get_db)
):
    """Responder/actualizar una interconsulta"""
    
    ic = db.query(Interconsulta).filter(Interconsulta.id == interconsulta_id).first()
    if not ic:
        raise HTTPException(status_code=404, detail="Interconsulta no encontrada")
    
    update_data = update.model_dump(exclude_unset=True)
    
    # Si se está completando la interconsulta, registrar fecha de respuesta
    if 'estado' in update_data and update_data['estado'] == EstadoInterconsultaEnum.completada:
        ic.fecha_respuesta = datetime.now()
    
    for field, value in update_data.items():
        setattr(ic, field, value)
    
    db.commit()
    db.refresh(ic)
    
    return ic