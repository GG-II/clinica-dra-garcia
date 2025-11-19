from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    rol = relationship("Rol", back_populates="usuarios")
    
    activo = Column(Boolean, default=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relaciones con logs
    logs_creados = relationship("LogAuditoria", back_populates="usuario", foreign_keys="LogAuditoria.usuario_id")

class Rol(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    
    usuarios = relationship("Usuario", back_populates="rol")
    permisos = relationship("RolPermiso", back_populates="rol")
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Permiso(Base):
    __tablename__ = "permisos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), unique=True, nullable=False)
    descripcion = Column(String(255))
    modulo = Column(String(50), nullable=False)
    
    roles = relationship("RolPermiso", back_populates="permiso")

class RolPermiso(Base):
    __tablename__ = "rol_permisos"
    
    id = Column(Integer, primary_key=True, index=True)
    rol_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    permiso_id = Column(Integer, ForeignKey("permisos.id"), nullable=False)
    
    rol = relationship("Rol", back_populates="permisos")
    permiso = relationship("Permiso", back_populates="roles")

class LogAuditoria(Base):
    __tablename__ = "logs_auditoria"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    accion = Column(String(100), nullable=False)
    modulo = Column(String(50), nullable=False)
    descripcion = Column(String(500))
    ip_address = Column(String(45))
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    usuario = relationship("Usuario", back_populates="logs_creados", foreign_keys=[usuario_id])