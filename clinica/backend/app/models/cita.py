from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

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

class Cita(Base):
    __tablename__ = "citas"

    id = Column(Integer, primary_key=True, index=True)
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    fecha_hora = Column(DateTime(timezone=True), nullable=False, index=True)
    duracion_minutos = Column(Integer, default=20)
    
    tipo_cita = Column(SQLEnum(TipoCitaEnum), nullable=False)
    estado = Column(SQLEnum(EstadoCitaEnum), default=EstadoCitaEnum.programada)
    
    motivo = Column(Text, nullable=True)
    notas = Column(Text, nullable=True)
    
    recordatorio_enviado = Column(Boolean, default=False)
    confirmada_paciente = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    paciente = relationship("Paciente")
    medico = relationship("Usuario")