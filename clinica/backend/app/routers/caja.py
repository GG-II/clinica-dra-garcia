from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime, date
from pydantic import BaseModel
from sqlalchemy import func
from create_simple_tables import (
    Caja, MovimientoCaja, CuentaPorCobrar, Cotizacion,
    TipoMovimientoEnum, TipoIngresoEnum, TipoEgresoEnum,
    Usuario, Paciente
)

# ============================================================================
# SCHEMAS - CAJA
# ============================================================================

class CajaBase(BaseModel):
    monto_inicial: float

class CajaCreate(CajaBase):
    usuario_id: int

class CajaResponse(CajaBase):
    id: int
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime]
    usuario_id: int
    monto_final: Optional[float]
    total_ingresos: Optional[float]
    total_egresos: Optional[float]
    diferencia: Optional[float]
    cerrada: bool
    usuario_nombre: Optional[str] = None

    class Config:
        from_attributes = True

class CajaCierre(BaseModel):
    monto_final: float

# ============================================================================
# SCHEMAS - MOVIMIENTOS
# ============================================================================

class MovimientoCajaBase(BaseModel):
    caja_id: int
    tipo_movimiento: TipoMovimientoEnum
    concepto: str
    monto: float
    forma_pago: str
    numero_documento: Optional[str] = None
    usuario_id: int
    
    # Para ingresos
    tipo_ingreso: Optional[TipoIngresoEnum] = None
    paciente_id: Optional[int] = None
    
    # Para egresos
    tipo_egreso: Optional[TipoEgresoEnum] = None
    proveedor: Optional[str] = None

class MovimientoCajaCreate(MovimientoCajaBase):
    pass

class MovimientoCajaResponse(MovimientoCajaBase):
    id: int
    fecha_hora: datetime
    paciente_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# SCHEMAS - CUENTAS POR COBRAR
# ============================================================================

class CuentaPorCobrarBase(BaseModel):
    paciente_id: Optional[int] = None
    convenio: Optional[str] = None
    concepto: str
    monto_total: float
    fecha_emision: date
    fecha_vencimiento: Optional[date] = None
    observaciones: Optional[str] = None

class CuentaPorCobrarCreate(CuentaPorCobrarBase):
    pass

class CuentaPorCobrarUpdate(BaseModel):
    monto_pagado: float

class CuentaPorCobrarResponse(CuentaPorCobrarBase):
    id: int
    monto_pagado: float
    saldo: float
    pagado: bool
    paciente_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# SCHEMAS - COTIZACIONES
# ============================================================================

class CotizacionBase(BaseModel):
    paciente_id: int
    medico_id: Optional[int] = None
    vigencia_dias: int = 30
    servicios: str  # JSON
    total: float
    condiciones: Optional[str] = None

class CotizacionCreate(CotizacionBase):
    pass

class CotizacionResponse(CotizacionBase):
    id: int
    fecha: datetime
    aceptada: bool
    paciente_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/caja",
    tags=["Caja y Facturación"]
)

# ============================================================================
# ENDPOINTS - CAJA
# ============================================================================

@router.post("/apertura", response_model=CajaResponse, status_code=status.HTTP_201_CREATED)
def abrir_caja(caja: CajaCreate, db: Session = Depends(get_db)):
    """Abrir caja al inicio del día"""
    
    # Verificar que no haya una caja abierta
    caja_abierta = db.query(Caja).filter(Caja.cerrada == False).first()
    if caja_abierta:
        raise HTTPException(
            status_code=400,
            detail="Ya existe una caja abierta. Debe cerrarla antes de abrir una nueva."
        )
    
    # Verificar usuario
    usuario = db.query(Usuario).filter(Usuario.id == caja.usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_caja = Caja(**caja.model_dump())
    db.add(db_caja)
    db.commit()
    db.refresh(db_caja)
    
    response = CajaResponse.model_validate(db_caja)
    response.usuario_nombre = f"{usuario.nombres} {usuario.apellidos}"
    
    return response

@router.get("/actual", response_model=CajaResponse)
def obtener_caja_actual(db: Session = Depends(get_db)):
    """Obtener la caja abierta actualmente"""
    
    caja = db.query(Caja).filter(Caja.cerrada == False).first()
    if not caja:
        raise HTTPException(status_code=404, detail="No hay una caja abierta")
    
    usuario = db.query(Usuario).filter(Usuario.id == caja.usuario_id).first()
    response = CajaResponse.model_validate(caja)
    if usuario:
        response.usuario_nombre = f"{usuario.nombres} {usuario.apellidos}"
    
    return response

@router.post("/cierre/{caja_id}", response_model=CajaResponse)
def cerrar_caja(caja_id: int, cierre: CajaCierre, db: Session = Depends(get_db)):
    """Cerrar caja al final del día"""
    
    caja = db.query(Caja).filter(Caja.id == caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    
    if caja.cerrada:
        raise HTTPException(status_code=400, detail="La caja ya está cerrada")
    
    # Calcular totales
    ingresos = db.query(func.sum(MovimientoCaja.monto)).filter(
        MovimientoCaja.caja_id == caja_id,
        MovimientoCaja.tipo_movimiento == TipoMovimientoEnum.ingreso
    ).scalar() or 0
    
    egresos = db.query(func.sum(MovimientoCaja.monto)).filter(
        MovimientoCaja.caja_id == caja_id,
        MovimientoCaja.tipo_movimiento == TipoMovimientoEnum.egreso
    ).scalar() or 0
    
    caja.fecha_cierre = datetime.now()
    caja.monto_final = cierre.monto_final
    caja.total_ingresos = ingresos
    caja.total_egresos = egresos
    caja.diferencia = (caja.monto_inicial + ingresos - egresos) - cierre.monto_final
    caja.cerrada = True
    
    db.commit()
    db.refresh(caja)
    
    return caja

@router.get("/historial", response_model=List[CajaResponse])
def listar_cajas(
    skip: int = 0,
    limit: int = 100,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Listar historial de cajas"""
    
    query = db.query(Caja)
    
    if fecha_desde:
        query = query.filter(func.date(Caja.fecha_apertura) >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(func.date(Caja.fecha_apertura) <= fecha_hasta)
    
    cajas = query.order_by(Caja.fecha_apertura.desc()).offset(skip).limit(limit).all()
    
    result = []
    for caja in cajas:
        usuario = db.query(Usuario).filter(Usuario.id == caja.usuario_id).first()
        response = CajaResponse.model_validate(caja)
        if usuario:
            response.usuario_nombre = f"{usuario.nombres} {usuario.apellidos}"
        result.append(response)
    
    return result

# ============================================================================
# ENDPOINTS - MOVIMIENTOS
# ============================================================================

@router.post("/movimientos", response_model=MovimientoCajaResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimiento(movimiento: MovimientoCajaCreate, db: Session = Depends(get_db)):
    """Registrar un movimiento de caja (ingreso o egreso)"""
    
    # Verificar que la caja existe y está abierta
    caja = db.query(Caja).filter(Caja.id == movimiento.caja_id).first()
    if not caja:
        raise HTTPException(status_code=404, detail="Caja no encontrada")
    
    if caja.cerrada:
        raise HTTPException(status_code=400, detail="No se pueden registrar movimientos en una caja cerrada")
    
    db_movimiento = MovimientoCaja(**movimiento.model_dump())
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    
    response = MovimientoCajaResponse.model_validate(db_movimiento)
    
    if db_movimiento.paciente_id:
        paciente = db.query(Paciente).filter(Paciente.id == db_movimiento.paciente_id).first()
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    
    return response

@router.get("/movimientos/caja/{caja_id}", response_model=List[MovimientoCajaResponse])
def listar_movimientos_caja(caja_id: int, db: Session = Depends(get_db)):
    """Listar movimientos de una caja"""
    
    movimientos = db.query(MovimientoCaja).filter(
        MovimientoCaja.caja_id == caja_id
    ).order_by(MovimientoCaja.fecha_hora.desc()).all()
    
    result = []
    for mov in movimientos:
        response = MovimientoCajaResponse.model_validate(mov)
        if mov.paciente_id:
            paciente = db.query(Paciente).filter(Paciente.id == mov.paciente_id).first()
            if paciente:
                response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        result.append(response)
    
    return result

# ============================================================================
# ENDPOINTS - CUENTAS POR COBRAR
# ============================================================================

@router.post("/cuentas-por-cobrar", response_model=CuentaPorCobrarResponse, status_code=status.HTTP_201_CREATED)
def crear_cuenta_por_cobrar(cuenta: CuentaPorCobrarCreate, db: Session = Depends(get_db)):
    """Crear una cuenta por cobrar"""
    
    db_cuenta = CuentaPorCobrar(**cuenta.model_dump())
    db_cuenta.saldo = cuenta.monto_total
    db.add(db_cuenta)
    db.commit()
    db.refresh(db_cuenta)
    
    response = CuentaPorCobrarResponse.model_validate(db_cuenta)
    
    if db_cuenta.paciente_id:
        paciente = db.query(Paciente).filter(Paciente.id == db_cuenta.paciente_id).first()
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    
    return response

@router.get("/cuentas-por-cobrar", response_model=List[CuentaPorCobrarResponse])
def listar_cuentas_por_cobrar(
    paciente_id: Optional[int] = None,
    pagado: Optional[bool] = None,
    vencidas: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar cuentas por cobrar"""
    
    query = db.query(CuentaPorCobrar)
    
    if paciente_id:
        query = query.filter(CuentaPorCobrar.paciente_id == paciente_id)
    
    if pagado is not None:
        query = query.filter(CuentaPorCobrar.pagado == pagado)
    
    if vencidas:
        hoy = date.today()
        query = query.filter(
            CuentaPorCobrar.fecha_vencimiento < hoy,
            CuentaPorCobrar.pagado == False
        )
    
    cuentas = query.order_by(CuentaPorCobrar.fecha_emision.desc()).all()
    
    result = []
    for cuenta in cuentas:
        response = CuentaPorCobrarResponse.model_validate(cuenta)
        if cuenta.paciente_id:
            paciente = db.query(Paciente).filter(Paciente.id == cuenta.paciente_id).first()
            if paciente:
                response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        result.append(response)
    
    return result

@router.put("/cuentas-por-cobrar/{cuenta_id}/abonar", response_model=CuentaPorCobrarResponse)
def abonar_cuenta(
    cuenta_id: int,
    abono: CuentaPorCobrarUpdate,
    db: Session = Depends(get_db)
):
    """Registrar abono a cuenta por cobrar"""
    
    cuenta = db.query(CuentaPorCobrar).filter(CuentaPorCobrar.id == cuenta_id).first()
    if not cuenta:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    
    if cuenta.pagado:
        raise HTTPException(status_code=400, detail="La cuenta ya está pagada")
    
    cuenta.monto_pagado += abono.monto_pagado
    cuenta.saldo = cuenta.monto_total - cuenta.monto_pagado
    
    if cuenta.saldo <= 0:
        cuenta.pagado = True
        cuenta.saldo = 0
    
    db.commit()
    db.refresh(cuenta)
    
    return cuenta

# ============================================================================
# ENDPOINTS - COTIZACIONES
# ============================================================================

@router.post("/cotizaciones", response_model=CotizacionResponse, status_code=status.HTTP_201_CREATED)
def crear_cotizacion(cotizacion: CotizacionCreate, db: Session = Depends(get_db)):
    """Crear una cotización"""
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == cotizacion.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    db_cotizacion = Cotizacion(**cotizacion.model_dump())
    db.add(db_cotizacion)
    db.commit()
    db.refresh(db_cotizacion)
    
    response = CotizacionResponse.model_validate(db_cotizacion)
    response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    
    return response

@router.get("/cotizaciones", response_model=List[CotizacionResponse])
def listar_cotizaciones(
    paciente_id: Optional[int] = None,
    aceptada: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Listar cotizaciones"""
    
    query = db.query(Cotizacion)
    
    if paciente_id:
        query = query.filter(Cotizacion.paciente_id == paciente_id)
    
    if aceptada is not None:
        query = query.filter(Cotizacion.aceptada == aceptada)
    
    cotizaciones = query.order_by(Cotizacion.fecha.desc()).all()
    
    result = []
    for cot in cotizaciones:
        paciente = db.query(Paciente).filter(Paciente.id == cot.paciente_id).first()
        response = CotizacionResponse.model_validate(cot)
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        result.append(response)
    
    return result

@router.put("/cotizaciones/{cotizacion_id}/aceptar")
def aceptar_cotizacion(cotizacion_id: int, db: Session = Depends(get_db)):
    """Marcar cotización como aceptada"""
    
    cotizacion = db.query(Cotizacion).filter(Cotizacion.id == cotizacion_id).first()
    if not cotizacion:
        raise HTTPException(status_code=404, detail="Cotización no encontrada")
    
    cotizacion.aceptada = True
    db.commit()
    
    return {"message": "Cotización aceptada"}