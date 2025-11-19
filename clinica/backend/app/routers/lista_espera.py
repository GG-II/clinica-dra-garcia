from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import ListaEspera, TipoCitaEnum, Paciente, Usuario

# ============================================================================
# SCHEMAS
# ============================================================================

class ListaEsperaBase(BaseModel):
    paciente_id: int
    medico_id: int
    tipo_cita: TipoCitaEnum
    motivo: Optional[str] = None
    prioridad: int = 0

class ListaEsperaCreate(ListaEsperaBase):
    pass

class ListaEsperaUpdate(BaseModel):
    prioridad: Optional[int] = None
    notificado: Optional[bool] = None
    activo: Optional[bool] = None

class ListaEsperaResponse(ListaEsperaBase):
    id: int
    fecha_solicitud: datetime
    notificado: bool
    activo: bool
    paciente_nombre: Optional[str] = None
    medico_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/lista-espera",
    tags=["Lista de Espera"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=ListaEsperaResponse, status_code=status.HTTP_201_CREATED)
def agregar_a_lista_espera(item: ListaEsperaCreate, db: Session = Depends(get_db)):
    """Agregar paciente a lista de espera"""
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == item.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar médico
    medico = db.query(Usuario).filter(Usuario.id == item.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    # Verificar si ya está en lista de espera activa
    existe = db.query(ListaEspera).filter(
        ListaEspera.paciente_id == item.paciente_id,
        ListaEspera.medico_id == item.medico_id,
        ListaEspera.activo == True
    ).first()
    
    if existe:
        raise HTTPException(
            status_code=400,
            detail="El paciente ya está en la lista de espera para este médico"
        )
    
    db_item = ListaEspera(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    response = ListaEsperaResponse.model_validate(db_item)
    response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    
    return response

@router.get("/", response_model=List[ListaEsperaResponse])
def listar_lista_espera(
    medico_id: Optional[int] = None,
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar pacientes en lista de espera"""
    
    query = db.query(ListaEspera).filter(ListaEspera.activo == activo)
    
    if medico_id:
        query = query.filter(ListaEspera.medico_id == medico_id)
    
    items = query.order_by(
        ListaEspera.prioridad.desc(),
        ListaEspera.fecha_solicitud
    ).all()
    
    result = []
    for item in items:
        paciente = db.query(Paciente).filter(Paciente.id == item.paciente_id).first()
        medico = db.query(Usuario).filter(Usuario.id == item.medico_id).first()
        
        response = ListaEsperaResponse.model_validate(item)
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        
        result.append(response)
    
    return result

@router.put("/{item_id}", response_model=ListaEsperaResponse)
def actualizar_lista_espera(
    item_id: int,
    update: ListaEsperaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar item de lista de espera"""
    
    item = db.query(ListaEspera).filter(ListaEspera.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    update_data = update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_de_lista_espera(item_id: int, db: Session = Depends(get_db)):
    """Remover paciente de lista de espera"""
    
    item = db.query(ListaEspera).filter(ListaEspera.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    item.activo = False
    db.commit()
    
    return None