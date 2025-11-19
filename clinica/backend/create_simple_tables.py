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