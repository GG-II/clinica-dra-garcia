from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime, date
from pydantic import BaseModel
import json
from create_simple_tables import (
    TipoEstudio, ResultadoLaboratorio, CategoriaLaboratorioEnum, 
    Paciente, Consulta
)

# ============================================================================
# SCHEMAS
# ============================================================================

class TipoEstudioBase(BaseModel):
    nombre: str
    categoria: CategoriaLaboratorioEnum
    descripcion: Optional[str] = None

class TipoEstudioCreate(TipoEstudioBase):
    pass

class TipoEstudioResponse(TipoEstudioBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

class ResultadoLaboratorioBase(BaseModel):
    paciente_id: int
    consulta_id: Optional[int] = None
    tipo_estudio_id: int
    fecha_toma: datetime
    resultado: str  # JSON string
    valor_minimo: Optional[str] = None
    valor_maximo: Optional[str] = None
    unidad: Optional[str] = None
    valor_critico: bool = False
    laboratorio_externo: Optional[str] = None
    observaciones: Optional[str] = None

class ResultadoLaboratorioCreate(ResultadoLaboratorioBase):
    pass

class ResultadoLaboratorioResponse(ResultadoLaboratorioBase):
    id: int
    fecha_resultado: datetime
    tipo_estudio_nombre: Optional[str] = None
    categoria: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/laboratorios",
    tags=["Laboratorios"]
)

# ============================================================================
# ENDPOINTS - TIPOS DE ESTUDIO
# ============================================================================

@router.post("/tipos-estudio", response_model=TipoEstudioResponse, status_code=status.HTTP_201_CREATED)
def crear_tipo_estudio(tipo: TipoEstudioCreate, db: Session = Depends(get_db)):
    """Crear un nuevo tipo de estudio"""
    
    db_tipo = TipoEstudio(**tipo.model_dump())
    db.add(db_tipo)
    db.commit()
    db.refresh(db_tipo)
    
    return db_tipo

@router.get("/tipos-estudio", response_model=List[TipoEstudioResponse])
def listar_tipos_estudio(
    categoria: Optional[CategoriaLaboratorioEnum] = None,
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar tipos de estudio"""
    
    query = db.query(TipoEstudio).filter(TipoEstudio.activo == activo)
    
    if categoria:
        query = query.filter(TipoEstudio.categoria == categoria)
    
    return query.all()

# ============================================================================
# ENDPOINTS - RESULTADOS
# ============================================================================

@router.post("/resultados", response_model=ResultadoLaboratorioResponse, status_code=status.HTTP_201_CREATED)
def crear_resultado(resultado: ResultadoLaboratorioCreate, db: Session = Depends(get_db)):
    """Registrar resultado de laboratorio"""
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == resultado.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar tipo de estudio
    tipo = db.query(TipoEstudio).filter(TipoEstudio.id == resultado.tipo_estudio_id).first()
    if not tipo:
        raise HTTPException(status_code=404, detail="Tipo de estudio no encontrado")
    
    db_resultado = ResultadoLaboratorio(**resultado.model_dump())
    db.add(db_resultado)
    db.commit()
    db.refresh(db_resultado)
    
    response = ResultadoLaboratorioResponse.model_validate(db_resultado)
    response.tipo_estudio_nombre = tipo.nombre
    response.categoria = tipo.categoria.value
    
    return response

@router.get("/resultados/paciente/{paciente_id}", response_model=List[ResultadoLaboratorioResponse])
def listar_resultados_paciente(
    paciente_id: int,
    tipo_estudio_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar resultados de laboratorio de un paciente"""
    
    query = db.query(ResultadoLaboratorio).filter(ResultadoLaboratorio.paciente_id == paciente_id)
    
    if tipo_estudio_id:
        query = query.filter(ResultadoLaboratorio.tipo_estudio_id == tipo_estudio_id)
    
    resultados = query.order_by(ResultadoLaboratorio.fecha_resultado.desc()).all()
    
    result = []
    for res in resultados:
        tipo = db.query(TipoEstudio).filter(TipoEstudio.id == res.tipo_estudio_id).first()
        response = ResultadoLaboratorioResponse.model_validate(res)
        if tipo:
            response.tipo_estudio_nombre = tipo.nombre
            response.categoria = tipo.categoria.value
        result.append(response)
    
    return result

@router.get("/resultados/{resultado_id}", response_model=ResultadoLaboratorioResponse)
def obtener_resultado(resultado_id: int, db: Session = Depends(get_db)):
    """Obtener un resultado específico"""
    
    resultado = db.query(ResultadoLaboratorio).filter(ResultadoLaboratorio.id == resultado_id).first()
    if not resultado:
        raise HTTPException(status_code=404, detail="Resultado no encontrado")
    
    tipo = db.query(TipoEstudio).filter(TipoEstudio.id == resultado.tipo_estudio_id).first()
    response = ResultadoLaboratorioResponse.model_validate(resultado)
    if tipo:
        response.tipo_estudio_nombre = tipo.nombre
        response.categoria = tipo.categoria.value
    
    return response

@router.get("/resultados/criticos/paciente/{paciente_id}", response_model=List[ResultadoLaboratorioResponse])
def listar_valores_criticos(paciente_id: int, db: Session = Depends(get_db)):
    """Listar valores críticos de un paciente"""
    
    resultados = db.query(ResultadoLaboratorio).filter(
        ResultadoLaboratorio.paciente_id == paciente_id,
        ResultadoLaboratorio.valor_critico == True
    ).order_by(ResultadoLaboratorio.fecha_resultado.desc()).all()
    
    result = []
    for res in resultados:
        tipo = db.query(TipoEstudio).filter(TipoEstudio.id == res.tipo_estudio_id).first()
        response = ResultadoLaboratorioResponse.model_validate(res)
        if tipo:
            response.tipo_estudio_nombre = tipo.nombre
            response.categoria = tipo.categoria.value
        result.append(response)
    
    return result