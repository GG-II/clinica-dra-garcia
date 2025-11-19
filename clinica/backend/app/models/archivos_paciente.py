from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class CategoriaArchivoEnum(str, enum.Enum):
    foto = "Foto"
    laboratorio = "Laboratorio"
    imagen = "Imagen"
    receta = "Receta"
    ekg = "EKG"
    video = "Video"
    otro = "Otro"

class ArchivosPaciente(Base):
    __tablename__ = "archivos_paciente"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    
    categoria = Column(SQLEnum(CategoriaArchivoEnum), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(500), nullable=False)
    tipo_mime = Column(String(100), nullable=False)
    tamano_bytes = Column(Integer, nullable=False)
    
    descripcion = Column(String(500), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relación
    paciente = relationship("Paciente", back_populates="archivos")