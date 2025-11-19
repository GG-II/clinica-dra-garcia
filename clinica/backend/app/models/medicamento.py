from sqlalchemy import Column, Integer, String, Text, Float, Boolean
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from database import Base

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    
    nombre_generico = Column(String(200), nullable=False, index=True)
    nombre_comercial = Column(String(200), nullable=True)
    presentacion = Column(String(100), nullable=True)
    concentracion = Column(String(100), nullable=True)
    via_administracion = Column(String(50), nullable=True)
    
    interacciones = Column(Text, nullable=True)
    contraindicaciones = Column(Text, nullable=True)
    
    activo = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())