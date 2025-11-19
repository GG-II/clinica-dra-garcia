from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import datetime, date, timedelta
from pydantic import BaseModel
from sqlalchemy import func
from create_simple_tables import (
    Proveedor, ProductoFarmacia, MovimientoInventario, CompraFarmacia,
    DetalleCompra, VentaFarmacia, DetalleVenta,
    TipoMovimientoInventarioEnum, Paciente, Usuario, Receta, Medicamento
)

# ============================================================================
# SCHEMAS - PROVEEDORES
# ============================================================================

class ProveedorBase(BaseModel):
    nombre: str
    nit: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    contacto: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorResponse(ProveedorBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

# ============================================================================
# SCHEMAS - PRODUCTOS
# ============================================================================

class ProductoFarmaciaBase(BaseModel):
    medicamento_id: Optional[int] = None
    codigo_interno: Optional[str] = None
    nombre: str
    tipo: Optional[str] = None
    presentacion: Optional[str] = None
    lote: Optional[str] = None
    fecha_vencimiento: Optional[date] = None
    proveedor_id: Optional[int] = None
    stock_actual: int = 0
    stock_minimo: int = 10
    precio_compra: float
    precio_venta: float
    ubicacion: Optional[str] = None

class ProductoFarmaciaCreate(ProductoFarmaciaBase):
    pass

class ProductoFarmaciaUpdate(BaseModel):
    nombre: Optional[str] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None
    precio_compra: Optional[float] = None
    precio_venta: Optional[float] = None
    ubicacion: Optional[str] = None
    activo: Optional[bool] = None

class ProductoFarmaciaResponse(ProductoFarmaciaBase):
    id: int
    activo: bool
    created_at: datetime
    alerta_stock: bool = False
    alerta_vencimiento: bool = False

    class Config:
        from_attributes = True

# ============================================================================
# SCHEMAS - MOVIMIENTOS INVENTARIO
# ============================================================================

class MovimientoInventarioBase(BaseModel):
    producto_id: int
    tipo: TipoMovimientoInventarioEnum
    cantidad: int
    motivo: str
    usuario_id: int

class MovimientoInventarioCreate(MovimientoInventarioBase):
    pass

class MovimientoInventarioResponse(MovimientoInventarioBase):
    id: int
    stock_anterior: int
    stock_nuevo: int
    fecha_hora: datetime
    producto_nombre: Optional[str] = None

    class Config:
        from_attributes = True

# ============================================================================
# SCHEMAS - COMPRAS
# ============================================================================

class DetalleCompraBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetalleCompraCreate(DetalleCompraBase):
    pass

class DetalleCompraResponse(DetalleCompraBase):
    id: int
    compra_id: int
    subtotal: float
    producto_nombre: Optional[str] = None

    class Config:
        from_attributes = True

class CompraFarmaciaBase(BaseModel):
    proveedor_id: int
    fecha_compra: date
    numero_factura: Optional[str] = None
    observaciones: Optional[str] = None

class CompraFarmaciaCreate(CompraFarmaciaBase):
    usuario_id: int
    productos: List[DetalleCompraCreate]

class CompraFarmaciaResponse(CompraFarmaciaBase):
    id: int
    total: float
    usuario_id: int
    created_at: datetime
    proveedor_nombre: Optional[str] = None
    productos: List[DetalleCompraResponse] = []

    class Config:
        from_attributes = True

# ============================================================================
# SCHEMAS - VENTAS
# ============================================================================

class DetalleVentaBase(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetalleVentaCreate(DetalleVentaBase):
    pass

class DetalleVentaResponse(DetalleVentaBase):
    id: int
    venta_id: int
    subtotal: float
    producto_nombre: Optional[str] = None

    class Config:
        from_attributes = True

class VentaFarmaciaBase(BaseModel):
    paciente_id: Optional[int] = None
    receta_id: Optional[int] = None
    descuento: float = 0

class VentaFarmaciaCreate(VentaFarmaciaBase):
    usuario_id: int
    productos: List[DetalleVentaCreate]

class VentaFarmaciaResponse(VentaFarmaciaBase):
    id: int
    fecha_venta: datetime
    total: float
    total_final: float
    usuario_id: int
    paciente_nombre: Optional[str] = None
    productos: List[DetalleVentaResponse] = []

    class Config:
        from_attributes = True

class EstadisticasFarmacia(BaseModel):
    total_productos: int
    productos_stock_bajo: int
    productos_por_vencer: int
    valor_inventario: float

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/farmacia",
    tags=["Farmacia e Inventario"]
)

# ============================================================================
# ENDPOINTS - PROVEEDORES
# ============================================================================

@router.post("/proveedores", response_model=ProveedorResponse, status_code=status.HTTP_201_CREATED)
def crear_proveedor(proveedor: ProveedorCreate, db: Session = Depends(get_db)):
    """Crear un nuevo proveedor"""
    
    db_proveedor = Proveedor(**proveedor.model_dump())
    db.add(db_proveedor)
    db.commit()
    db.refresh(db_proveedor)
    
    return db_proveedor

@router.get("/proveedores", response_model=List[ProveedorResponse])
def listar_proveedores(activo: bool = True, db: Session = Depends(get_db)):
    """Listar proveedores"""
    
    return db.query(Proveedor).filter(Proveedor.activo == activo).all()

# ============================================================================
# ENDPOINTS - PRODUCTOS
# ============================================================================

@router.post("/productos", response_model=ProductoFarmaciaResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoFarmaciaCreate, db: Session = Depends(get_db)):
    """Crear un nuevo producto en farmacia"""
    
    db_producto = ProductoFarmacia(**producto.model_dump())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    
    return db_producto

@router.get("/productos", response_model=List[ProductoFarmaciaResponse])
def listar_productos(
    buscar: Optional[str] = None,
    stock_bajo: Optional[bool] = None,
    activo: bool = True,
    db: Session = Depends(get_db)
):
    """Listar productos de farmacia"""
    
    query = db.query(ProductoFarmacia).filter(ProductoFarmacia.activo == activo)
    
    if buscar:
        buscar_lower = f"%{buscar.lower()}%"
        query = query.filter(ProductoFarmacia.nombre.ilike(buscar_lower))
    
    if stock_bajo:
        query = query.filter(ProductoFarmacia.stock_actual <= ProductoFarmacia.stock_minimo)
    
    productos = query.all()
    
    # Agregar alertas
    hoy = date.today()
    result = []
    for prod in productos:
        response = ProductoFarmaciaResponse.model_validate(prod)
        response.alerta_stock = prod.stock_actual <= prod.stock_minimo
        if prod.fecha_vencimiento:
            dias_vencimiento = (prod.fecha_vencimiento - hoy).days
            response.alerta_vencimiento = dias_vencimiento <= 30
        result.append(response)
    
    return result

@router.get("/productos/{producto_id}", response_model=ProductoFarmaciaResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener un producto por ID"""
    
    producto = db.query(ProductoFarmacia).filter(ProductoFarmacia.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return producto

@router.put("/productos/{producto_id}", response_model=ProductoFarmaciaResponse)
def actualizar_producto(
    producto_id: int,
    producto_update: ProductoFarmaciaUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un producto"""
    
    producto = db.query(ProductoFarmacia).filter(ProductoFarmacia.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    update_data = producto_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(producto, field, value)
    
    db.commit()
    db.refresh(producto)
    
    return producto

# ============================================================================
# ENDPOINTS - MOVIMIENTOS INVENTARIO
# ============================================================================

@router.post("/movimientos", response_model=MovimientoInventarioResponse, status_code=status.HTTP_201_CREATED)
def registrar_movimiento_inventario(
    movimiento: MovimientoInventarioCreate,
    db: Session = Depends(get_db)
):
    """Registrar movimiento de inventario (entrada/salida/ajuste)"""
    
    producto = db.query(ProductoFarmacia).filter(ProductoFarmacia.id == movimiento.producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    stock_anterior = producto.stock_actual
    
    if movimiento.tipo == TipoMovimientoInventarioEnum.entrada:
        producto.stock_actual += movimiento.cantidad
    elif movimiento.tipo == TipoMovimientoInventarioEnum.salida:
        if producto.stock_actual < movimiento.cantidad:
            raise HTTPException(status_code=400, detail="Stock insuficiente")
        producto.stock_actual -= movimiento.cantidad
    else:  # ajuste
        producto.stock_actual = movimiento.cantidad
    
    db_movimiento = MovimientoInventario(
        **movimiento.model_dump(),
        stock_anterior=stock_anterior,
        stock_nuevo=producto.stock_actual
    )
    
    db.add(db_movimiento)
    db.commit()
    db.refresh(db_movimiento)
    
    response = MovimientoInventarioResponse.model_validate(db_movimiento)
    response.producto_nombre = producto.nombre
    
    return response

@router.get("/movimientos/producto/{producto_id}", response_model=List[MovimientoInventarioResponse])
def listar_movimientos_producto(producto_id: int, db: Session = Depends(get_db)):
    """Listar movimientos de un producto"""
    
    movimientos = db.query(MovimientoInventario).filter(
        MovimientoInventario.producto_id == producto_id
    ).order_by(MovimientoInventario.fecha_hora.desc()).all()
    
    result = []
    for mov in movimientos:
        producto = db.query(ProductoFarmacia).filter(ProductoFarmacia.id == mov.producto_id).first()
        response = MovimientoInventarioResponse.model_validate(mov)
        if producto:
            response.producto_nombre = producto.nombre
        result.append(response)
    
    return result

# ============================================================================
# ENDPOINTS - COMPRAS
# ============================================================================

@router.post("/compras", response_model=CompraFarmaciaResponse, status_code=status.HTTP_201_CREATED)
def crear_compra(compra: CompraFarmaciaCreate, db: Session = Depends(get_db)):
    """Registrar una compra a proveedor"""
    
    # Verificar proveedor
    proveedor = db.query(Proveedor).filter(Proveedor.id == compra.proveedor_id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    # Calcular total
    total = sum(p.cantidad * p.precio_unitario for p in compra.productos)
    
    # Crear compra
    db_compra = CompraFarmacia(
        proveedor_id=compra.proveedor_id,
        fecha_compra=compra.fecha_compra,
        numero_factura=compra.numero_factura,
        total=total,
        observaciones=compra.observaciones,
        usuario_id=compra.usuario_id
    )
    db.add(db_compra)
    db.flush()
    
    # Agregar detalles y actualizar inventario
    detalles = []
    for prod in compra.productos:
        producto = db.query(ProductoFarmacia).filter(ProductoFarmacia.id == prod.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {prod.producto_id} no encontrado")
        
        detalle = DetalleCompra(
            compra_id=db_compra.id,
            producto_id=prod.producto_id,
            cantidad=prod.cantidad,
            precio_unitario=prod.precio_unitario,
            subtotal=prod.cantidad * prod.precio_unitario
        )
        db.add(detalle)
        detalles.append(detalle)
        
        # Actualizar stock
        producto.stock_actual += prod.cantidad
    
    db.commit()
    db.refresh(db_compra)
    
    # Preparar respuesta
    response = CompraFarmaciaResponse.model_validate(db_compra)
    response.proveedor_nombre = proveedor.nombre
    response.productos = [DetalleCompraResponse.model_validate(d) for d in detalles]
    
    return response

@router.get("/compras", response_model=List[CompraFarmaciaResponse])
def listar_compras(
    proveedor_id: Optional[int] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Listar compras"""
    
    query = db.query(CompraFarmacia)
    
    if proveedor_id:
        query = query.filter(CompraFarmacia.proveedor_id == proveedor_id)
    
    if fecha_desde:
        query = query.filter(CompraFarmacia.fecha_compra >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(CompraFarmacia.fecha_compra <= fecha_hasta)
    
    compras = query.order_by(CompraFarmacia.fecha_compra.desc()).all()
    
    result = []
    for compra in compras:
        proveedor = db.query(Proveedor).filter(Proveedor.id == compra.proveedor_id).first()
        detalles = db.query(DetalleCompra).filter(DetalleCompra.compra_id == compra.id).all()
        
        response = CompraFarmaciaResponse.model_validate(compra)
        if proveedor:
            response.proveedor_nombre = proveedor.nombre
        response.productos = [DetalleCompraResponse.model_validate(d) for d in detalles]
        
        result.append(response)
    
    return result

# ============================================================================
# ENDPOINTS - VENTAS
# ============================================================================

@router.post("/ventas", response_model=VentaFarmaciaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(venta: VentaFarmaciaCreate, db: Session = Depends(get_db)):
    """Registrar una venta de farmacia"""
    
    # Calcular total
    total = sum(p.cantidad * p.precio_unitario for p in venta.productos)
    total_final = total - venta.descuento
    
    # Crear venta
    db_venta = VentaFarmacia(
        paciente_id=venta.paciente_id,
        receta_id=venta.receta_id,
        total=total,
        descuento=venta.descuento,
        total_final=total_final,
        usuario_id=venta.usuario_id
    )
    db.add(db_venta)
    db.flush()
    
    # Agregar detalles y actualizar inventario
    detalles = []
    for prod in venta.productos:
        producto = db.query(ProductoFarmacia).filter(ProductoFarmacia.id == prod.producto_id).first()
        if not producto:
            raise HTTPException(status_code=404, detail=f"Producto {prod.producto_id} no encontrado")
        
        if producto.stock_actual < prod.cantidad:
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock_actual}"
            )
        
        detalle = DetalleVenta(
            venta_id=db_venta.id,
            producto_id=prod.producto_id,
            cantidad=prod.cantidad,
            precio_unitario=prod.precio_unitario,
            subtotal=prod.cantidad * prod.precio_unitario
        )
        db.add(detalle)
        detalles.append(detalle)
        
        # Actualizar stock
        producto.stock_actual -= prod.cantidad
    
    db.commit()
    db.refresh(db_venta)
    
    # Preparar respuesta
    response = VentaFarmaciaResponse.model_validate(db_venta)
    
    if db_venta.paciente_id:
        paciente = db.query(Paciente).filter(Paciente.id == db_venta.paciente_id).first()
        if paciente:
            response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
    
    response.productos = [DetalleVentaResponse.model_validate(d) for d in detalles]
    
    return response

@router.get("/ventas", response_model=List[VentaFarmaciaResponse])
def listar_ventas(
    paciente_id: Optional[int] = None,
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Listar ventas"""
    
    query = db.query(VentaFarmacia)
    
    if paciente_id:
        query = query.filter(VentaFarmacia.paciente_id == paciente_id)
    
    if fecha_desde:
        query = query.filter(func.date(VentaFarmacia.fecha_venta) >= fecha_desde)
    
    if fecha_hasta:
        query = query.filter(func.date(VentaFarmacia.fecha_venta) <= fecha_hasta)
    
    ventas = query.order_by(VentaFarmacia.fecha_venta.desc()).all()
    
    result = []
    for venta in ventas:
        detalles = db.query(DetalleVenta).filter(DetalleVenta.venta_id == venta.id).all()
        
        response = VentaFarmaciaResponse.model_validate(venta)
        
        if venta.paciente_id:
            paciente = db.query(Paciente).filter(Paciente.id == venta.paciente_id).first()
            if paciente:
                response.paciente_nombre = f"{paciente.nombres} {paciente.apellidos}"
        
        response.productos = [DetalleVentaResponse.model_validate(d) for d in detalles]
        
        result.append(response)
    
    return result

# ============================================================================
# ENDPOINTS - ESTADÍSTICAS
# ============================================================================

@router.get("/estadisticas", response_model=EstadisticasFarmacia)
def obtener_estadisticas_farmacia(db: Session = Depends(get_db)):
    """Obtener estadísticas de farmacia"""
    
    total_productos = db.query(ProductoFarmacia).filter(ProductoFarmacia.activo == True).count()
    
    productos_stock_bajo = db.query(ProductoFarmacia).filter(
        ProductoFarmacia.activo == True,
        ProductoFarmacia.stock_actual <= ProductoFarmacia.stock_minimo
    ).count()
    
    # Productos por vencer en 30 días
    fecha_limite = date.today() + timedelta(days=30)
    productos_por_vencer = db.query(ProductoFarmacia).filter(
        ProductoFarmacia.activo == True,
        ProductoFarmacia.fecha_vencimiento <= fecha_limite,
        ProductoFarmacia.fecha_vencimiento >= date.today()
    ).count()
    
    # Valor del inventario
    productos = db.query(ProductoFarmacia).filter(ProductoFarmacia.activo == True).all()
    valor_inventario = sum(p.stock_actual * p.precio_compra for p in productos)
    
    return {
        "total_productos": total_productos,
        "productos_stock_bajo": productos_stock_bajo,
        "productos_por_vencer": productos_por_vencer,
        "valor_inventario": round(valor_inventario, 2)
    }