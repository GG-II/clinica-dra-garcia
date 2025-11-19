from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime, date, timedelta
from pydantic import BaseModel
from create_simple_tables import Cita, Paciente, Usuario, TipoCitaEnum, EstadoCitaEnum

# ============================================================================
# SCHEMAS
# ============================================================================

class CitaBase(BaseModel):
    paciente_id: int
    medico_id: int
    fecha_hora: datetime
    duracion_minutos: int = 20
    tipo_cita: TipoCitaEnum
    motivo: Optional[str] = None
    notas: Optional[str] = None

class CitaCreate(CitaBase):
    pass

class CitaUpdate(BaseModel):
    fecha_hora: Optional[datetime] = None
    duracion_minutos: Optional[int] = None
    tipo_cita: Optional[TipoCitaEnum] = None
    estado: Optional[EstadoCitaEnum] = None
    motivo: Optional[str] = None
    notas: Optional[str] = None
    confirmada_paciente: Optional[bool] = None

class CitaResponse(CitaBase):
    id: int
    estado: EstadoCitaEnum
    recordatorio_enviado: bool
    confirmada_paciente: bool
    created_at: datetime
    
    # Información adicional
    paciente_nombre: Optional[str] = None
    medico_nombre: Optional[str] = None

    class Config:
        from_attributes = True

class AgendaDiaResponse(BaseModel):
    fecha: date
    medico_id: int
    medico_nombre: str
    total_citas: int
    citas: List[CitaResponse]

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/citas",
    tags=["Citas"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=CitaResponse, status_code=status.HTTP_201_CREATED)
def crear_cita(cita: CitaCreate, db: Session = Depends(get_db)):
    """Crear una nueva cita"""
    
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == cita.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar que el médico existe
    medico = db.query(Usuario).filter(Usuario.id == cita.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    # Verificar disponibilidad (no permitir citas en el mismo horario)
    cita_existente = db.query(Cita).filter(
        Cita.medico_id == cita.medico_id,
        Cita.fecha_hora == cita.fecha_hora,
        Cita.estado.in_([EstadoCitaEnum.programada, EstadoCitaEnum.confirmada])
    ).first()
    
    if cita_existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una cita programada en este horario"
        )
    
    # Crear cita
    db_cita = Cita(**cita.model_dump())
    db.add(db_cita)
    db.commit()
    db.refresh(db_cita)
    
    return db_cita

@router.get("/", response_model=List[CitaResponse])
def listar_citas(
    skip: int = 0,
    limit: int = 100,
    medico_id: Optional[int] = None,
    paciente_id: Optional[int] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    estado: Optional[EstadoCitaEnum] = None,
    db: Session = Depends(get_db)
):
    """Listar citas con filtros opcionales"""
    
    query = db.query(Cita)
    
    if medico_id:
        query = query.filter(Cita.medico_id == medico_id)
    
    if paciente_id:
        query = query.filter(Cita.paciente_id == paciente_id)
    
    if fecha_desde:
        query = query.filter(Cita.fecha_hora >= datetime.combine(fecha_desde, datetime.min.time()))
    
    if fecha_hasta:
        query = query.filter(Cita.fecha_hora <= datetime.combine(fecha_hasta, datetime.max.time()))
    
    if estado:
        query = query.filter(Cita.estado == estado)
    
    citas = query.order_by(Cita.fecha_hora).offset(skip).limit(limit).all()
    return citas

@router.get("/agenda/{medico_id}/{fecha}", response_model=AgendaDiaResponse)
def obtener_agenda_dia(medico_id: int, fecha: date, db: Session = Depends(get_db)):
    """Obtener agenda completa de un médico para un día específico"""
    
    medico = db.query(Usuario).filter(Usuario.id == medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    # Obtener citas del día
    fecha_inicio = datetime.combine(fecha, datetime.min.time())
    fecha_fin = datetime.combine(fecha, datetime.max.time())
    
    citas = db.query(Cita).filter(
        Cita.medico_id == medico_id,
        Cita.fecha_hora >= fecha_inicio,
        Cita.fecha_hora <= fecha_fin
    ).order_by(Cita.fecha_hora).all()
    
    return {
        "fecha": fecha,
        "medico_id": medico_id,
        "medico_nombre": f"{medico.nombres} {medico.apellidos}",
        "total_citas": len(citas),
        "citas": citas
    }

@router.get("/{cita_id}", response_model=CitaResponse)
def obtener_cita(cita_id: int, db: Session = Depends(get_db)):
    """Obtener una cita por ID"""
    
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    return cita

@router.put("/{cita_id}", response_model=CitaResponse)
def actualizar_cita(
    cita_id: int,
    cita_update: CitaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar una cita"""
    
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    # Actualizar campos
    update_data = cita_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(cita, field, value)
    
    db.commit()
    db.refresh(cita)
    
    return cita

@router.delete("/{cita_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancelar_cita(cita_id: int, db: Session = Depends(get_db)):
    """Cancelar una cita"""
    
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    cita.estado = EstadoCitaEnum.cancelada
    db.commit()
    
    return None

@router.post("/{cita_id}/confirmar")
def confirmar_cita(cita_id: int, db: Session = Depends(get_db)):
    """Confirmar asistencia del paciente"""
    
    cita = db.query(Cita).filter(Cita.id == cita_id).first()
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    
    cita.confirmada_paciente = True
    cita.estado = EstadoCitaEnum.confirmada
    db.commit()
    
    return {"message": "Cita confirmada exitosamente"}