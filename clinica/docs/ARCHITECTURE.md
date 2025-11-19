# 🏗️ Arquitectura del Sistema - Sistema Clínico MEDGAR

## Información General

- **Versión**: 2.0.0
- **Patrón Arquitectónico**: Arquitectura en Capas (Layered Architecture)
- **Estilo API**: RESTful
- **Paradigma**: Backend-Frontend Separation

---

## 📐 Vista General de la Arquitectura
```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENTE (Frontend)                         │
│                     Next.js 14 + TypeScript                         │
│                                                                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │   Páginas    │  │ Componentes  │  │   Services   │            │
│  │   (Pages)    │  │  (UI/shadcn) │  │   (API)      │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
└─────────────────────────────────────────────────────────────────────┘
                              ↓ HTTP/REST ↓
┌─────────────────────────────────────────────────────────────────────┐
│                           API GATEWAY                               │
│                        FastAPI (main.py)                            │
│                                                                     │
│  • CORS Middleware                                                 │
│  • Routing                                                         │
│  • Error Handling                                                  │
│  • Documentation (Swagger/ReDoc)                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                        CAPA DE ROUTERS                              │
│                      (Controladores REST)                           │
│                                                                     │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐        │
│  │  pacientes  │   citas     │  consultas  │  recetas    │        │
│  │   .router   │  .router    │  .router    │  .router    │        │
│  └─────────────┴─────────────┴─────────────┴─────────────┘        │
│  ┌─────────────┬─────────────┬─────────────┬─────────────┐        │
│  │hospitali-   │ laboratorios│   caja      │  farmacia   │        │
│  │zacion.router│  .router    │  .router    │  .router    │        │
│  └─────────────┴─────────────┴─────────────┴─────────────┘        │
│                                                                     │
│  16 routers en total                                               │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    CAPA DE LÓGICA DE NEGOCIO                        │
│                      (Business Logic)                               │
│                                                                     │
│  • Validaciones de negocio                                         │
│  • Cálculos (IMC, saldos, stock)                                  │
│  • Reglas de negocio                                               │
│  • Alertas y notificaciones                                        │
│  • Gestión de estados                                              │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                    CAPA DE ACCESO A DATOS                           │
│                    SQLAlchemy ORM + Models                          │
│                                                                     │
│  • Modelos de datos (31 tablas)                                   │
│  • Relaciones entre entidades                                      │
│  • Consultas y operaciones CRUD                                    │
│  • Transacciones                                                   │
└─────────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────────┐
│                      BASE DE DATOS                                  │
│                      PostgreSQL 15                                  │
│                                                                     │
│  • 31 tablas relacionales                                          │
│  • Índices optimizados                                             │
│  • Constraints y FK                                                │
│  • Backups automáticos                                             │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                    SISTEMA DE ARCHIVOS                              │
│                    D:\clinica-archivos\                             │
│                                                                     │
│  • Fotos de pacientes                                              │
│  • Archivos multimedia                                             │
│  • Documentos PDF                                                  │
│  • Backups                                                         │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔧 Arquitectura Detallada del Backend

### Estructura de Carpetas
```
clinica/backend/
│
├── main.py                          # Entry point, API Gateway
│
├── database.py                      # Configuración de BD
│
├── create_simple_tables.py          # Modelos SQLAlchemy
│
├── app/
│   └── routers/                     # Routers (Controladores)
│       ├── pacientes.py             # 9 endpoints
│       ├── citas.py                 # 7 endpoints
│       ├── lista_espera.py          # 4 endpoints
│       ├── medicamentos.py          # 5 endpoints
│       ├── consultas.py             # 5 endpoints
│       ├── antecedentes.py          # 5 endpoints
│       ├── vacunas.py               # 4 endpoints
│       ├── interconsultas.py        # 4 endpoints
│       ├── recetas.py               # 4 endpoints
│       ├── hospitalizacion.py       # 11 endpoints
│       ├── notas_medicas.py         # 3 endpoints
│       ├── ordenes_medicas.py       # 3 endpoints
│       ├── laboratorios.py          # 6 endpoints
│       ├── caja.py                  # 13 endpoints
│       ├── farmacia.py              # 15 endpoints
│       └── reportes.py              # 5 endpoints
│
├── init_data_completo.py            # Script de inicialización
│
├── requirements.txt                 # Dependencias Python
│
└── venv/                            # Entorno virtual
```

---

## 🎯 Patrón de Diseño: Arquitectura en Capas

### 1. Capa de Presentación (API Layer)

**Responsabilidad**: Exponer endpoints REST y manejar HTTP

**Componentes**:
- `main.py`: FastAPI app, CORS, routing
- Routers individuales por módulo

**Características**:
```python
# Ejemplo de estructura de router
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(prefix="/api/pacientes", tags=["Pacientes"])

@router.post("/")
def crear_paciente(paciente: PacienteCreate, db: Session = Depends(get_db)):
    # Validación de entrada
    # Lógica de negocio
    # Acceso a datos
    # Respuesta
    pass
```

**Responsabilidades**:
- Validación de entrada (Pydantic)
- Serialización/Deserialización (JSON ↔ Modelos)
- Manejo de errores HTTP
- Documentación automática (Swagger)

---

### 2. Capa de Lógica de Negocio (Business Logic Layer)

**Responsabilidad**: Implementar reglas de negocio y lógica compleja

**Ejemplos de Lógica de Negocio**:

#### Cálculo de IMC
```python
# En consultas.py
if consulta.peso and consulta.talla and consulta.talla > 0:
    imc = consulta.peso / ((consulta.talla / 100) ** 2)
    response.imc = round(imc, 2)
```

#### Validación de Stock en Farmacia
```python
# En farmacia.py
if producto.stock_actual < cantidad:
    raise HTTPException(
        status_code=400,
        detail=f"Stock insuficiente. Disponible: {producto.stock_actual}"
    )
```

#### Cambio Automático de Estado de Cama
```python
# En hospitalizacion.py
if cama.estado != EstadoCamaEnum.disponible:
    raise HTTPException(status_code=400, detail="Cama no disponible")

# Al ingresar paciente
cama.estado = EstadoCamaEnum.ocupada

# Al dar egreso
cama.estado = EstadoCamaEnum.limpieza
```

#### Cálculo de Saldos en Cuentas por Cobrar
```python
# En caja.py
cuenta.monto_pagado += abono.monto_pagado
cuenta.saldo = cuenta.monto_total - cuenta.monto_pagado

if cuenta.saldo <= 0:
    cuenta.pagado = True
    cuenta.saldo = 0
```

#### Alertas de Inventario
```python
# En farmacia.py
response.alerta_stock = producto.stock_actual <= producto.stock_minimo

if producto.fecha_vencimiento:
    dias_vencimiento = (producto.fecha_vencimiento - date.today()).days
    response.alerta_vencimiento = dias_vencimiento <= 30
```

---

### 3. Capa de Acceso a Datos (Data Access Layer)

**Responsabilidad**: Interactuar con la base de datos

**Componentes**:
- SQLAlchemy Models (`create_simple_tables.py`)
- Session management (`database.py`)

**Patrón Repository Implícito**:
```python
# Consultas comunes
db.query(Paciente).filter(Paciente.id == paciente_id).first()
db.query(Cita).filter(Cita.medico_id == medico_id).all()
db.add(nuevo_paciente)
db.commit()
db.refresh(nuevo_paciente)
```

**Relaciones**:
```python
# Ejemplo: Consulta con paciente y médico
class Consulta(Base):
    __tablename__ = "consultas"
    
    paciente_id = Column(Integer, ForeignKey("pacientes.id"))
    medico_id = Column(Integer, ForeignKey("usuarios.id"))
    
    # Relaciones (opcional, por implementar)
    # paciente = relationship("Paciente", back_populates="consultas")
    # medico = relationship("Usuario", back_populates="consultas")
```

---

### 4. Capa de Persistencia (Database Layer)

**Responsabilidad**: Almacenamiento físico de datos

**Configuración**:
```python
# database.py
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password@localhost/clinica_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

**Características**:
- Pool de conexiones
- Transacciones ACID
- Constraints y Foreign Keys
- Índices optimizados

---

## 🔄 Flujo de Datos (Request-Response)

### Ejemplo: Crear una Consulta
```
1. CLIENTE (Frontend)
   POST http://localhost:8000/api/consultas
   Body: { paciente_id: 1, medico_id: 2, ... }
   
                    ↓

2. API GATEWAY (main.py)
   • Recibe request
   • Aplica CORS
   • Rutea a consultas.router
   
                    ↓

3. ROUTER (consultas.py)
   • Valida entrada con Pydantic (ConsultaCreate)
   • Obtiene sesión de BD (Depends(get_db))
   
                    ↓

4. BUSINESS LOGIC (en router)
   • Verifica que paciente existe
   • Verifica que médico existe
   • Calcula IMC si hay peso y talla
   
                    ↓

5. DATA ACCESS (SQLAlchemy)
   • db.add(nueva_consulta)
   • db.commit()
   • db.refresh(nueva_consulta)
   
                    ↓

6. DATABASE (PostgreSQL)
   • INSERT INTO consultas ...
   • COMMIT
   • RETURN inserted row
   
                    ↓

7. RESPONSE (JSON)
   • Serializa con Pydantic (ConsultaResponse)
   • Status: 201 Created
   • Body: { id: 1, imc: 24.05, ... }
   
                    ↓

8. CLIENTE (Frontend)
   • Recibe respuesta
   • Actualiza UI
```

---

## 🔐 Seguridad (Por Implementar en Sprint 11)

### Autenticación JWT

**Flujo Propuesto**:
```
1. Login
   POST /api/auth/login
   { email, password }
   
2. Validación
   • Verificar credenciales
   • Generar JWT token
   
3. Response
   { token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...", user: {...} }
   
4. Requests Posteriores
   Headers: { Authorization: "Bearer <token>" }
   
5. Middleware
   • Verificar token
   • Extraer user_id y rol
   • Permitir/Denegar acceso
```

### Autorización por Roles

**Matriz de Permisos** (Propuesta):

| Endpoint | Médico | Enfermera | Recepcionista | Admin |
|----------|--------|-----------|---------------|-------|
| GET /pacientes | ✅ | ✅ | ✅ | ✅ |
| POST /pacientes | ✅ | ❌ | ✅ | ✅ |
| POST /consultas | ✅ | ❌ | ❌ | ✅ |
| POST /recetas | ✅ | ❌ | ❌ | ✅ |
| POST /hospitalizacion/ingresos | ✅ | ❌ | ❌ | ✅ |
| POST /ordenes-medicas | ✅ | ❌ | ❌ | ✅ |
| POST /notas-medicas | ✅ | ✅ | ❌ | ✅ |
| POST /caja/apertura | ❌ | ❌ | ✅ | ✅ |
| GET /reportes/dashboard | ❌ | ❌ | ❌ | ✅ |
| POST /farmacia/compras | ❌ | ❌ | ❌ | ✅ |

---

## 📊 Patrones de Diseño Utilizados

### 1. Dependency Injection

**Uso**: Inyección de sesión de base de datos
```python
from fastapi import Depends
from database import get_db

@router.post("/")
def crear_paciente(
    paciente: PacienteCreate,
    db: Session = Depends(get_db)  # ← Dependency Injection
):
    pass
```

**Ventajas**:
- Testabilidad
- Separación de responsabilidades
- Flexibilidad

---

### 2. Repository Pattern (Implícito)

**Uso**: Acceso a datos centralizado en routers
```python
# Operaciones CRUD encapsuladas
def obtener_paciente(paciente_id: int, db: Session):
    return db.query(Paciente).filter(Paciente.id == paciente_id).first()

def crear_paciente(paciente: PacienteCreate, db: Session):
    db_paciente = Paciente(**paciente.model_dump())
    db.add(db_paciente)
    db.commit()
    return db_paciente
```

---

### 3. DTO Pattern (Data Transfer Object)

**Uso**: Schemas de Pydantic
```python
# Input DTO
class ConsultaCreate(BaseModel):
    paciente_id: int
    medico_id: int
    motivo_consulta: str
    # ...

# Output DTO
class ConsultaResponse(BaseModel):
    id: int
    paciente_id: int
    imc: Optional[float]  # Campo calculado
    created_at: datetime
    
    class Config:
        from_attributes = True
```

**Ventajas**:
- Validación automática
- Documentación clara
- Separación modelo interno vs. API

---

### 4. Factory Pattern (Implícito)

**Uso**: Creación de objetos complejos
```python
# En recetas.py - Crear receta con múltiples medicamentos
def crear_receta(receta: RecetaCreate, db: Session):
    # Factory: crear receta + detalles
    db_receta = Receta(...)
    db.add(db_receta)
    db.flush()  # Obtener ID
    
    for med in receta.medicamentos:
        detalle = RecetaDetalle(receta_id=db_receta.id, ...)
        db.add(detalle)
    
    db.commit()
    return db_receta
```

---

### 5. Strategy Pattern (En Validaciones)

**Uso**: Diferentes estrategias de validación según contexto
```python
# Validación según tipo de orden médica
if orden.tipo == TipoOrdenEnum.medicamento:
    # Validar que medicamento_id existe
    # Validar dosis, frecuencia, vía
    pass
elif orden.tipo == TipoOrdenEnum.dieta:
    # Solo validar descripción
    pass
```

---

## 🔄 Manejo de Transacciones

### Transacciones Automáticas
```python
@router.post("/ventas")
def crear_venta(venta: VentaCreate, db: Session):
    try:
        # Todo dentro de una transacción
        db_venta = VentaFarmacia(...)
        db.add(db_venta)
        db.flush()
        
        for prod in venta.productos:
            # Crear detalle
            detalle = DetalleVenta(...)
            db.add(detalle)
            
            # Actualizar stock (crítico)
            producto.stock_actual -= prod.cantidad
        
        db.commit()  # ← Commit si todo OK
        
    except Exception as e:
        db.rollback()  # ← Rollback si hay error
        raise HTTPException(status_code=500, detail=str(e))
```

**Garantías ACID**:
- **Atomicity**: Todo o nada
- **Consistency**: Stock siempre correcto
- **Isolation**: Sin conflictos concurrentes
- **Durability**: Cambios persistentes

---

## 📈 Escalabilidad

### Escalabilidad Vertical (Actual)

**Hardware**:
- CPU: AMD Ryzen 5 7520U (4 cores)
- RAM: 16 GB
- Disco: 500 GB SSD

**Capacidad Estimada**:
- Usuarios concurrentes: 10-20
- Pacientes en BD: 10,000+
- Transacciones/día: 500+

### Escalabilidad Horizontal (Futuro)

**Preparación para Múltiples Sucursales**:
```
Sucursal 1 (Huehuetenango)
    ↓
    API Local → BD Local
    ↓
    Sincronización ← → Servidor Central
    ↑
Sucursal 2 (Nueva)
    ↑
    API Local → BD Local
```

**Estrategias**:
- Base de datos por sucursal
- Replicación de catálogos (medicamentos, tipos de estudio)
- Sincronización de pacientes compartidos
- Reportes consolidados en servidor central

---

## 🔧 Configuración y Variables de Entorno

### Archivo: `.env` (Por Crear)
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/clinica_db

# Server
HOST=0.0.0.0
PORT=8000

# Security (Futuro)
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Storage
UPLOAD_DIR=D:/clinica-archivos
MAX_FILE_SIZE_MB=50

# Backup
BACKUP_DIR=D:/clinica-backups
BACKUP_RETENTION_DAYS=30

# Email (Futuro)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=clinica@example.com
SMTP_PASSWORD=password

# Twilio (Para recordatorios - Futuro)
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+14155238886

# FEL (Futuro)
FEL_API_KEY=your_fel_api_key
FEL_API_URL=https://api-fel.com
```

---

## 🧪 Testing (Por Implementar)

### Estructura Propuesta
```
clinica/backend/tests/
│
├── test_pacientes.py
├── test_citas.py
├── test_consultas.py
├── test_hospitalizacion.py
├── test_farmacia.py
└── test_reportes.py
```

### Ejemplo de Test
```python
# test_pacientes.py
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_crear_paciente():
    response = client.post(
        "/api/pacientes",
        json={
            "nombres": "Test",
            "apellidos": "Paciente",
            "fecha_nacimiento": "1990-01-01",
            "dpi": "1234567890101",
            "genero": "Masculino"
        }
    )
    assert response.status_code == 201
    assert response.json()["nombres"] == "Test"
```

---

## 📊 Monitoreo y Logging (Por Implementar)

### Logging Propuesto
```python
import logging

# Configuración
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('clinica.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Uso en routers
@router.post("/")
def crear_paciente(...):
    logger.info(f"Creando paciente: {paciente.nombres} {paciente.apellidos}")
    # ...
    logger.info(f"Paciente creado con ID: {db_paciente.id}")
```

### Métricas Importantes

- Requests por endpoint
- Tiempo de respuesta promedio
- Errores 4xx y 5xx
- Uso de CPU y RAM
- Transacciones de BD por segundo
- Espacio en disco utilizado

---

## 🚀 Performance

### Optimizaciones Implementadas

#### 1. Índices en Base de Datos
```python
# En create_simple_tables.py
class Paciente(Base):
    # ...
    __table_args__ = (
        Index('idx_pacientes_dpi', 'dpi'),
        Index('idx_pacientes_nombres', 'nombres'),
    )
```

#### 2. Paginación
```python
@router.get("/")
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = ...):
    return db.query(Paciente).offset(skip).limit(limit).all()
```

#### 3. Eager Loading (Por Implementar)
```python
# Cargar relaciones en una sola query
db.query(Consulta).options(
    joinedload(Consulta.paciente),
    joinedload(Consulta.medico)
).all()
```

### Optimizaciones Futuras

- Caché de catálogos (medicamentos, tipos de estudio)
- Compresión de respuestas (gzip)
- CDN para archivos estáticos
- Background tasks para operaciones pesadas
- Database connection pooling optimizado

---

## 🔄 Versionamiento de API (Futuro)

### Estrategia Propuesta
```python
# v1/
@app.include_router(pacientes.router, prefix="/api/v1")

# v2/ (cuando sea necesario)
@app.include_router(pacientes_v2.router, prefix="/api/v2")
```

**Política de Deprecación**:
- Anunciar con 6 meses de anticipación
- Mantener 2 versiones simultáneas
- Documentar cambios breaking

---

## 📚 Documentación de Código

### Estándares

**Docstrings**:
```python
def crear_paciente(paciente: PacienteCreate, db: Session):
    """
    Crear un nuevo paciente en el sistema.
    
    Args:
        paciente: Datos del paciente a crear
        db: Sesión de base de datos
    
    Returns:
        PacienteResponse: Paciente creado con ID asignado
    
    Raises:
        HTTPException 400: Si el DPI ya existe
    """
    pass
```

**Type Hints**:
```python
from typing import List, Optional

def obtener_pacientes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
) -> List[PacienteResponse]:
    pass
```

---

## 🎯 Principios SOLID Aplicados

### Single Responsibility Principle (SRP)
- Cada router maneja un solo módulo
- Cada endpoint tiene una responsabilidad clara

### Open/Closed Principle (OCP)
- Fácil agregar nuevos routers sin modificar existentes
- Extensible mediante Pydantic models

### Liskov Substitution Principle (LSP)
- Schemas base reutilizables (Create, Update, Response)

### Interface Segregation Principle (ISP)
- Schemas específicos por operación
- No forzar campos innecesarios

### Dependency Inversion Principle (DIP)
- Dependencia de abstracción (Session) no implementación
- FastAPI Depends para inyección

---

## 📝 Convenciones de Código

### Naming Conventions

**Archivos**: `snake_case.py`
- `pacientes.py`, `lista_espera.py`

**Clases**: `PascalCase`
- `PacienteCreate`, `ConsultaResponse`

**Funciones**: `snake_case`
- `crear_paciente()`, `obtener_consultas()`

**Variables**: `snake_case`
- `paciente_id`, `fecha_nacimiento`

**Constantes**: `UPPER_SNAKE_CASE`
- `MAX_FILE_SIZE`, `DEFAULT_PAGE_SIZE`

### Estructura de Endpoint
```python
@router.post("/", response_model=ResponseSchema, status_code=201)
def crear_entidad(
    entidad: CreateSchema,
    db: Session = Depends(get_db)
):
    """Docstring detallado"""
    
    # 1. Validaciones
    # 2. Lógica de negocio
    # 3. Acceso a datos
    # 4. Response
    
    return response
```

---

## 🔮 Roadmap Técnico

### Sprint 11: Autenticación y Seguridad
- [ ] JWT Authentication
- [ ] Autorización por roles
- [ ] Encriptación de datos sensibles
- [ ] Logs de auditoría

### Sprint 12: Optimización
- [ ] Caching de catálogos
- [ ] Query optimization
- [ ] Background tasks
- [ ] Performance monitoring

### Futuro: Multi-Tenancy
- [ ] Arquitectura multi-sucursal
- [ ] Sincronización de datos
- [ ] Reportes consolidados

---

**Última actualización**: Enero 2025  
**Versión**: 2.0.0