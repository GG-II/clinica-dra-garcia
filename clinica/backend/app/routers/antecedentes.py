from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from pydantic import BaseModel
from create_simple_tables import Antecedente, Paciente, TipoAntecedenteEnum

# ============================================================================
# SCHEMAS
# ============================================================================

class AntecedenteBase(BaseModel):
    paciente_id: int
    tipo: TipoAntecedenteEnum
    descripcion: str

class AntecedenteCreate(AntecedenteBase):
    pass

class AntecedenteUpdate(BaseModel):
    tipo: Optional[TipoAntecedenteEnum] = None
    descripcion: Optional[str] = None
    activo: Optional[bool] = None

class AntecedenteResponse(AntecedenteBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/antecedentes",
    tags=["Antecedentes"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=AntecedenteResponse, status_code=status.HTTP_201_CREATED)
def crear_antecedente(antecedente: AntecedenteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo antecedente"""
    
    # Verificar que el paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == antecedente.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    db_antecedente = Antecedente(**antecedente.model_dump())
    db.add(db_antecedente)
    db.commit()
    db.refresh(db_antecedente)
    
    return db_antecedente

@router.get("/paciente/{paciente_id}", response_model=List[AntecedenteResponse])
def listar_antecedentes_paciente(
    paciente_id: int,
    tipo: Optional[TipoAntecedenteEnum] = None,
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar antecedentes de un paciente"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    query = db.query(Antecedente).filter(
        Antecedente.paciente_id == paciente_id,
        Antecedente.activo == activo
    )
    
    if tipo:
        query = query.filter(Antecedente.tipo == tipo)
    
    antecedentes = query.all()
    return antecedentes

@router.get("/{antecedente_id}", response_model=AntecedenteResponse)
def obtener_antecedente(antecedente_id: int, db: Session = Depends(get_db)):
    """Obtener un antecedente por ID"""
    
    antecedente = db.query(Antecedente).filter(Antecedente.id == antecedente_id).first()
    if not antecedente:
        raise HTTPException(status_code=404, detail="Antecedente no encontrado")
    
    return antecedente

@router.put("/{antecedente_id}", response_model=AntecedenteResponse)
def actualizar_antecedente(
    antecedente_id: int,
    antecedente_update: AntecedenteUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un antecedente"""
    
    antecedente = db.query(Antecedente).filter(Antecedente.id == antecedente_id).first()
    if not antecedente:
        raise HTTPException(status_code=404, detail="Antecedente no encontrado")
    
    update_data = antecedente_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(antecedente, field, value)
    
    db.commit()
    db.refresh(antecedente)
    
    return antecedente

@router.delete("/{antecedente_id}", status_code=status.HTTP_204_NO_CONTENT)
def desactivar_antecedente(antecedente_id: int, db: Session = Depends(get_db)):
    """Desactivar un antecedente"""
    
    antecedente = db.query(Antecedente).filter(Antecedente.id == antecedente_id).first()
    if not antecedente:
        raise HTTPException(status_code=404, detail="Antecedente no encontrado")
    
    antecedente.activo = False
    db.commit()
    
    return None