from sqlalchemy import Column, Integer, String, Date, Text, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

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

class Paciente(Base):
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    
    # Datos personales básicos
    nombres = Column(String(100), nullable=False, index=True)
    apellidos = Column(String(100), nullable=False, index=True)
    fecha_nacimiento = Column(Date, nullable=False)
    genero = Column(SQLEnum(GeneroEnum), nullable=False)
    dpi = Column(String(13), unique=True, nullable=False, index=True)
    
    # Contacto
    telefono_principal = Column(String(15), nullable=False)
    telefono_secundario = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    direccion = Column(Text, nullable=False)
    municipio = Column(String(100), nullable=True)
    departamento = Column(String(100), nullable=True)
    
    # Información adicional
    estado_civil = Column(SQLEnum(EstadoCivilEnum), nullable=True)
    religion = Column(String(50), nullable=True)
    ocupacion = Column(String(100), nullable=True)
    tipo_sangre = Column(SQLEnum(TipoSangreEnum), nullable=True)
    
    # Seguro médico
    tiene_igss = Column(Boolean, default=False)
    numero_igss = Column(String(20), nullable=True)
    tiene_seguro_privado = Column(Boolean, default=False)
    nombre_seguro = Column(String(100), nullable=True)
    
    # Contacto de emergencia
    emergencia_nombre = Column(String(100), nullable=False)
    emergencia_telefono = Column(String(15), nullable=False)
    emergencia_parentesco = Column(String(50), nullable=True)
    
    # Foto
    foto_url = Column(String(255), nullable=True)
    
    # Metadatos
    activo = Column(Boolean, default=True)
    observaciones = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones (las agregaremos después)
    # archivos = relationship("ArchivosPaciente", back_populates="paciente")
    # consultas = relationship("Consulta", back_populates="paciente")

    # Relaciones
    archivos = relationship("ArchivosPaciente", back_populates="paciente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Paciente {self.nombres} {self.apellidos}>"
    
    @property
    def edad(self) -> int:
        """Calcular edad actual del paciente"""
        from datetime import date
        today = date.today()
        edad = today.year - self.fecha_nacimiento.year
        if today.month < self.fecha_nacimiento.month or \
           (today.month == self.fecha_nacimiento.month and today.day < self.fecha_nacimiento.day):
            edad -= 1
        return edad