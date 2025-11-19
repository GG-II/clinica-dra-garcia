from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)

class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=8, max_length=100)
    rol_id: int

class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombres: Optional[str] = None
    apellidos: Optional[str] = None
    rol_id: Optional[int] = None
    activo: Optional[bool] = None

class UsuarioResponse(UsuarioBase):
    id: int
    rol_id: int
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolResponse(RolBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True