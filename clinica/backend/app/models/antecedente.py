from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
import enum

class TipoAntecedenteEnum(str, enum.Enum):
    patologico = "Patológico"
    quirurgico = "Quirúrgico"
    traumatico = "Traumático"
    alergico = "Alérgico"
    ginecologico = "Ginecológico"
    obstetrico = "Obstétrico"

class Antecedente(Base):
    __tablename__ = "antecedentes"

    id = Column(Integer, primary_key=True, index=True)
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    tipo = Column(SQLEnum(TipoAntecedenteEnum), nullable=False)
    
    descripcion = Column(Text, nullable=False)
    activo = Column(Boolean, default=True)
    
    # Relación
    paciente = relationship("Paciente")