from database import engine, Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, DateTime, Text, Float, Enum as SQLEnum
from sqlalchemy.sql import func
import enum

print("🚀 Creando TODAS las tablas del sistema clínico...")
print("-" * 60)

# ============================================================================
# ENUMS
# ============================================================================

class GeneroEnum(str, enum.Enum):
    masculino = "Masculino"
    femenino = "Femenino"
    otro = "Otro"

class EstadoCivilEnum(str, enum.Enum):
    soltero = "Soltero/a"
    casado = "Casado/a"
    divorciado = "Divorciado/a"
    viudo = "Viudo/a"
    union_libre = "Unión Libre"

class TipoSangreEnum(str, enum.Enum):
    a_positivo = "A+"
    a_negativo = "A-"
    b_positivo = "B+"
    b_negativo = "B-"
    ab_positivo = "AB+"
    ab_negativo = "AB-"
    o_positivo = "O+"
    o_negativo = "O-"

class TipoCitaEnum(str, enum.Enum):
    primera_consulta = "Primera Consulta"
    reconsulta = "Reconsulta"
    procedimiento = "Procedimiento"
    control_embarazo = "Control de Embarazo"
    control_nino_sano = "Control de Niño Sano"
    emergencia = "Emergencia"

class EstadoCitaEnum(str, enum.Enum):
    programada = "Programada"
    confirmada = "Confirmada"
    en_atencion = "En Atención"
    completada = "Completada"
    cancelada = "Cancelada"
    no_asistio = "No Asistió"

class CategoriaArchivoEnum(str, enum.Enum):
    foto = "Foto"
    laboratorio = "Laboratorio"
    imagen = "Imagen"
    receta = "Receta"
    ekg = "EKG"
    video = "Video"
    otro = "Otro"

class TipoAntecedenteEnum(str, enum.Enum):
    patologico = "Patológico"
    quirurgico = "Quirúrgico"
    traumatico = "Traumático"
    alergico = "Alérgico"
    ginecologico = "Ginecológico"
    obstetrico = "Obstétrico"

class EstadoCamaEnum(str, enum.Enum):
    disponible = "Disponible"
    ocupada = "Ocupada"
    limpieza = "En Limpieza"
    mantenimiento = "Mantenimiento"

# ============================================================================
# TABLAS BASE (sin foreign keys)
# ============================================================================

class Rol(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(200))

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(200), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Medicamento(Base):
    __tablename__ = "medicamentos"
    id = Column(Integer, primary_key=True, index=True)
    nombre_generico = Column(String(200), nullable=False, index=True)
    nombre_comercial = Column(String(200))
    presentacion = Column(String(100))
    concentracion = Column(String(100))
    via_administracion = Column(String(50))
    interacciones = Column(Text)
    contraindicaciones = Column(Text)
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Cama(Base):
    __tablename__ = "camas"
    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    estado = Column(SQLEnum(EstadoCamaEnum), default=EstadoCamaEnum.disponible)
    ubicacion = Column(String(100))

# ============================================================================
# PACIENTES
# ============================================================================

class Paciente(Base):
    __tablename__ = "pacientes"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Datos personales
    nombres = Column(String(100), nullable=False, index=True)
    apellidos = Column(String(100), nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(SQLEnum(GeneroEnum), nullable=False)
    dpi = Column(String(13), unique=True, nullable=False, index=True)
    
    # Contacto
    telefono_principal = Column(String(15), nullable=False)
    telefono_secundario = Column(String(15))
    email = Column(String(100))
    direccion = Column(Text, nullable=False)
    municipio = Column(String(100))
    departamento = Column(String(100))
    
    # Información adicional
    estado_civil = Column(SQLEnum(EstadoCivilEnum))
    religion = Column(String(50))
    ocupacion = Column(String(100))
    tipo_sangre = Column(SQLEnum(TipoSangreEnum))
    
    # Seguro
    tiene_igss = Column(Boolean, default=False)
    numero_igss = Column(String(20))
    tiene_seguro_privado = Column(Boolean, default=False)
    nombre_seguro = Column(String(100))
    
    # Emergencia
    emergencia_nombre = Column(String(100), nullable=False)
    emergencia_telefono = Column(String(15), nullable=False)
    emergencia_parentesco = Column(String(50))
    
    # Foto
    foto_url = Column(String(255))
    
    # Metadatos
    activo = Column(Boolean, default=True)
    observaciones = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

# ============================================================================
# TABLAS CON FOREIGN KEYS
# ============================================================================

class ArchivosPaciente(Base):
    __tablename__ = "archivos_paciente"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    categoria = Column(SQLEnum(CategoriaArchivoEnum), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    tipo_mime = Column(String(100), nullable=False)
    tamano_bytes = Column(Integer, nullable=False)
    descripcion = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Cita(Base):
    __tablename__ = "citas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), nullable=False, index=True)
    duracion_minutos = Column(Integer, default=20)
    tipo_cita = Column(SQLEnum(TipoCitaEnum), nullable=False)
    estado = Column(SQLEnum(EstadoCitaEnum), default=EstadoCitaEnum.programada)
    motivo = Column(Text)
    notas = Column(Text)
    recordatorio_enviado = Column(Boolean, default=False)
    confirmada_paciente = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Antecedente(Base):
    __tablename__ = "antecedentes"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo = Column(SQLEnum(TipoAntecedenteEnum), nullable=False)
    descripcion = Column(Text, nullable=False)
    activo = Column(Boolean, default=True)

class Consulta(Base):
    __tablename__ = "consultas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cita_id = Column(Integer, ForeignKey("citas.id"))
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    
    # Consulta
    motivo_consulta = Column(Text, nullable=False)
    historia_enfermedad_actual = Column(Text)
    
    # Signos vitales
    presion_sistolica = Column(Integer)
    presion_diastolica = Column(Integer)
    frecuencia_cardiaca = Column(Integer)
    temperatura = Column(Float)
    saturacion_oxigeno = Column(Integer)
    frecuencia_respiratoria = Column(Integer)
    peso = Column(Float)
    talla = Column(Float)
    
    # Diagnóstico
    examen_fisico = Column(Text)
    diagnostico = Column(Text)
    plan_tratamiento = Column(Text)
    observaciones = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Receta(Base):
    __tablename__ = "recetas"
    
    id = Column(Integer, primary_key=True, index=True)
    consulta_id = Column(Integer, ForeignKey("consultas.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    indicaciones_generales = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class RecetaDetalle(Base):
    __tablename__ = "receta_detalle"
    
    id = Column(Integer, primary_key=True, index=True)
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"))
    medicamento_texto = Column(String(300), nullable=False)
    presentacion = Column(String(100))
    dosis = Column(String(100), nullable=False)
    frecuencia = Column(String(100), nullable=False)
    duracion = Column(String(100), nullable=False)
    via_administracion = Column(String(50))
    indicaciones = Column(Text)

class Hospitalizacion(Base):
    __tablename__ = "hospitalizaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_responsable_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cama_id = Column(Integer, ForeignKey("camas.id"), nullable=False)
    fecha_ingreso = Column(DateTime(timezone=True), server_default=func.now())
    fecha_egreso = Column(DateTime(timezone=True))
    diagnostico_ingreso = Column(Text, nullable=False)
    motivo = Column(Text, nullable=False)
    activa = Column(Boolean, default=True)


    # ============================================================================
# NOTAS MÉDICAS
# ============================================================================

class TipoNotaMedicaEnum(str, enum.Enum):
    ingreso = "Ingreso"
    evolucion = "Evolución"
    procedimiento = "Procedimiento"
    operatoria = "Operatoria"
    egreso = "Egreso"

class NotaMedica(Base):
    __tablename__ = "notas_medicas"
    
    id = Column(Integer, primary_key=True, index=True)
    hospitalizacion_id = Column(Integer, ForeignKey("hospitalizaciones.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(SQLEnum(TipoNotaMedicaEnum), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    
    # Campos comunes
    contenido = Column(Text, nullable=False)
    
    # Campos específicos de nota operatoria
    cirugia_realizada = Column(String(300))
    cirujano_id = Column(Integer, ForeignKey("usuarios.id"))
    anestesiologo = Column(String(200))
    tipo_anestesia = Column(String(100))
    diagnostico_preoperatorio = Column(Text)
    diagnostico_postoperatorio = Column(Text)
    hallazgos = Column(Text)
    complicaciones = Column(Text)
    sangrado_estimado = Column(String(100))
    especimenes_patologia = Column(Text)
    pronostico = Column(String(200))

# ============================================================================
# ÓRDENES MÉDICAS
# ============================================================================

class TipoOrdenEnum(str, enum.Enum):
    medicamento = "Medicamento"
    dieta = "Dieta"
    signos_vitales = "Signos Vitales"
    laboratorio = "Laboratorio"
    imagen = "Estudio de Imagen"
    interconsulta = "Interconsulta"
    cuidados = "Cuidados de Enfermería"
    otro = "Otro"

class EstadoOrdenEnum(str, enum.Enum):
    activa = "Activa"
    suspendida = "Suspendida"
    completada = "Completada"

class OrdenMedica(Base):
    __tablename__ = "ordenes_medicas"
    
    id = Column(Integer, primary_key=True, index=True)
    hospitalizacion_id = Column(Integer, ForeignKey("hospitalizaciones.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(SQLEnum(TipoOrdenEnum), nullable=False)
    descripcion = Column(Text, nullable=False)
    estado = Column(SQLEnum(EstadoOrdenEnum), default=EstadoOrdenEnum.activa)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    
    # Para medicamentos
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"))
    dosis = Column(String(100))
    frecuencia = Column(String(100))
    via = Column(String(50))
    duracion = Column(String(100))

# ============================================================================
# LABORATORIOS
# ============================================================================

class CategoriaLaboratorioEnum(str, enum.Enum):
    hematologia = "Hematología"
    quimica = "Química Sanguínea"
    funcion_hepatica = "Función Hepática"
    funcion_renal = "Función Renal"
    perfil_lipidico = "Perfil Lipídico"
    tiroides = "Pruebas Tiroideas"
    diabetes = "Diabetes"
    marcadores_tumorales = "Marcadores Tumorales"
    inmunologia = "Inmunología"
    grupo_sanguineo = "Grupo Sanguíneo"
    orina_heces = "Orina y Heces"
    microbiologia = "Microbiología"
    imagen = "Estudios de Imagen"
    otro = "Otro"

class TipoEstudio(Base):
    __tablename__ = "tipos_estudio"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    categoria = Column(SQLEnum(CategoriaLaboratorioEnum), nullable=False)
    descripcion = Column(Text)
    activo = Column(Boolean, default=True)

class ResultadoLaboratorio(Base):
    __tablename__ = "resultados_laboratorio"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    consulta_id = Column(Integer, ForeignKey("consultas.id"))
    tipo_estudio_id = Column(Integer, ForeignKey("tipos_estudio.id"), nullable=False)
    fecha_toma = Column(DateTime(timezone=True), nullable=False)
    fecha_resultado = Column(DateTime(timezone=True), server_default=func.now())
    
    # Resultado como JSON (flexible para diferentes tipos de estudios)
    resultado = Column(Text, nullable=False)  # JSON string
    
    # Valores de referencia
    valor_minimo = Column(String(50))
    valor_maximo = Column(String(50))
    unidad = Column(String(50))
    
    # Flags
    valor_critico = Column(Boolean, default=False)
    laboratorio_externo = Column(String(200))
    observaciones = Column(Text)

# ============================================================================
# VACUNACIÓN
# ============================================================================

class TipoVacunaEnum(str, enum.Enum):
    bcg = "BCG"
    hepatitis_b = "Hepatitis B"
    pentavalente = "Pentavalente"
    rotavirus = "Rotavirus"
    neumococo = "Neumococo"
    influenza = "Influenza"
    srp = "SRP (Sarampión, Rubéola, Paperas)"
    varicela = "Varicela"
    hepatitis_a = "Hepatitis A"
    dpt = "DPT"
    opv = "OPV (Polio Oral)"
    covid19 = "COVID-19"
    otra = "Otra"

class Vacuna(Base):
    __tablename__ = "vacunas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo_vacuna = Column(SQLEnum(TipoVacunaEnum), nullable=False)
    dosis = Column(String(50), nullable=False)  # "1ra dosis", "2da dosis", "Refuerzo"
    fecha_aplicacion = Column(Date, nullable=False)
    lote = Column(String(100))
    lugar_aplicacion = Column(String(100))  # "Brazo izquierdo", "Muslo derecho"
    medico_id = Column(Integer, ForeignKey("usuarios.id"))
    observaciones = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# ============================================================================
# LISTA DE ESPERA
# ============================================================================

class ListaEspera(Base):
    __tablename__ = "lista_espera"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo_cita = Column(SQLEnum(TipoCitaEnum), nullable=False)
    motivo = Column(Text)
    prioridad = Column(Integer, default=0)  # Mayor número = mayor prioridad
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now())
    notificado = Column(Boolean, default=False)
    activo = Column(Boolean, default=True)

# ============================================================================
# INTERCONSULTAS
# ============================================================================

class EstadoInterconsultaEnum(str, enum.Enum):
    solicitada = "Solicitada"
    en_proceso = "En Proceso"
    completada = "Completada"
    cancelada = "Cancelada"

class Interconsulta(Base):
    __tablename__ = "interconsultas"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    consulta_id = Column(Integer, ForeignKey("consultas.id"))
    hospitalizacion_id = Column(Integer, ForeignKey("hospitalizaciones.id"))
    
    medico_solicitante_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    especialidad_solicitada = Column(String(100), nullable=False)
    medico_consultor_id = Column(Integer, ForeignKey("usuarios.id"))
    
    motivo = Column(Text, nullable=False)
    hallazgos = Column(Text)
    recomendaciones = Column(Text)
    
    estado = Column(SQLEnum(EstadoInterconsultaEnum), default=EstadoInterconsultaEnum.solicitada)
    fecha_solicitud = Column(DateTime(timezone=True), server_default=func.now())
    fecha_respuesta = Column(DateTime(timezone=True))

# ============================================================================
# CAJA Y FACTURACIÓN
# ============================================================================

class Caja(Base):
    __tablename__ = "caja"
    
    id = Column(Integer, primary_key=True, index=True)
    fecha_apertura = Column(DateTime(timezone=True), server_default=func.now())
    fecha_cierre = Column(DateTime(timezone=True))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto_inicial = Column(Float, nullable=False)
    monto_final = Column(Float)
    total_ingresos = Column(Float)
    total_egresos = Column(Float)
    diferencia = Column(Float)  # Faltante o sobrante
    cerrada = Column(Boolean, default=False)

class TipoMovimientoEnum(str, enum.Enum):
    ingreso = "Ingreso"
    egreso = "Egreso"

class TipoIngresoEnum(str, enum.Enum):
    consulta = "Consulta Médica"
    reconsulta = "Reconsulta"
    procedimiento = "Procedimiento"
    hospitalizacion = "Hospitalización"
    farmacia = "Venta Farmacia"
    laboratorio = "Laboratorio"
    otro = "Otro"

class TipoEgresoEnum(str, enum.Enum):
    compra_medicamentos = "Compra Medicamentos"
    servicios = "Servicios"
    salarios = "Salarios"
    mantenimiento = "Mantenimiento"
    publicidad = "Publicidad"
    papeleria = "Papelería"
    otro = "Otro"

class MovimientoCaja(Base):
    __tablename__ = "movimientos_caja"
    
    id = Column(Integer, primary_key=True, index=True)
    caja_id = Column(Integer, ForeignKey("caja.id"), nullable=False)
    tipo_movimiento = Column(SQLEnum(TipoMovimientoEnum), nullable=False)
    
    # Para ingresos
    tipo_ingreso = Column(SQLEnum(TipoIngresoEnum))
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    
    # Para egresos
    tipo_egreso = Column(SQLEnum(TipoEgresoEnum))
    proveedor = Column(String(200))
    
    concepto = Column(String(300), nullable=False)
    monto = Column(Float, nullable=False)
    forma_pago = Column(String(50), nullable=False)  # Efectivo, Transferencia
    numero_documento = Column(String(100))
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

class CuentaPorCobrar(Base):
    __tablename__ = "cuentas_por_cobrar"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    convenio = Column(String(100))  # "IGSS", "Seguro X"
    concepto = Column(String(300), nullable=False)
    monto_total = Column(Float, nullable=False)
    monto_pagado = Column(Float, default=0)
    saldo = Column(Float, nullable=False)
    fecha_emision = Column(Date, nullable=False)
    fecha_vencimiento = Column(Date)
    pagado = Column(Boolean, default=False)
    observaciones = Column(Text)

class Cotizacion(Base):
    __tablename__ = "cotizaciones"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha = Column(DateTime(timezone=True), server_default=func.now())
    vigencia_dias = Column(Integer, default=30)
    servicios = Column(Text, nullable=False)  # JSON
    total = Column(Float, nullable=False)
    condiciones = Column(Text)
    aceptada = Column(Boolean, default=False)

# ============================================================================
# FARMACIA E INVENTARIO
# ============================================================================

class Proveedor(Base):
    __tablename__ = "proveedores"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(200), nullable=False)
    nit = Column(String(20))
    direccion = Column(Text)
    telefono = Column(String(15))
    email = Column(String(100))
    contacto = Column(String(100))
    activo = Column(Boolean, default=True)

class ProductoFarmacia(Base):
    __tablename__ = "productos_farmacia"
    
    id = Column(Integer, primary_key=True, index=True)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"))
    codigo_interno = Column(String(50), unique=True)
    nombre = Column(String(200), nullable=False)
    tipo = Column(String(50))  # "Medicamento", "Insumo", "Material"
    presentacion = Column(String(100))
    lote = Column(String(100))
    fecha_vencimiento = Column(Date)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"))
    
    # Inventario
    stock_actual = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=10)
    
    # Precios
    precio_compra = Column(Float, nullable=False)
    precio_venta = Column(Float, nullable=False)
    
    ubicacion = Column(String(100))
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class TipoMovimientoInventarioEnum(str, enum.Enum):
    entrada = "Entrada"
    salida = "Salida"
    ajuste = "Ajuste"

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"
    
    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos_farmacia.id"), nullable=False)
    tipo = Column(SQLEnum(TipoMovimientoInventarioEnum), nullable=False)
    cantidad = Column(Integer, nullable=False)
    stock_anterior = Column(Integer, nullable=False)
    stock_nuevo = Column(Integer, nullable=False)
    motivo = Column(String(300), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())

class CompraFarmacia(Base):
    __tablename__ = "compras_farmacia"
    
    id = Column(Integer, primary_key=True, index=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=False)
    fecha_compra = Column(Date, nullable=False)
    numero_factura = Column(String(100))
    total = Column(Float, nullable=False)
    observaciones = Column(Text)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DetalleCompra(Base):
    __tablename__ = "detalle_compra"
    
    id = Column(Integer, primary_key=True, index=True)
    compra_id = Column(Integer, ForeignKey("compras_farmacia.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos_farmacia.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

class VentaFarmacia(Base):
    __tablename__ = "ventas_farmacia"
    
    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    receta_id = Column(Integer, ForeignKey("recetas.id"))
    fecha_venta = Column(DateTime(timezone=True), server_default=func.now())
    total = Column(Float, nullable=False)
    descuento = Column(Float, default=0)
    total_final = Column(Float, nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

class DetalleVenta(Base):
    __tablename__ = "detalle_venta"
    
    id = Column(Integer, primary_key=True, index=True)
    venta_id = Column(Integer, ForeignKey("ventas_farmacia.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos_farmacia.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

# ============================================================================
# CREAR TODAS LAS TABLAS
# ============================================================================

def create_all_tables():
    """Crear todas las tablas del sistema"""
    Base.metadata.create_all(bind=engine)
    
    print("✅ ¡Todas las tablas creadas exitosamente!")
    print("-" * 60)
    print("\n📋 Tablas creadas:")
    print("  ✅ roles")
    print("  ✅ usuarios")
    print("  ✅ medicamentos")
    print("  ✅ camas")
    print("  ✅ pacientes")
    print("  ✅ archivos_paciente")
    print("  ✅ citas")
    print("  ✅ antecedentes")
    print("  ✅ consultas")
    print("  ✅ recetas")
    print("  ✅ receta_detalle")
    print("  ✅ hospitalizaciones")
    print("\n🎉 Base de datos completa lista para usar!")

    

if __name__ == "__main__":
    create_all_tables()