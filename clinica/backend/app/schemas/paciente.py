from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import date, datetime
from models.paciente import GeneroEnum, EstadoCivilEnum, TipoSangreEnum

class PacienteBase(BaseModel):
    # Datos personales
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    genero: GeneroEnum
    dpi: str
    
    # Contacto
    telefono_principal: str
    telefono_secundario: Optional[str] = None
    email: Optional[EmailStr] = None
    direccion: str
    municipio: Optional[str] = None
    departamento: Optional[str] = None
    
    # Información adicional
    estado_civil: Optional[EstadoCivilEnum] = None
    religion: Optional[str] = None
    ocupacion: Optional[str] = None
    tipo_sangre: Optional[TipoSangreEnum] = None
    
    # Seguro
    tiene_igss: bool = False
    numero_igss: Optional[str] = None
    tiene_seguro_privado: bool = False
    nombre_seguro: Optional[str] = None
    
    # Emergencia
    emergencia_nombre: str
    emergencia_telefono: str
    emergencia_parentesco: Optional[str] = None
    
    # Otros
    observaciones: Optional[str] = None

    @validator('dpi')
    def validar_dpi(cls, v):
        """Validar formato de DPI guatemalteco (13 dígitos)"""
        if not v.isdigit():
            raise ValueError('DPI debe contener solo números')
        if len(v) != 13:
            raise ValueError('DPI debe tener exactamente 13 dígitos')
        return v
    
    @validator('telefono_principal', 'telefono_secundario', 'emergencia_telefono')
    def validar_telefono(cls, v):
        """Validar formato de teléfono guatemalteco"""
        if v is None:
            return v
        # Remover espacios y guiones
        telefono = v.replace(' ', '').replace('-', '')
        if not telefono.isdigit():
            raise ValueError('Teléfono debe contener solo números')
        if len(telefono) != 8:
            raise ValueError('Teléfono debe tener 8 dígitos')
        return telefono

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(PacienteBase):
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    fecha_nacimiento: Optional[date] = None
    genero: Optional[GeneroEnum] = None
    dpi: Optional[str] = None
    telefono_principal: Optional[str] = None
    direccion: Optional[str] = None
    emergencia_nombre: Optional[str] = None
    emergencia_telefono: Optional[str] = None

class PacienteResponse(PacienteBase):
    id: int
    activo: bool
    foto_url: Optional[str]
    edad: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class PacienteListItem(BaseModel):
    """Para listar pacientes (menos campos)"""
    id: int
    nombres: str
    apellidos: str
    dpi: str
    telefono_principal: str
    edad: int
    genero: GeneroEnum
    foto_url: Optional[str]
    activo: bool

    class Config:
        from_attributes = True