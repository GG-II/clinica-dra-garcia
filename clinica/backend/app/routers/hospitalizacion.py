from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime
from pydantic import BaseModel
from create_simple_tables import Hospitalizacion, Cama, Paciente, Usuario, EstadoCamaEnum

# ============================================================================
# SCHEMAS
# ============================================================================

class CamaBase(BaseModel):
    numero: int
    estado: EstadoCamaEnum
    ubicacion: Optional[str] = None

class CamaResponse(CamaBase):
    id: int
    paciente_actual: Optional[str] = None  # Nombre del paciente si está ocupada

    class Config:
        from_attributes = True

class HospitalizacionBase(BaseModel):
    paciente_id: int
    medico_responsable_id: int
    cama_id: int
    diagnostico_ingreso: str
    motivo: str

class HospitalizacionCreate(HospitalizacionBase):
    pass

class HospitalizacionUpdate(BaseModel):
    medico_responsable_id: Optional[int] = None
    cama_id: Optional[int] = None
    diagnostico_ingreso: Optional[str] = None
    motivo: Optional[str] = None
    fecha_egreso: Optional[datetime] = None
    activa: Optional[bool] = None

class HospitalizacionResponse(HospitalizacionBase):
    id: int
    fecha_ingreso: datetime
    fecha_egreso: Optional[datetime]
    activa: bool
    
    # Información adicional
    paciente_nombre: Optional[str] = None
    medico_nombre: Optional[str] = None
    cama_numero: Optional[int] = None
    dias_hospitalizacion: Optional[int] = None

    class Config:
        from_attributes = True

class EstadisticasHospitalizacion(BaseModel):
    total_camas: int
    camas_ocupadas: int
    camas_disponibles: int
    camas_limpieza: int
    camas_mantenimiento: int
    porcentaje_ocupacion: float
    hospitalizaciones_activas: int

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/hospitalizacion",
    tags=["Hospitalización"]
)

# ============================================================================
# ENDPOINTS DE CAMAS
# ============================================================================

@router.get("/camas", response_model=List[CamaResponse])
def listar_camas(db: Session = Depends(get_db)):
    """Listar todas las camas con su estado actual"""
    
    camas = db.query(Cama).order_by(Cama.numero).all()
    
    result = []
    for cama in camas:
        response = CamaResponse.model_validate(cama)
        
        # Si la cama está ocupada, obtener nombre del paciente
        if cama.estado == EstadoCamaEnum.ocupada:
            hospitalizacion = db.query(Hospitalizacion).filter(
                Hospitalizacion.cama_id == cama.id,
                Hospitalizacion.activa == True
            ).first()
            
            if hospitalizacion:
                paciente = db.query(Paciente).filter(Paciente.id == hospitalizacion.paciente_id).first()
                if paciente:
                    response.paciente_actual = f"{paciente.nombres} {paciente.apellidos}"
        
        result.append(response)
    
    return result

@router.get("/camas/disponibles", response_model=List[CamaResponse])
def listar_camas_disponibles(db: Session = Depends(get_db)):
    """Listar solo las camas disponibles"""
    
    camas = db.query(Cama).filter(Cama.estado == EstadoCamaEnum.disponible).order_by(Cama.numero).all()
    return [CamaResponse.model_validate(c) for c in camas]

@router.put("/camas/{cama_id}/estado")
def cambiar_estado_cama(
    cama_id: int,
    nuevo_estado: EstadoCamaEnum,
    db: Session = Depends(get_db)
):
    """Cambiar el estado de una cama (limpieza, mantenimiento, disponible)"""
    
    cama = db.query(Cama).filter(Cama.id == cama_id).first()
    if not cama:
        raise HTTPException(status_code=404, detail="Cama no encontrada")
    
    # No permitir cambiar a ocupada manualmente
    if nuevo_estado == EstadoCamaEnum.ocupada:
        raise HTTPException(
            status_code=400,
            detail="No se puede marcar una cama como ocupada manualmente. Use el endpoint de ingreso hospitalario."
        )
    
    # Verificar que la cama no esté ocupada
    if cama.estado == EstadoCamaEnum.ocupada:
        raise HTTPException(
            status_code=400,
            detail="No se puede cambiar el estado de una cama ocupada"
        )
    
    cama.estado = nuevo_estado
    db.commit()
    
    return {"message": f"Estado de cama {cama.numero} actualizado a {nuevo_estado.value}"}

# ============================================================================
# ENDPOINTS DE HOSPITALIZACIÓN
# ============================================================================

@router.post("/ingresos", response_model=HospitalizacionResponse, status_code=status.HTTP_201_CREATED)
def crear_ingreso_hospitalario(ingreso: HospitalizacionCreate, db: Session = Depends(get_db)):
    """Ingresar un paciente a hospitalización"""
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == ingreso.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Verificar médico
    medico = db.query(Usuario).filter(Usuario.id == ingreso.medico_responsable_id).first()
    if not medico:
        raise HTTPException(status_code=404, detail="Médico no encontrado")
    
    # Verificar cama
    cama = db.query(Cama).filter(Cama.id == ingreso.cama_id).first()
    if not cama:
        raise HTTPException(status_code=404, detail="Cama no encontrada")
    
    # Verificar que la cama esté disponible
    if cama.estado != EstadoCamaEnum.disponible:
        raise HTTPException(
            status_code=400,
            detail=f"La cama {cama.numero} no está disponible. Estado actual: {cama.estado.value}"
        )
    
    # Verificar que el paciente no esté ya hospitalizado
    hospitalizado = db.query(Hospitalizacion).filter(
        Hospitalizacion.paciente_id == ingreso.paciente_id,
        Hospitalizacion.activa == True
    ).first()
    
    if hospitalizado:
        raise HTTPException(
            status_code=400,
            detail="El paciente ya tiene una hospitalización activa"
        )
    
    # Crear hospitalización
    db_hospitalizacion = Hospitalizacion(**ingreso.model_dump())
    db.add(db_hospitalizacion)
    
    # Cambiar estado de la cama a ocupada
    cama.estado = EstadoCamaEnum.ocupada
    
    db.commit()
    db.refresh(db_hospitalizacion)
    
    response = HospitalizacionResponse.model_validate(db_hospitalizacion)
    response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    response.cama_numero = cama.numero
    
    return response

@router.get("/ingresos", response_model=List[HospitalizacionResponse])
def listar_hospitalizaciones(
    skip: int = 0,
    limit: int = 100,
    activa: Optional[bool] = None,
    paciente_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Listar hospitalizaciones con filtros opcionales"""
    
    query = db.query(Hospitalizacion)
    
    if activa is not None:
        query = query.filter(Hospitalizacion.activa == activa)
    
    if paciente_id:
        query = query.filter(Hospitalizacion.paciente_id == paciente_id)
    
    hospitalizaciones = query.order_by(Hospitalizacion.fecha_ingreso.desc()).offset(skip).limit(limit).all()
    
    result = []
    for hosp in hospitalizaciones:
        response = HospitalizacionResponse.model_validate(hosp)
        
        # Agregar información adicional
        paciente = db.query(Paciente).filter(Paciente.id == hosp.paciente_id).first()
        medico = db.query(Usuario).filter(Usuario.id == hosp.medico_responsable_id).first()
        cama = db.query(Cama).filter(Cama.id == hosp.cama_id).first()
        
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        if cama:
            response.cama_numero = cama.numero
        
        # Calcular días de hospitalización
        if hosp.activa:
            response.dias_hospitalizacion = (datetime.now() - hosp.fecha_ingreso).days
        elif hosp.fecha_egreso:
            response.dias_hospitalizacion = (hosp.fecha_egreso - hosp.fecha_ingreso).days
        
        result.append(response)
    
    return result

@router.get("/ingresos/activos", response_model=List[HospitalizacionResponse])
def listar_hospitalizaciones_activas(db: Session = Depends(get_db)):
    """Listar solo las hospitalizaciones activas"""
    
    hospitalizaciones = db.query(Hospitalizacion).filter(
        Hospitalizacion.activa == True
    ).order_by(Hospitalizacion.fecha_ingreso.desc()).all()
    
    result = []
    for hosp in hospitalizaciones:
        response = HospitalizacionResponse.model_validate(hosp)
        
        paciente = db.query(Paciente).filter(Paciente.id == hosp.paciente_id).first()
        medico = db.query(Usuario).filter(Usuario.id == hosp.medico_responsable_id).first()
        cama = db.query(Cama).filter(Cama.id == hosp.cama_id).first()
        
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        if cama:
            response.cama_numero = cama.numero
        
        response.dias_hospitalizacion = (datetime.now() - hosp.fecha_ingreso).days
        
        result.append(response)
    
    return result

@router.get("/ingresos/{hospitalizacion_id}", response_model=HospitalizacionResponse)
def obtener_hospitalizacion(hospitalizacion_id: int, db: Session = Depends(get_db)):
    """Obtener una hospitalización por ID"""
    
    hosp = db.query(Hospitalizacion).filter(Hospitalizacion.id == hospitalizacion_id).first()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalización no encontrada")
    
    response = HospitalizacionResponse.model_validate(hosp)
    
    paciente = db.query(Paciente).filter(Paciente.id == hosp.paciente_id).first()
    medico = db.query(Usuario).filter(Usuario.id == hosp.medico_responsable_id).first()
    cama = db.query(Cama).filter(Cama.id == hosp.cama_id).first()
    
    if paciente:
        response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    if medico:
        response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    if cama:
        response.cama_numero = cama.numero
    
    if hosp.activa:
        response.dias_hospitalizacion = (datetime.now() - hosp.fecha_ingreso).days
    elif hosp.fecha_egreso:
        response.dias_hospitalizacion = (hosp.fecha_egreso - hosp.fecha_ingreso).days
    
    return response

@router.put("/ingresos/{hospitalizacion_id}", response_model=HospitalizacionResponse)
def actualizar_hospitalizacion(
    hospitalizacion_id: int,
    hospitalizacion_update: HospitalizacionUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar datos de una hospitalización"""
    
    hosp = db.query(Hospitalizacion).filter(Hospitalizacion.id == hospitalizacion_id).first()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalización no encontrada")
    
    update_data = hospitalizacion_update.model_dump(exclude_unset=True)
    
    # Si se está cambiando de cama
    if 'cama_id' in update_data and update_data['cama_id'] != hosp.cama_id:
        nueva_cama = db.query(Cama).filter(Cama.id == update_data['cama_id']).first()
        if not nueva_cama:
            raise HTTPException(status_code=404, detail="Nueva cama no encontrada")
        
        if nueva_cama.estado != EstadoCamaEnum.disponible:
            raise HTTPException(
                status_code=400,
                detail=f"La cama {nueva_cama.numero} no está disponible"
            )
        
        # Liberar cama anterior
        cama_anterior = db.query(Cama).filter(Cama.id == hosp.cama_id).first()
        if cama_anterior:
            cama_anterior.estado = EstadoCamaEnum.limpieza
        
        # Ocupar nueva cama
        nueva_cama.estado = EstadoCamaEnum.ocupada
    
    for field, value in update_data.items():
        setattr(hosp, field, value)
    
    db.commit()
    db.refresh(hosp)
    
    return hosp

@router.post("/ingresos/{hospitalizacion_id}/egreso")
def dar_egreso(hospitalizacion_id: int, db: Session = Depends(get_db)):
    """Dar egreso a un paciente hospitalizado"""
    
    hosp = db.query(Hospitalizacion).filter(Hospitalizacion.id == hospitalizacion_id).first()
    if not hosp:
        raise HTTPException(status_code=404, detail="Hospitalización no encontrada")
    
    if not hosp.activa:
        raise HTTPException(
            status_code=400,
            detail="La hospitalización ya está cerrada"
        )
    
    # Registrar egreso
    hosp.fecha_egreso = datetime.now()
    hosp.activa = False
    
    # Liberar cama
    cama = db.query(Cama).filter(Cama.id == hosp.cama_id).first()
    if cama:
        cama.estado = EstadoCamaEnum.limpieza
    
    db.commit()
    
    dias = (hosp.fecha_egreso - hosp.fecha_ingreso).days
    
    return {
        "message": "Egreso registrado exitosamente",
        "fecha_egreso": hosp.fecha_egreso,
        "dias_hospitalizacion": dias
    }

@router.get("/estadisticas", response_model=EstadisticasHospitalizacion)
def obtener_estadisticas_hospitalizacion(db: Session = Depends(get_db)):
    """Obtener estadísticas de hospitalización"""
    
    total_camas = db.query(Cama).count()
    
    camas_ocupadas = db.query(Cama).filter(Cama.estado == EstadoCamaEnum.ocupada).count()
    camas_disponibles = db.query(Cama).filter(Cama.estado == EstadoCamaEnum.disponible).count()
    camas_limpieza = db.query(Cama).filter(Cama.estado == EstadoCamaEnum.limpieza).count()
    camas_mantenimiento = db.query(Cama).filter(Cama.estado == EstadoCamaEnum.mantenimiento).count()
    
    porcentaje_ocupacion = (camas_ocupadas / total_camas * 100) if total_camas > 0 else 0
    
    hospitalizaciones_activas = db.query(Hospitalizacion).filter(Hospitalizacion.activa == True).count()
    
    return {
        "total_camas": total_camas,
        "camas_ocupadas": camas_ocupadas,
        "camas_disponibles": camas_disponibles,
        "camas_limpieza": camas_limpieza,
        "camas_mantenimiento": camas_mantenimiento,
        "porcentaje_ocupacion": round(porcentaje_ocupacion, 2),
        "hospitalizaciones_activas": hospitalizaciones_activas
    }