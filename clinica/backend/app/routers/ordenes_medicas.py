from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import OrdenMedica, TipoOrdenEnum, EstadoOrdenEnum, Hospitalizacion, Usuario, Medicamento

# ============================================================================
# SCHEMAS
# ============================================================================

class OrdenMedicaBase(BaseModel):
    hospitalizacion_id: int
    medico_id: int
    tipo: TipoOrdenEnum
    descripcion: str
    medicamento_id: Optional[int] = None
    dosis: Optional[str] = None
    frecuencia: Optional[str] = None
    via: Optional[str] = None
    duracion: Optional[str] = None

class OrdenMedicaCreate(OrdenMedicaBase):
    pass

class OrdenMedicaUpdate(BaseModel):
    estado: EstadoOrdenEnum

class OrdenMedicaResponse(OrdenMedicaBase):
    id: int
    estado: EstadoOrdenEnum
    fecha_hora: datetime
    medico_nombre: Optional[str] = None
    medicamento_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/ordenes-medicas",
    tags=["Órdenes Médicas"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=OrdenMedicaResponse, status_code=status.HTTP_201_CREATED)
def crear_orden(orden: OrdenMedicaCreate, db: Session = Depends(get_db)):
    """Crear una orden médica"""
    
    # Verificar hospitalización
    hosp = db.query(Hospitalizacion).filter(Hospitalizacion.id == orden.hospitalizacion_id).first()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalización no encontrada")
    
    # Verificar médico
    medico = db.query(Usuario).filter(Usuario.id == orden.medico_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    db_orden = OrdenMedica(**orden.model_dump())
    db.add(db_orden)
    db.commit()
    db.refresh(db_orden)
    
    response = OrdenMedicaResponse.model_validate(db_orden)
    response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    
    if db_orden.medicamento_id:
        med = db.query(Medicamento).filter(Medicamento.id == db_orden.medicamento_id).first()
        if med:
            response.medicamento_nombre = med.nombre_generico
    
    return response

@router.get("/hospitalizacion/{hospitalizacion_id}", response_model=List[OrdenMedicaResponse])
def listar_ordenes_hospitalizacion(
    hospitalizacion_id: int,
    estado: Optional[EstadoOrdenEnum] = None,
    db: Session = Depends(get_db)
):
    """Listar órdenes de una hospitalización"""
    
    query = db.query(OrdenMedica).filter(OrdenMedica.hospitalizacion_id == hospitalizacion_id)
    
    if estado:
        query = query.filter(OrdenMedica.estado == estado)
    
    ordenes = query.order_by(OrdenMedica.fecha_hora.desc()).all()
    
    result = []
    for orden in ordenes:
        medico = db.query(Usuario).filter(Usuario.id == orden.medico_id).first()
        response = OrdenMedicaResponse.model_validate(orden)
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        
        if orden.medicamento_id:
            med = db.query(Medicamento).filter(Medicamento.id == orden.medicamento_id).first()
            if med:
                response.medicamento_nombre = med.nombre_generico
        
        result.append(response)
    
    return result

@router.put("/{orden_id}", response_model=OrdenMedicaResponse)
def actualizar_estado_orden(
    orden_id: int,
    orden_update: OrdenMedicaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar estado de una orden"""
    
    orden = db.query(OrdenMedica).filter(OrdenMedica.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    orden.estado = orden_update.estado
    db.commit()
    db.refresh(orden)
    
    return orden