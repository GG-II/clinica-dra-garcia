# 🔧 Guía de Desarrollo - Sistema Clínico MEDGAR

Guía completa para desarrollar nuevas features en el sistema.

## 📋 Índice

1. [Flujo de Trabajo](#flujo-de-trabajo)
2. [Desarrollo de Backend](#desarrollo-de-backend)
3. [Desarrollo de Frontend](#desarrollo-de-frontend)
4. [Testing](#testing)
5. [Convenciones de Código](#convenciones-de-código)
6. [Git Workflow](#git-workflow)
7. [Ejemplo Completo: Nueva Feature](#ejemplo-completo-nueva-feature)

---

## 🔄 Flujo de Trabajo

### Proceso General para Nueva Feature
```
1. Planificación
   ├─ Definir User Story
   ├─ Estimar Story Points
   └─ Asignar a Sprint

2. Diseño
   ├─ Diseñar API endpoints (backend)
   ├─ Diseñar UI/UX (frontend)
   └─ Definir modelos de datos

3. Desarrollo
   ├─ Crear rama Git
   ├─ Backend: Models → Schemas → Endpoints
   ├─ Frontend: Types → Services → Components → Pages
   └─ Testing manual

4. Revisión
   ├─ Code review
   ├─ Testing
   └─ Ajustes

5. Integración
   ├─ Merge a develop
   ├─ Deploy a local
   └─ Demostración
```

---

## 🐍 Desarrollo de Backend

### Paso 1: Crear Modelo SQLAlchemy

**Ubicación**: `backend/app/models/`

**Ejemplo**: Crear modelo de Paciente

**Archivo**: `backend/app/models/paciente.py`
```python
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Identificación
    numero_expediente = Column(String(20), unique=True, nullable=False, index=True)
    dpi = Column(String(13), unique=True, index=True)
    
    # Información Personal
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    sexo = Column(String(1), nullable=False)  # M/F
    
    # Contacto
    direccion = Column(String(500))
    telefono1 = Column(String(8))
    telefono2 = Column(String(8))
    email = Column(String(100))
    
    # Datos Adicionales
    estado_civil = Column(String(20))
    religion = Column(String(50))
    tiene_igss = Column(Boolean, default=False)
    
    # Contacto de Emergencia
    contacto_emergencia_nombre = Column(String(100))
    contacto_emergencia_telefono = Column(String(8))
    
    # Foto
    foto_url = Column(String(255))
    
    # Control
    activo = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("usuarios.id"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    updated_by = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relaciones
    # archivos = relationship("ArchivoPaciente", back_populates="paciente")
    # consultas = relationship("Consulta", back_populates="paciente")

# Importar en app/models/__init__.py
# from app.models.paciente import Paciente
```

**Crear índices**:
```python
from sqlalchemy import Index

# Al final del archivo
Index('idx_pacientes_nombre', Paciente.nombres, Paciente.apellidos)
Index('idx_pacientes_fecha_nacimiento', Paciente.fecha_nacimiento)
```

---

### Paso 2: Crear Schemas Pydantic

**Ubicación**: `backend/app/schemas/`

**Archivo**: `backend/app/schemas/paciente.py`
```python
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date, datetime

# Schema Base (campos comunes)
class PacienteBase(BaseModel):
    nombres: str = Field(..., min_length=2, max_length=100)
    apellidos: str = Field(..., min_length=2, max_length=100)
    fecha_nacimiento: date
    sexo: str = Field(..., pattern="^[MF]$")
    dpi: Optional[str] = Field(None, max_length=13)
    direccion: Optional[str] = None
    telefono1: Optional[str] = Field(None, max_length=8)
    telefono2: Optional[str] = Field(None, max_length=8)
    email: Optional[EmailStr] = None
    estado_civil: Optional[str] = None
    religion: Optional[str] = None
    tiene_igss: bool = False
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None

# Schema para crear (incluye validaciones extra)
class PacienteCreate(PacienteBase):
    pass

# Schema para actualizar (todos opcionales)
class PacienteUpdate(BaseModel):
    nombres: Optional[str] = Field(None, min_length=2, max_length=100)
    apellidos: Optional[str] = Field(None, min_length=2, max_length=100)
    fecha_nacimiento: Optional[date] = None
    sexo: Optional[str] = Field(None, pattern="^[MF]$")
    dpi: Optional[str] = Field(None, max_length=13)
    direccion: Optional[str] = None
    telefono1: Optional[str] = Field(None, max_length=8)
    telefono2: Optional[str] = Field(None, max_length=8)
    email: Optional[EmailStr] = None
    estado_civil: Optional[str] = None
    religion: Optional[str] = None
    tiene_igss: Optional[bool] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    activo: Optional[bool] = None

# Schema para respuesta (incluye campos generados)
class PacienteResponse(PacienteBase):
    id: int
    numero_expediente: str
    foto_url: Optional[str] = None
    activo: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Schema para lista (versión reducida)
class PacienteListItem(BaseModel):
    id: int
    numero_expediente: str
    nombres: str
    apellidos: str
    fecha_nacimiento: date
    telefono1: Optional[str] = None
    foto_url: Optional[str] = None
    
    class Config:
        from_attributes = True
```

---

### Paso 3: Crear Endpoints

**Ubicación**: `backend/app/api/v1/endpoints/`

**Archivo**: `backend/app/api/v1/endpoints/pacientes.py`
```python
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.paciente import Paciente
from app.schemas.paciente import (
    PacienteCreate, 
    PacienteUpdate, 
    PacienteResponse,
    PacienteListItem
)

router = APIRouter()

@router.get("/", response_model=List[PacienteListItem])
async def get_pacientes(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    activo: bool = Query(True),
    db: Session = Depends(get_db)
):
    """
    Obtener lista de pacientes con paginación.
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Número máximo de registros (default: 100, max: 100)
    - **activo**: Filtrar por estado activo (default: True)
    """
    query = db.query(Paciente).filter(Paciente.activo == activo)
    pacientes = query.offset(skip).limit(limit).all()
    return pacientes

@router.get("/buscar", response_model=List[PacienteListItem])
async def buscar_pacientes(
    q: str = Query(..., min_length=3),
    db: Session = Depends(get_db)
):
    """
    Buscar pacientes por nombre, apellido, DPI o número de expediente.
    
    - **q**: Término de búsqueda (mínimo 3 caracteres)
    """
    search_term = f"%{q}%"
    pacientes = db.query(Paciente).filter(
        (Paciente.nombres.ilike(search_term)) |
        (Paciente.apellidos.ilike(search_term)) |
        (Paciente.dpi.ilike(search_term)) |
        (Paciente.numero_expediente.ilike(search_term))
    ).limit(50).all()
    
    return pacientes

@router.get("/{paciente_id}", response_model=PacienteResponse)
async def get_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtener un paciente específico por ID.
    """
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    return paciente

@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
async def create_paciente(
    paciente_data: PacienteCreate,
    db: Session = Depends(get_db)
):
    """
    Crear un nuevo paciente.
    """
    # Validar DPI único si se proporciona
    if paciente_data.dpi:
        existing = db.query(Paciente).filter(Paciente.dpi == paciente_data.dpi).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un paciente con este DPI"
            )
    
    # Generar número de expediente
    ultimo = db.query(Paciente).order_by(Paciente.id.desc()).first()
    numero = 1 if not ultimo else ultimo.id + 1
    numero_expediente = f"EXP-{numero:06d}"
    
    # Crear paciente
    paciente = Paciente(
        **paciente_data.model_dump(),
        numero_expediente=numero_expediente
    )
    
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    
    return paciente

@router.put("/{paciente_id}", response_model=PacienteResponse)
async def update_paciente(
    paciente_id: int,
    paciente_data: PacienteUpdate,
    db: Session = Depends(get_db)
):
    """
    Actualizar un paciente existente.
    """
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    # Validar DPI único si se está actualizando
    if paciente_data.dpi and paciente_data.dpi != paciente.dpi:
        existing = db.query(Paciente).filter(
            Paciente.dpi == paciente_data.dpi,
            Paciente.id != paciente_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un paciente con este DPI"
            )
    
    # Actualizar campos
    update_data = paciente_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(paciente, field, value)
    
    db.commit()
    db.refresh(paciente)
    
    return paciente

@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paciente(
    paciente_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un paciente (soft delete - marca como inactivo).
    """
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    # Soft delete
    paciente.activo = False
    db.commit()
    
    return None
```

---

### Paso 4: Registrar Router

**Archivo**: `backend/app/api/v1/__init__.py`
```python
from fastapi import APIRouter
from app.api.v1.endpoints import auth, usuarios, pacientes  # ← Agregar

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Autenticación"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
api_router.include_router(pacientes.router, prefix="/pacientes", tags=["Pacientes"])  # ← Agregar
```

---

### Paso 5: Crear Migración con Alembic
```bash
cd backend

# Generar migración automática
alembic revision --autogenerate -m "add pacientes table"

# Revisar archivo generado en alembic/versions/

# Aplicar migración
alembic upgrade head
```

**Si no usas Alembic** (Sprint 1 actual):
```python
# En main.py se crea automáticamente
Base.metadata.create_all(bind=engine)
```

---

### Paso 6: Probar en Swagger

1. Iniciar backend: `uvicorn main:app --reload`
2. Abrir: http://localhost:8000/docs
3. Probar cada endpoint:
   - POST /pacientes/ → Crear paciente
   - GET /pacientes/ → Listar pacientes
   - GET /pacientes/{id} → Ver paciente
   - PUT /pacientes/{id} → Actualizar
   - DELETE /pacientes/{id} → Eliminar

---

## ⚛️ Desarrollo de Frontend

### Paso 1: Crear TypeScript Types

**Ubicación**: `frontend/types/`

**Archivo**: `frontend/types/index.ts` (agregar)
```typescript
export interface Paciente {
  id: number;
  numero_expediente: string;
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string; // ISO date string
  sexo: 'M' | 'F';
  dpi?: string;
  direccion?: string;
  telefono1?: string;
  telefono2?: string;
  email?: string;
  estado_civil?: string;
  religion?: string;
  tiene_igss: boolean;
  contacto_emergencia_nombre?: string;
  contacto_emergencia_telefono?: string;
  foto_url?: string;
  activo: boolean;
  created_at: string;
}

export interface PacienteCreate {
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string;
  sexo: 'M' | 'F';
  dpi?: string;
  direccion?: string;
  telefono1?: string;
  telefono2?: string;
  email?: string;
  estado_civil?: string;
  religion?: string;
  tiene_igss: boolean;
  contacto_emergencia_nombre?: string;
  contacto_emergencia_telefono?: string;
}

export interface PacienteListItem {
  id: number;
  numero_expediente: string;
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string;
  telefono1?: string;
  foto_url?: string;
}
```

---

### Paso 2: Crear Servicio de API

**Ubicación**: `frontend/lib/`

**Archivo**: `frontend/lib/pacientes.ts`
```typescript
import api from './api';
import { Paciente, PacienteCreate, PacienteListItem } from '@/types';

export const pacientesService = {
  async getAll(skip: number = 0, limit: number = 100): Promise<PacienteListItem[]> {
    const response = await api.get<PacienteListItem[]>('/pacientes/', {
      params: { skip, limit }
    });
    return response.data;
  },

  async buscar(query: string): Promise<PacienteListItem[]> {
    const response = await api.get<PacienteListItem[]>('/pacientes/buscar', {
      params: { q: query }
    });
    return response.data;
  },

  async getById(id: number): Promise<Paciente> {
    const response = await api.get<Paciente>(`/pacientes/${id}`);
    return response.data;
  },

  async create(data: PacienteCreate): Promise<Paciente> {
    const response = await api.post<Paciente>('/pacientes/', data);
    return response.data;
  },

  async update(id: number, data: Partial<PacienteCreate>): Promise<Paciente> {
    const response = await api.put<Paciente>(`/pacientes/${id}`, data);
    return response.data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/pacientes/${id}`);
  },
};
```

---

### Paso 3: Crear Componentes

**Ubicación**: `frontend/components/pacientes/`

**Archivo**: `frontend/components/pacientes/PacienteCard.tsx`
```typescript
import { PacienteListItem } from '@/types';
import Image from 'next/image';

interface PacienteCardProps {
  paciente: PacienteListItem;
  onClick: () => void;
}

export default function PacienteCard({ paciente, onClick }: PacienteCardProps) {
  const calcularEdad = (fechaNacimiento: string) => {
    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    return edad;
  };

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow cursor-pointer"
    >
      <div className="flex items-center space-x-4">
        {/* Foto */}
        <div className="relative h-16 w-16 rounded-full overflow-hidden bg-gray-200">
          {paciente.foto_url ? (
            <Image
              src={paciente.foto_url}
              alt={`${paciente.nombres} ${paciente.apellidos}`}
              fill
              className="object-cover"
            />
          ) : (
            <div className="h-full w-full flex items-center justify-center text-gray-400 text-2xl">
              👤
            </div>
          )}
        </div>

        {/* Info */}
        <div className="flex-1">
          <h3 className="font-semibold text-gray-900">
            {paciente.nombres} {paciente.apellidos}
          </h3>
          <p className="text-sm text-gray-500">
            {paciente.numero_expediente}
          </p>
          <div className="flex items-center space-x-4 mt-1">
            <span className="text-xs text-gray-600">
              {calcularEdad(paciente.fecha_nacimiento)} años
            </span>
            {paciente.telefono1 && (
              <span className="text-xs text-gray-600">
                📱 {paciente.telefono1}
              </span>
            )}
          </div>
        </div>

        {/* Flecha */}
        <svg
          className="w-5 h-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M9 5l7 7-7 7"
          />
        </svg>
      </div>
    </div>
  );
}
```

---

### Paso 4: Crear Página

**Ubicación**: `frontend/app/dashboard/pacientes/`

**Archivo**: `frontend/app/dashboard/pacientes/page.tsx`
```typescript
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { pacientesService } from '@/lib/pacientes';
import { PacienteListItem } from '@/types';
import PacienteCard from '@/components/pacientes/PacienteCard';

export default function PacientesPage() {
  const router = useRouter();
  const [pacientes, setPacientes] = useState<PacienteListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    cargarPacientes();
  }, []);

  const cargarPacientes = async () => {
    try {
      const data = await pacientesService.getAll();
      setPacientes(data);
    } catch (error) {
      console.error('Error cargando pacientes:', error);
    } finally {
      setLoading(false);
    }
  };

  const buscarPacientes = async (query: string) => {
    if (query.length < 3) {
      cargarPacientes();
      return;
    }

    try {
      const data = await pacientesService.buscar(query);
      setPacientes(data);
    } catch (error) {
      console.error('Error buscando pacientes:', error);
    }
  };

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const query = e.target.value;
    setSearchQuery(query);
    buscarPacientes(query);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Pacientes</h1>
          <p className="text-gray-600">Gestión de expedientes médicos</p>
        </div>
        <button
          onClick={() => router.push('/dashboard/pacientes/nuevo')}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors"
        >
          + Nuevo Paciente
        </button>
      </div>

      {/* Search */}
      <div className="relative">
        <input
          type="text"
          value={searchQuery}
          onChange={handleSearch}
          placeholder="Buscar por nombre, DPI o expediente..."
          className="w-full px-4 py-3 pl-10 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        />
        <svg
          className="absolute left-3 top-3.5 h-5 w-5 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      {/* Lista */}
      {pacientes.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500">No se encontraron pacientes</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {pacientes.map((paciente) => (
            <PacienteCard
              key={paciente.id}
              paciente={paciente}
              onClick={() => router.push(`/dashboard/pacientes/${paciente.id}`)}
            />
          ))}
        </div>
      )}
    </div>
  );
}
```

---

## 🧪 Testing

### Testing Manual

**Backend**:
1. Usar Swagger UI en http://localhost:8000/docs
2. Probar cada endpoint con datos válidos
3. Probar con datos inválidos (errores)
4. Verificar en PostgreSQL que los datos se guardan correctamente

**Frontend**:
1. Navegar por la interfaz
2. Probar formularios
3. Probar búsquedas
4. Verificar responsive (desktop, tablet, móvil)
5. Probar errores de red

### Testing con cURL
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Guardar token
TOKEN="eyJhbGci..."

# Crear paciente
curl -X POST "http://localhost:8000/api/v1/pacientes/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "Juan",
    "apellidos": "Pérez",
    "fecha_nacimiento": "1990-01-15",
    "sexo": "M",
    "telefono1": "12345678"
  }'

# Listar pacientes
curl -X GET "http://localhost:8000/api/v1/pacientes/" \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📝 Convenciones de Código

### Python (Backend)
```python
# Nombres de archivos: snake_case
paciente.py, usuario_service.py

# Nombres de clases: PascalCase
class Paciente:
class UsuarioService:

# Nombres de funciones: snake_case
def get_pacientes():
def crear_usuario():

# Nombres de variables: snake_case
paciente_id = 1
numero_expediente = "EXP-000001"

# Constantes: UPPER_SNAKE_CASE
MAX_PACIENTES = 100
DEFAULT_LIMIT = 50

# Type hints siempre
def get_user(user_id: int) -> Usuario:
    pass

# Docstrings
def create_paciente(data: PacienteCreate) -> Paciente:
    """
    Crear un nuevo paciente.
    
    Args:
        data: Datos del paciente a crear
        
    Returns:
        Paciente creado con ID generado
        
    Raises:
        HTTPException: Si el DPI ya existe
    """
    pass
```

### TypeScript (Frontend)
```typescript
// Nombres de archivos: PascalCase para componentes, camelCase para utils
PacienteCard.tsx, pacientes.ts

// Nombres de interfaces: PascalCase
interface Paciente {}
interface PacienteCreate {}

// Nombres de componentes: PascalCase
export default function PacienteCard() {}

// Nombres de funciones: camelCase
const cargarPacientes = async () => {}
const buscarPacientes = async () => {}

// Nombres de variables: camelCase
const pacienteId = 1;
const numeroExpediente = "EXP-000001";

// Constantes: UPPER_SNAKE_CASE
const MAX_FILE_SIZE = 5 * 1024 * 1024;

// Props types siempre
interface PacienteCardProps {
  paciente: PacienteListItem;
  onClick: () => void;
}
```

---

## 🌿 Git Workflow

### Crear nueva rama
```bash
# Asegurarte de estar en develop
git checkout develop
git pull origin develop

# Crear rama para feature
git checkout -b feature/sprint-2-pacientes

# O para un bugfix
git checkout -b fix/corregir-login-error
```

### Convención de commits
```bash
# Formato: tipo(alcance): descripción

# Tipos:
feat:     Nueva funcionalidad
fix:      Corrección de bug
docs:     Cambios en documentación
style:    Cambios de formato (no afectan código)
refactor: Refactorización
test:     Agregar tests
chore:    Tareas de mantenimiento

# Ejemplos:
git commit -m "feat(pacientes): agregar endpoint de búsqueda"
git commit -m "fix(auth): corregir validación de token expirado"
git commit -m "docs: actualizar README con nuevos endpoints"
git commit -m "style(frontend): aplicar formato Prettier"
```

### Commits frecuentes
```bash
# Hacer commits pequeños y frecuentes
git add backend/app/models/paciente.py
git commit -m "feat(pacientes): agregar modelo Paciente"

git add backend/app/schemas/paciente.py
git commit -m "feat(pacientes): agregar schemas Pydantic"

git add backend/app/api/v1/endpoints/pacientes.py
git commit -m "feat(pacientes): agregar endpoints CRUD"
```

### Push y Pull Request
```bash
# Push de la rama
git push origin feature/sprint-2-pacientes

# Crear Pull Request en GitHub
# Desde: feature/sprint-2-pacientes
# Hacia: develop
# Título: "Sprint 2: Módulo de Gestión de Pacientes"
# Descripción: Lista de cambios y screenshots
```

### Merge
```bash
# Una vez aprobado el PR
git checkout develop
git merge feature/sprint-2-pacientes
git push origin develop

# Eliminar rama local
git branch -d feature/sprint-2-pacientes

# Eliminar rama remota
git push origin --delete feature/sprint-2-pacientes
```

---

## 🎯 Ejemplo Completo: Nueva Feature

### Feature: Agregar foto de perfil al paciente

**User Story**: 
"Como médico, necesito poder subir una foto del paciente para identificarlo visualmente en la lista"

**Pasos**:

#### 1. Backend - Agregar endpoint de upload
```python
# backend/app/api/v1/endpoints/pacientes.py

from fastapi import File, UploadFile
import shutil
from pathlib import Path

@router.post("/{paciente_id}/foto")
async def upload_foto(
    paciente_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Validar paciente existe
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Validar tipo de archivo
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG/PNG")
    
    # Validar tamaño (5 MB)
    file.file.seek(0, 2)
    size = file.file.tell()
    if size > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="La imagen no debe superar 5 MB")
    file.file.seek(0)
    
    # Guardar archivo
    upload_dir = Path("D:/clinica-archivos/pacientes") / str(paciente_id) / "fotos"
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / f"foto_perfil.{file.filename.split('.')[-1]}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Actualizar BD
    paciente.foto_url = f"/pacientes/{paciente_id}/fotos/foto_perfil.{file.filename.split('.')[-1]}"
    db.commit()
    
    return {"message": "Foto subida exitosamente", "url": paciente.foto_url}
```

#### 2. Frontend - Componente de upload
```typescript
// frontend/components/pacientes/FotoUpload.tsx

'use client';

import { useState } from 'react';
import axios from 'axios';

interface FotoUploadProps {
  pacienteId: number;
  onSuccess: (url: string) => void;
}

export default function FotoUpload({ pacienteId, onSuccess }: FotoUploadProps) {
  const [uploading, setUploading] = useState(false);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validar tamaño
    if (file.size > 5 * 1024 * 1024) {
      alert('La imagen no debe superar 5 MB');
      return;
    }

    // Validar tipo
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      alert('Solo se permiten imágenes JPG/PNG');
      return;
    }

    setUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        `http://localhost:8000/api/v1/pacientes/${pacienteId}/foto`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      onSuccess(response.data.url);
      alert('Foto subida exitosamente');
    } catch (error) {
      console.error('Error subiendo foto:', error);
      alert('Error al subir la foto');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Foto de perfil
      </label>
      <input
        type="file"
        accept="image/jpeg,image/png"
        onChange={handleFileChange}
        disabled={uploading}
        className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
      />
      {uploading && (
        <p className="text-sm text-gray-500 mt-2">Subiendo foto...</p>
      )}
    </div>
  );
}
```

#### 3. Testing
```bash
# Backend
curl -X POST "http://localhost:8000/api/v1/pacientes/1/foto" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@foto.jpg"

# Frontend
# Usar la interfaz para seleccionar y subir archivo
```

#### 4. Commit
```bash
git add .
git commit -m "feat(pacientes): agregar upload de foto de perfil

- Backend: endpoint POST /pacientes/{id}/foto
- Frontend: componente FotoUpload
- Validaciones: tipo y tamaño de archivo
- Storage: D:/clinica-archivos/pacientes/{id}/fotos/"

git push origin feature/foto-perfil
```

---

## 📚 Recursos Útiles

### Documentación
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
- Tailwind: https://tailwindcss.com/docs

### Tools
- Swagger UI: http://localhost:8000/docs
- PostgreSQL GUI: pgAdmin, DBeaver
- API Testing: Thunder Client (VS Code), Postman
- Git GUI: GitHub Desktop

### VS Code Extensions
- Python (Microsoft)
- Pylance
- ES7+ React snippets
- Tailwind CSS IntelliSense
- Prettier
- ESLint

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0 - Sprint 1  
**Próxima actualización**: Sprint 2 - Módulo Pacientes