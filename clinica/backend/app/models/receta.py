from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    
    consulta_id = Column(Integer, ForeignKey("consultas.id"), nullable=False)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    medico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    
    indicaciones_generales = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    consulta = relationship("Consulta")
    paciente = relationship("Paciente")
    medico = relationship("Usuario")
    detalles = relationship("RecetaDetalle", back_populates="receta")

class RecetaDetalle(Base):
    __tablename__ = "receta_detalle"

    id = Column(Integer, primary_key=True, index=True)
    
    receta_id = Column(Integer, ForeignKey("recetas.id"), nullable=False)
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"), nullable=True)
    
    medicamento_texto = Column(String(300), nullable=False)
    presentacion = Column(String(100), nullable=True)
    dosis = Column(String(100), nullable=False)
    frecuencia = Column(String(100), nullable=False)
    duracion = Column(String(100), nullable=False)
    via_administracion = Column(String(50), nullable=True)
    indicaciones = Column(Text, nullable=True)
    
    # Relación
    receta = relationship("Receta", back_populates="detalles")
    medicamento = relationship("Medicamento")