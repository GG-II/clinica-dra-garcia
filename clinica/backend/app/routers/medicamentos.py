from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import Medicamento

# ============================================================================
# SCHEMAS
# ============================================================================

class MedicamentoBase(BaseModel):
    nombre_generico: str
    nombre_comercial: Optional[str] = None
    presentacion: Optional[str] = None
    concentracion: Optional[str] = None
    via_administracion: Optional[str] = None
    interacciones: Optional[str] = None
    contraindicaciones: Optional[str] = None

class MedicamentoCreate(MedicamentoBase):
    pass

class MedicamentoUpdate(BaseModel):
    nombre_generico: Optional[str] = None
    nombre_comercial: Optional[str] = None
    presentacion: Optional[str] = None
    concentracion: Optional[str] = None
    via_administracion: Optional[str] = None
    interacciones: Optional[str] = None
    contraindicaciones: Optional[str] = None
    activo: Optional[bool] = None

class MedicamentoResponse(MedicamentoBase):
    id: int
    activo: bool
    created_at: datetime

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=MedicamentoResponse, status_code=status.HTTP_201_CREATED)
def crear_medicamento(medicamento: MedicamentoCreate, db: Session = Depends(get_db)):
    """Crear un nuevo medicamento"""
    
    db_medicamento = Medicamento(**medicamento.model_dump())
    db.add(db_medicamento)
    db.commit()
    db.refresh(db_medicamento)
    
    return db_medicamento

@router.get("/", response_model=List[MedicamentoResponse])
def listar_medicamentos(
    skip: int = 0,
    limit: int = 100,
    buscar: Optional[str] = None,
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar medicamentos con búsqueda opcional"""
    
    query = db.query(Medicamento).filter(Medicamento.activo == activo)
    
    if buscar:
        buscar_lower = f"%{buscar.lower()}%"
        query = query.filter(
            (Medicamento.nombre_generico.ilike(buscar_lower)) |
            (Medicamento.nombre_comercial.ilike(buscar_lower))
        )
    
    medicamentos = query.offset(skip).limit(limit).all()
    return medicamentos

@router.get("/{medicamento_id}", response_model=MedicamentoResponse)
def obtener_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    """Obtener un medicamento por ID"""
    
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    
    return medicamento

@router.put("/{medicamento_id}", response_model=MedicamentoResponse)
def actualizar_medicamento(
    medicamento_id: int,
    medicamento_update: MedicamentoUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un medicamento"""
    
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    
    update_data = medicamento_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(medicamento, field, value)
    
    db.commit()
    db.refresh(medicamento)
    
    return medicamento

@router.delete("/{medicamento_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_medicamento(medicamento_id: int, db: Session = Depends(get_db)):
    """Desactivar un medicamento"""
    
    medicamento = db.query(Medicamento).filter(Medicamento.id == medicamento_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento no encontrado")
    
    medicamento.activo = False
    db.commit()
    
    return None