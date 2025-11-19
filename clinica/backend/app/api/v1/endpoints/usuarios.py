from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.usuario import Usuario, Rol
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate, RolResponse
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/roles", response_model=List[RolResponse])
async def get_roles(db: Session = Depends(get_db)):
    roles = db.query(Rol).all()
    return roles

@router.get("/", response_model=List[UsuarioResponse])
async def get_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.post("/", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def create_usuario(
    usuario_data: UsuarioCreate,
    db: Session = Depends(get_db)
):
    # Verificar si username ya existe
    existing = db.query(Usuario).filter(Usuario.username == usuario_data.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="El username ya existe")
    
    # Verificar si email ya existe
    existing = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="El email ya existe")
    
    # Crear nuevo usuario
    usuario = Usuario(
        username=usuario_data.username,
        email=usuario_data.email,
        password_hash=get_password_hash(usuario_data.password),
        nombres=usuario_data.nombres,
        apellidos=usuario_data.apellidos,
        rol_id=usuario_data.rol_id
    )
    
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    
    return usuario

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Actualizar campos
    if usuario_data.email:
        usuario.email = usuario_data.email
    if usuario_data.nombres:
        usuario.nombres = usuario_data.nombres
    if usuario_data.apellidos:
        usuario.apellidos = usuario_data.apellidos
    if usuario_data.rol_id:
        usuario.rol_id = usuario_data.rol_id
    if usuario_data.activo is not None:
        usuario.activo = usuario_data.activo
    
    db.commit()
    db.refresh(usuario)
    
    return usuario

@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(usuario)
    db.commit()
    
    return None