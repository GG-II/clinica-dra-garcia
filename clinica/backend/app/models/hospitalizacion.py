from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class EstadoCamaEnum(str, enum.Enum):
    disponible = "Disponible"
    ocupada = "Ocupada"
    limpieza = "En Limpieza"
    mantenimiento = "Mantenimiento"

class Cama(Base):
    __tablename__ = "camas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(Integer, unique=True, nullable=False)
    estado = Column(SQLEnum(EstadoCamaEnum), default=EstadoCamaEnum.disponible)
    ubicacion = Column(String(100), nullable=True)

class Hospitalizacion(Base):
    __tablename__ = "hospitalizaciones"

    id = Column(Integer, primary_key=True, index=True)
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_responsable_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cama_id = Column(Integer, ForeignKey("camas.id"), nullable=False)
    
    fecha_ingreso = Column(DateTime(timezone=True), server_default=func.now())
    fecha_egreso = Column(DateTime(timezone=True), nullable=True)
    
    diagnostico_ingreso = Column(Text, nullable=False)
    motivo = Column(Text, nullable=False)
    
    activa = Column(Boolean, default=True)
    
    # Relaciones
    paciente = relationship("Paciente")
    medico_responsable = relationship("Usuario")
    cama = relationship("Cama")