from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Consulta(Base):
    __tablename__ = "consultas"

    id = Column(Integer, primary_key=True, index=True)
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cita_id = Column(Integer, ForeignKey("citas.id"), nullable=True)
    
    fecha_hora = Column(DateTime(timezone=True), server_default=func.now())
    
    # Motivo y enfermedad actual
    motivo_consulta = Column(Text, nullable=False)
    historia_enfermedad_actual = Column(Text, nullable=True)
    
    # Signos vitales
    presion_sistolica = Column(Integer, nullable=True)
    presion_diastolica = Column(Integer, nullable=True)
    frecuencia_cardiaca = Column(Integer, nullable=True)
    temperatura = Column(Float, nullable=True)
    saturacion_oxigeno = Column(Integer, nullable=True)
    frecuencia_respiratoria = Column(Integer, nullable=True)
    peso = Column(Float, nullable=True)
    talla = Column(Float, nullable=True)
    
    # Examen físico y diagnóstico
    examen_fisico = Column(Text, nullable=True)
    diagnostico = Column(Text, nullable=True)
    plan_tratamiento = Column(Text, nullable=True)
    
    # Observaciones
    observaciones = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones
    paciente = relationship("Paciente")
    medico = relationship("Usuario")
    cita = relationship("Cita")