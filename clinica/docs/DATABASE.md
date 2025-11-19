# 🗂️ Guía de Base de Datos - Sistema Clínico MEDGAR

Documentación completa del esquema de base de datos y gestión con PostgreSQL.

## 📋 Índice

1. [Esquema General](#esquema-general)
2. [Tablas del Sistema](#tablas-del-sistema)
3. [Relaciones y Constraints](#relaciones-y-constraints)
4. [Migraciones con Alembic](#migraciones-con-alembic)
5. [Queries Comunes](#queries-comunes)
6. [Backup y Restore](#backup-y-restore)
7. [Performance y Optimización](#performance-y-optimización)
8. [Seeds y Datos de Prueba](#seeds-y-datos-de-prueba)

---

## 🏗️ Esquema General

### Diagrama ER Completo (Planificado)
```
                                ┌─────────────────┐
                                │     roles       │
                                ├─────────────────┤
                                │ id (PK)        │
                   ┌────────────│ nombre         │
                   │            │ descripcion    │
                   │            └─────────────────┘
                   │                     │
                   │                     │
                   │            ┌─────────────────┐
                   │            │   permisos      │
                   │            ├─────────────────┤
                   │            │ id (PK)        │
                   │       ┌────│ nombre         │
                   │       │    │ descripcion    │
                   │       │    │ modulo         │
                   │       │    └─────────────────┘
                   │       │             │
                   │       │             │
                   │  ┌────▼─────────────▼────┐
                   │  │   rol_permisos        │
                   │  ├───────────────────────┤
                   │  │ id (PK)              │
                   │  │ rol_id (FK)          │
                   │  │ permiso_id (FK)      │
                   │  └───────────────────────┘
                   │
                   │
        ┌──────────▼──────────┐
        │     usuarios        │
        ├─────────────────────┤
        │ id (PK)            │◄────────────────┐
        │ username (UK)      │                 │
        │ email (UK)         │                 │
        │ password_hash      │                 │
        │ nombres            │                 │
        │ apellidos          │                 │
        │ rol_id (FK)        │                 │
        │ activo             │                 │
        │ created_at         │                 │
        │ updated_at         │                 │
        └────────┬────────────┘                 │
                 │                              │
                 │                              │
        ┌────────▼──────────┐                  │
        │   pacientes       │                  │
        ├───────────────────┤                  │
        │ id (PK)          │                  │
        │ numero_expediente│                  │
        │ dpi (UK)         │                  │
        │ nombres          │                  │
        │ apellidos        │                  │
        │ fecha_nacimiento │                  │
        │ sexo             │                  │
        │ direccion        │                  │
        │ telefono1        │                  │
        │ telefono2        │                  │
        │ email            │                  │
        │ estado_civil     │                  │
        │ religion         │                  │
        │ tiene_igss       │                  │
        │ contacto_emerg..│                  │
        │ foto_url         │                  │
        │ activo           │                  │
        │ created_at       │                  │
        │ created_by (FK)  │──────────────────┘
        │ updated_at       │
        │ updated_by (FK)  │
        └────────┬──────────┘
                 │
                 ├──────────────────────────┐
                 │                          │
        ┌────────▼──────────┐      ┌───────▼───────────┐
        │ archivos_paciente │      │   consultas       │
        ├───────────────────┤      ├───────────────────┤
        │ id (PK)          │      │ id (PK)          │
        │ paciente_id (FK) │      │ paciente_id (FK) │
        │ tipo_archivo     │      │ medico_id (FK)   │
        │ categoria        │      │ fecha_consulta   │
        │ url              │      │ motivo_consulta  │
        │ created_at       │      │ historia_actual  │
        └───────────────────┘      │ signos_vitales   │
                                   │ diagnostico      │
                                   │ plan_tratamiento │
                                   │ created_at       │
                                   └───────────────────┘
```

---

## 📊 Tablas del Sistema

### Sprint 1 - Implementadas

#### 1. `roles`

**Propósito**: Definir roles del sistema con sus permisos asociados
```sql
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    descripcion TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_roles_nombre ON roles(nombre);
```

**Datos iniciales**:
```sql
INSERT INTO roles (nombre, descripcion) VALUES
('Administrador', 'Acceso total al sistema'),
('Médico', 'Acceso a pacientes, historia clínica, agenda propia, recetas, hospitalización y laboratorios'),
('Enfermera', 'Acceso a pacientes, signos vitales, medicamentos, notas de enfermería y hospitalización'),
('Recepcionista', 'Acceso a agenda, citas, caja y datos básicos de pacientes');
```

---

#### 2. `permisos`

**Propósito**: Permisos granulares del sistema
```sql
CREATE TABLE permisos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL,
    descripcion TEXT,
    modulo VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_permisos_modulo ON permisos(modulo);
```

**Estructura de permisos**:
```
modulo.accion

Ejemplos:
- pacientes.ver
- pacientes.crear
- pacientes.editar
- pacientes.eliminar
- historias.ver
- historias.crear
- recetas.crear
- caja.abrir
```

---

#### 3. `rol_permisos`

**Propósito**: Tabla intermedia entre roles y permisos (Many-to-Many)
```sql
CREATE TABLE rol_permisos (
    id SERIAL PRIMARY KEY,
    rol_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    permiso_id INTEGER NOT NULL REFERENCES permisos(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(rol_id, permiso_id)
);

-- Índices
CREATE INDEX idx_rol_permisos_rol ON rol_permisos(rol_id);
CREATE INDEX idx_rol_permisos_permiso ON rol_permisos(permiso_id);
```

---

#### 4. `usuarios`

**Propósito**: Usuarios del sistema (médicos, enfermeras, recepcionistas, admin)
```sql
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    rol_id INTEGER NOT NULL REFERENCES roles(id),
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices
CREATE INDEX idx_usuarios_username ON usuarios(username);
CREATE INDEX idx_usuarios_email ON usuarios(email);
CREATE INDEX idx_usuarios_rol ON usuarios(rol_id);
CREATE INDEX idx_usuarios_activo ON usuarios(activo);
```

**Constraints**:
- `username`: 3-50 caracteres, único
- `email`: Formato válido, único
- `password_hash`: Bcrypt hash (60 caracteres)
- `nombres`, `apellidos`: 2-100 caracteres
- `rol_id`: Debe existir en tabla `roles`

---

#### 5. `logs_auditoria`

**Propósito**: Registro de acciones críticas para auditoría
```sql
CREATE TABLE logs_auditoria (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion VARCHAR(50) NOT NULL,
    modulo VARCHAR(50) NOT NULL,
    descripcion TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_logs_usuario ON logs_auditoria(usuario_id);
CREATE INDEX idx_logs_modulo ON logs_auditoria(modulo);
CREATE INDEX idx_logs_fecha ON logs_auditoria(created_at);
```

**Acciones registradas**:
- `login`, `logout`
- `crear`, `editar`, `eliminar` (por módulo)
- `ver_historia_clinica`
- `imprimir_receta`
- `facturar`

---

### Sprint 2+ - Planificadas

#### 6. `pacientes`

**Propósito**: Información demográfica de pacientes
```sql
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    numero_expediente VARCHAR(20) UNIQUE NOT NULL,
    dpi VARCHAR(13) UNIQUE,
    
    -- Información Personal
    nombres VARCHAR(100) NOT NULL,
    apellidos VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    sexo CHAR(1) NOT NULL CHECK (sexo IN ('M', 'F')),
    
    -- Contacto
    direccion VARCHAR(500),
    telefono1 VARCHAR(8),
    telefono2 VARCHAR(8),
    email VARCHAR(100),
    
    -- Datos Adicionales
    estado_civil VARCHAR(20),
    religion VARCHAR(50),
    tiene_igss BOOLEAN DEFAULT FALSE,
    
    -- Contacto de Emergencia
    contacto_emergencia_nombre VARCHAR(100),
    contacto_emergencia_telefono VARCHAR(8),
    
    -- Foto
    foto_url VARCHAR(255),
    
    -- Control
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id),
    updated_at TIMESTAMP WITH TIME ZONE,
    updated_by INTEGER REFERENCES usuarios(id)
);

-- Índices
CREATE INDEX idx_pacientes_expediente ON pacientes(numero_expediente);
CREATE INDEX idx_pacientes_dpi ON pacientes(dpi);
CREATE INDEX idx_pacientes_nombre ON pacientes(nombres, apellidos);
CREATE INDEX idx_pacientes_fecha_nac ON pacientes(fecha_nacimiento);
CREATE INDEX idx_pacientes_activo ON pacientes(activo);

-- Full-text search (futuro)
CREATE INDEX idx_pacientes_busqueda ON pacientes 
    USING gin(to_tsvector('spanish', nombres || ' ' || apellidos));
```

---

#### 7. `antecedentes`

**Propósito**: Antecedentes médicos del paciente
```sql
CREATE TABLE antecedentes (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id) ON DELETE CASCADE,
    
    -- Tipos de antecedentes
    tipo VARCHAR(50) NOT NULL, -- 'patologico', 'quirurgico', 'traumatico', 'alergico', 'ginecologico', 'obstetrico'
    
    -- Contenido
    descripcion TEXT NOT NULL,
    fecha_diagnostico DATE,
    observaciones TEXT,
    
    -- Control
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES usuarios(id)
);

-- Índices
CREATE INDEX idx_antecedentes_paciente ON antecedentes(paciente_id);
CREATE INDEX idx_antecedentes_tipo ON antecedentes(tipo);
```

---

#### 8. `consultas`

**Propósito**: Registro de consultas médicas
```sql
CREATE TABLE consultas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
    medico_id INTEGER NOT NULL REFERENCES usuarios(id),
    
    -- Fecha y tipo
    fecha_consulta TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    tipo_consulta VARCHAR(50), -- 'primera_vez', 'reconsulta', 'control', 'emergencia'
    
    -- Contenido
    motivo_consulta TEXT NOT NULL,
    historia_enfermedad_actual TEXT,
    examen_fisico TEXT,
    diagnostico TEXT,
    plan_tratamiento TEXT,
    
    -- Signos vitales (JSON)
    signos_vitales JSONB,
    
    -- Control
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_consultas_paciente ON consultas(paciente_id);
CREATE INDEX idx_consultas_medico ON consultas(medico_id);
CREATE INDEX idx_consultas_fecha ON consultas(fecha_consulta);

-- Ejemplo de signos_vitales JSON
/*
{
  "presion_arterial": "120/80",
  "frecuencia_cardiaca": 72,
  "temperatura": 36.5,
  "saturacion_oxigeno": 98,
  "frecuencia_respiratoria": 16,
  "peso": 70.5,
  "talla": 170,
  "imc": 24.4
}
*/
```

---

#### 9. `recetas`

**Propósito**: Recetas médicas
```sql
CREATE TABLE recetas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
    consulta_id INTEGER REFERENCES consultas(id),
    medico_id INTEGER NOT NULL REFERENCES usuarios(id),
    
    fecha_emision TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    indicaciones_generales TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE receta_detalle (
    id SERIAL PRIMARY KEY,
    receta_id INTEGER NOT NULL REFERENCES recetas(id) ON DELETE CASCADE,
    medicamento_id INTEGER REFERENCES medicamentos(id),
    medicamento_nombre VARCHAR(200) NOT NULL,
    presentacion VARCHAR(100),
    dosis VARCHAR(100) NOT NULL,
    frecuencia VARCHAR(100) NOT NULL,
    duracion VARCHAR(100) NOT NULL,
    via_administracion VARCHAR(50),
    orden INTEGER NOT NULL
);

-- Índices
CREATE INDEX idx_recetas_paciente ON recetas(paciente_id);
CREATE INDEX idx_recetas_medico ON recetas(medico_id);
CREATE INDEX idx_recetas_fecha ON recetas(fecha_emision);
```

---

#### 10. `medicamentos`

**Propósito**: Catálogo de medicamentos
```sql
CREATE TABLE medicamentos (
    id SERIAL PRIMARY KEY,
    nombre_generico VARCHAR(200) NOT NULL,
    nombre_comercial VARCHAR(200),
    presentacion VARCHAR(100),
    concentracion VARCHAR(50),
    via_administracion VARCHAR(50),
    categoria VARCHAR(50),
    interacciones TEXT,
    contraindicaciones TEXT,
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_medicamentos_generico ON medicamentos(nombre_generico);
CREATE INDEX idx_medicamentos_comercial ON medicamentos(nombre_comercial);
CREATE INDEX idx_medicamentos_categoria ON medicamentos(categoria);
```

---

#### 11. `citas`

**Propósito**: Agenda médica
```sql
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
    medico_id INTEGER NOT NULL REFERENCES usuarios(id),
    
    fecha_hora TIMESTAMP WITH TIME ZONE NOT NULL,
    duracion_minutos INTEGER DEFAULT 20,
    tipo_cita VARCHAR(50), -- 'primera_vez', 'reconsulta', 'control', 'procedimiento'
    
    motivo VARCHAR(255),
    observaciones TEXT,
    
    estado VARCHAR(20) DEFAULT 'programada', -- 'programada', 'confirmada', 'completada', 'cancelada', 'no_asistio'
    
    -- Recordatorios
    recordatorio_enviado BOOLEAN DEFAULT FALSE,
    confirmado BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Índices
CREATE INDEX idx_citas_paciente ON citas(paciente_id);
CREATE INDEX idx_citas_medico ON citas(medico_id);
CREATE INDEX idx_citas_fecha ON citas(fecha_hora);
CREATE INDEX idx_citas_estado ON citas(estado);

-- Constraint: No permitir citas duplicadas para mismo médico a la misma hora
CREATE UNIQUE INDEX idx_citas_medico_fecha ON citas(medico_id, fecha_hora) 
    WHERE estado NOT IN ('cancelada');
```

---

#### 12. `hospitalizacion`

**Propósito**: Control de pacientes hospitalizados
```sql
CREATE TABLE camas (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(10) UNIQUE NOT NULL,
    estado VARCHAR(20) DEFAULT 'disponible', -- 'disponible', 'ocupada', 'limpieza', 'mantenimiento'
    ubicacion VARCHAR(100)
);

CREATE TABLE hospitalizaciones (
    id SERIAL PRIMARY KEY,
    paciente_id INTEGER NOT NULL REFERENCES pacientes(id),
    medico_responsable_id INTEGER NOT NULL REFERENCES usuarios(id),
    cama_id INTEGER REFERENCES camas(id),
    
    fecha_ingreso TIMESTAMP WITH TIME ZONE NOT NULL,
    fecha_egreso TIMESTAMP WITH TIME ZONE,
    
    diagnostico_ingreso TEXT NOT NULL,
    diagnostico_egreso TEXT,
    
    motivo_hospitalizacion TEXT,
    condicion_egreso VARCHAR(50), -- 'mejorado', 'curado', 'referido', 'fallecido', 'voluntario'
    
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE notas_medicas (
    id SERIAL PRIMARY KEY,
    hospitalizacion_id INTEGER NOT NULL REFERENCES hospitalizaciones(id),
    medico_id INTEGER NOT NULL REFERENCES usuarios(id),
    
    tipo VARCHAR(50) NOT NULL, -- 'ingreso', 'evolucion', 'procedimiento', 'operatoria', 'egreso'
    
    contenido TEXT NOT NULL,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_hospitalizaciones_paciente ON hospitalizaciones(paciente_id);
CREATE INDEX idx_hospitalizaciones_cama ON hospitalizaciones(cama_id);
CREATE INDEX idx_hospitalizaciones_activo ON hospitalizaciones(activo);
```

---

#### 13. `inventario`

**Propósito**: Control de farmacia e insumos
```sql
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(20) NOT NULL, -- 'medicamento', 'insumo'
    codigo VARCHAR(50) UNIQUE,
    nombre VARCHAR(200) NOT NULL,
    presentacion VARCHAR(100),
    categoria VARCHAR(50),
    
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    
    precio_compra DECIMAL(10,2),
    precio_venta DECIMAL(10,2),
    
    lote VARCHAR(50),
    fecha_vencimiento DATE,
    
    activo BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE movimientos_inventario (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER NOT NULL REFERENCES productos(id),
    tipo_movimiento VARCHAR(20) NOT NULL, -- 'entrada', 'salida', 'ajuste'
    cantidad INTEGER NOT NULL,
    motivo VARCHAR(100),
    referencia VARCHAR(100), -- Ej: número de factura, receta
    usuario_id INTEGER REFERENCES usuarios(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Índices
CREATE INDEX idx_productos_nombre ON productos(nombre);
CREATE INDEX idx_productos_categoria ON productos(categoria);
CREATE INDEX idx_movimientos_producto ON movimientos_inventario(producto_id);
CREATE INDEX idx_movimientos_fecha ON movimientos_inventario(created_at);
```

---

#### 14. `facturacion`

**Propósito**: Facturación FEL Guatemala
```sql
CREATE TABLE facturas (
    id SERIAL PRIMARY KEY,
    numero_factura VARCHAR(50) UNIQUE NOT NULL,
    uuid_fel VARCHAR(100) UNIQUE, -- UUID del certificador
    
    paciente_id INTEGER REFERENCES pacientes(id),
    
    fecha_emision TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    subtotal DECIMAL(10,2) NOT NULL,
    descuento DECIMAL(10,2) DEFAULT 0,
    total DECIMAL(10,2) NOT NULL,
    
    forma_pago VARCHAR(20), -- 'efectivo', 'transferencia'
    
    estado VARCHAR(20) DEFAULT 'emitida', -- 'emitida', 'anulada'
    fecha_anulacion TIMESTAMP WITH TIME ZONE,
    motivo_anulacion TEXT,
    
    xml_url VARCHAR(255),
    
    created_by INTEGER REFERENCES usuarios(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE factura_detalle (
    id SERIAL PRIMARY KEY,
    factura_id INTEGER NOT NULL REFERENCES facturas(id) ON DELETE CASCADE,
    descripcion VARCHAR(255) NOT NULL,
    cantidad INTEGER NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL
);

-- Índices
CREATE INDEX idx_facturas_numero ON facturas(numero_factura);
CREATE INDEX idx_facturas_uuid ON facturas(uuid_fel);
CREATE INDEX idx_facturas_paciente ON facturas(paciente_id);
CREATE INDEX idx_facturas_fecha ON facturas(fecha_emision);
```

---

## 🔗 Relaciones y Constraints

### Tipos de Relaciones

#### One-to-Many
```sql
-- Un rol tiene muchos usuarios
roles (1) ──< (N) usuarios

-- Un paciente tiene muchas consultas
pacientes (1) ──< (N) consultas

-- Un paciente tiene muchas recetas
pacientes (1) ──< (N) recetas

-- Una receta tiene muchos detalles
recetas (1) ──< (N) receta_detalle
```

#### Many-to-Many
```sql
-- Roles y Permisos (a través de rol_permisos)
roles (N) ──< rol_permisos >── (N) permisos
```

### Foreign Key Constraints

**Acciones en cascada**:
```sql
-- ON DELETE CASCADE: Si se elimina el padre, se eliminan los hijos
CREATE TABLE receta_detalle (
    receta_id INTEGER REFERENCES recetas(id) ON DELETE CASCADE
);

-- ON DELETE SET NULL: Si se elimina el padre, se pone NULL en hijo
CREATE TABLE consultas (
    medico_id INTEGER REFERENCES usuarios(id) ON DELETE SET NULL
);

-- ON DELETE RESTRICT (default): No permite eliminar si tiene hijos
CREATE TABLE pacientes (
    created_by INTEGER REFERENCES usuarios(id)
);
```

### Check Constraints
```sql
-- Validar valores específicos
ALTER TABLE pacientes 
ADD CONSTRAINT check_sexo 
CHECK (sexo IN ('M', 'F'));

-- Validar rangos
ALTER TABLE productos 
ADD CONSTRAINT check_stock 
CHECK (stock_actual >= 0);

-- Validar relaciones
ALTER TABLE facturas 
ADD CONSTRAINT check_total 
CHECK (total >= 0 AND total >= subtotal - descuento);
```

---

## 🔄 Migraciones con Alembic

### Configuración Inicial

#### 1. Instalar Alembic
```bash
pip install alembic
```

#### 2. Inicializar Alembic
```bash
cd backend
alembic init alembic
```

Esto crea:
```
backend/
├── alembic/
│   ├── versions/          # Archivos de migración
│   ├── env.py            # Config de entorno
│   ├── script.py.mako    # Template
│   └── README
└── alembic.ini           # Config principal
```

#### 3. Configurar alembic.ini
```ini
# alembic.ini

[alembic]
script_location = alembic
sqlalchemy.url = postgresql://clinica_user:clinica2025!@localhost:5432/clinica_db

# O usar variable de entorno
# sqlalchemy.url = driver://user:pass@localhost/dbname
```

#### 4. Configurar env.py
```python
# alembic/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Importar Base de SQLAlchemy
from app.db.database import Base
from app.models import usuario, paciente  # Importar todos los modelos

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
target_metadata = Base.metadata

# Resto del archivo...
```

---

### Crear Migraciones

#### Migración Automática (Recomendado)
```bash
# Alembic detecta cambios automáticamente
alembic revision --autogenerate -m "add pacientes table"

# Esto genera: alembic/versions/xxxx_add_pacientes_table.py
```

**Archivo generado**:
```python
# alembic/versions/xxxx_add_pacientes_table.py

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = 'abc123'
down_revision = 'def456'
branch_labels = None
depends_on = None

def upgrade():
    # Crear tabla
    op.create_table(
        'pacientes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('numero_expediente', sa.String(20), nullable=False),
        sa.Column('nombres', sa.String(100), nullable=False),
        # ... más columnas
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear índices
    op.create_index('idx_pacientes_expediente', 'pacientes', ['numero_expediente'])

def downgrade():
    # Eliminar índices
    op.drop_index('idx_pacientes_expediente')
    
    # Eliminar tabla
    op.drop_table('pacientes')
```

#### Migración Manual
```bash
# Crear archivo vacío
alembic revision -m "add custom index"
```

Editar manualmente:
```python
def upgrade():
    op.execute("""
        CREATE INDEX idx_pacientes_busqueda 
        ON pacientes 
        USING gin(to_tsvector('spanish', nombres || ' ' || apellidos))
    """)

def downgrade():
    op.execute("DROP INDEX idx_pacientes_busqueda")
```

---

### Aplicar Migraciones
```bash
# Ver migraciones pendientes
alembic current

# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una migración específica
alembic upgrade abc123

# Aplicar siguiente migración
alembic upgrade +1

# Revertir última migración
alembic downgrade -1

# Revertir todas
alembic downgrade base

# Ver historial
alembic history

# Ver SQL sin ejecutar
alembic upgrade head --sql
```

---

### Ejemplo Completo: Agregar Campo

**Escenario**: Agregar campo `telefono3` a tabla `pacientes`

#### 1. Modificar modelo SQLAlchemy
```python
# app/models/paciente.py

class Paciente(Base):
    # ... campos existentes ...
    telefono3 = Column(String(8))  # ← Nuevo campo
```

#### 2. Generar migración
```bash
alembic revision --autogenerate -m "add telefono3 to pacientes"
```

#### 3. Revisar archivo generado
```python
# alembic/versions/xxxx_add_telefono3_to_pacientes.py

def upgrade():
    op.add_column('pacientes', 
        sa.Column('telefono3', sa.String(8), nullable=True)
    )

def downgrade():
    op.drop_column('pacientes', 'telefono3')
```

#### 4. Aplicar migración
```bash
alembic upgrade head
```

#### 5. Verificar en PostgreSQL
```sql
\d pacientes
-- Debería mostrar la nueva columna telefono3
```

---

## 🔍 Queries Comunes

### Queries de Gestión
```sql
-- Ver todas las tablas
\dt

-- Describir una tabla
\d pacientes

-- Ver tamaño de tablas
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Ver índices de una tabla
\di pacientes

-- Ver foreign keys
SELECT
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM information_schema.table_constraints AS tc 
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name='pacientes';
```

---

### Queries de Datos
```sql
-- Contar pacientes por estado
SELECT activo, COUNT(*) 
FROM pacientes 
GROUP BY activo;

-- Pacientes registrados en el último mes
SELECT COUNT(*) 
FROM pacientes 
WHERE created_at >= CURRENT_DATE - INTERVAL '1 month';

-- Consultas por médico (último mes)
SELECT 
    u.nombres || ' ' || u.apellidos AS medico,
    COUNT(c.id) AS total_consultas
FROM consultas c
JOIN usuarios u ON c.medico_id = u.id
WHERE c.fecha_consulta >= CURRENT_DATE - INTERVAL '1 month'
GROUP BY u.id, u.nombres, u.apellidos
ORDER BY total_consultas DESC;

-- Top 10 medicamentos más recetados
SELECT 
    rd.medicamento_nombre,
    COUNT(*) AS veces_recetado
FROM receta_detalle rd
JOIN recetas r ON rd.receta_id = r.id
WHERE r.fecha_emision >= CURRENT_DATE - INTERVAL '6 months'
GROUP BY rd.medicamento_nombre
ORDER BY veces_recetado DESC
LIMIT 10;

-- Pacientes con citas próximas (próximos 7 días)
SELECT 
    p.numero_expediente,
    p.nombres || ' ' || p.apellidos AS paciente,
    c.fecha_hora,
    u.nombres || ' ' || u.apellidos AS medico
FROM citas c
JOIN pacientes p ON c.paciente_id = p.id
JOIN usuarios u ON c.medico_id = u.id
WHERE c.fecha_hora BETWEEN CURRENT_TIMESTAMP AND CURRENT_TIMESTAMP + INTERVAL '7 days'
    AND c.estado = 'programada'
ORDER BY c.fecha_hora;

-- Productos de farmacia con stock bajo
SELECT 
    nombre,
    stock_actual,
    stock_minimo,
    fecha_vencimiento
FROM productos
WHERE stock_actual <= stock_minimo
    AND activo = TRUE
ORDER BY stock_actual;
```

---

## 💾 Backup y Restore

### Backup Completo
```bash
# Backup de toda la base de datos
pg_dump -U clinica_user -d clinica_db -F c -f backup_$(date +%Y%m%d).dump

# Backup con formato SQL plano
pg_dump -U clinica_user -d clinica_db > backup_$(date +%Y%m%d).sql

# Backup solo de esquema (sin datos)
pg_dump -U clinica_user -d clinica_db --schema-only > schema.sql

# Backup solo de datos
pg_dump -U clinica_user -d clinica_db --data-only > data.sql

# Backup de una tabla específica
pg_dump -U clinica_user -d clinica_db -t pacientes > pacientes_backup.sql
```

---

### Restore
```bash
# Restore desde archivo .dump
pg_restore -U clinica_user -d clinica_db backup_20251119.dump

# Restore desde SQL plano
psql -U clinica_user -d clinica_db < backup_20251119.sql

# Restore creando nueva base de datos
createdb -U postgres clinica_db_restore
pg_restore -U clinica_user -d clinica_db_restore backup_20251119.dump
```

---

### Script de Backup Automático (Windows)

**Archivo**: `backend/scripts/backup-db.bat`
```batch
@echo off
REM Backup automático de base de datos

SET FECHA=%date:~-4,4%%date:~-7,2%%date:~-10,2%
SET HORA=%time:~0,2%%time:~3,2%
SET BACKUP_DIR=D:\clinica-backups\%FECHA%
SET PGPASSWORD=clinica2025!

echo [%FECHA% %HORA%] Iniciando backup...

REM Crear directorio
mkdir "%BACKUP_DIR%" 2>nul

REM Backup de base de datos
"C:\Program Files\PostgreSQL\18\bin\pg_dump.exe" ^
    -U clinica_user ^
    -h localhost ^
    -d clinica_db ^
    -F c ^
    -f "%BACKUP_DIR%\db_backup.dump"

echo [%FECHA% %HORA%] Backup completado: %BACKUP_DIR%\db_backup.dump

REM Limpiar backups antiguos (más de 30 días)
forfiles /p "D:\clinica-backups" /d -30 /c "cmd /c rd /s /q @path" 2>nul

echo [%FECHA% %HORA%] Limpieza completada
```

**Programar en Windows**:
1. Abrir "Programador de Tareas"
2. Crear tarea básica
3. Trigger: Diariamente a las 11:00 PM
4. Acción: Ejecutar `backup-db.bat`

---

## ⚡ Performance y Optimización

### Índices

#### Cuándo Crear Índices

✅ **Crear índice en**:
- Primary Keys (automático)
- Foreign Keys
- Columnas con UNIQUE
- Columnas usadas frecuentemente en WHERE
- Columnas usadas en JOIN
- Columnas usadas en ORDER BY

❌ **NO crear índice en**:
- Tablas muy pequeñas (< 1000 filas)
- Columnas con baja cardinalidad (ej: booleanos)
- Columnas que rara vez se consultan

#### Tipos de Índices
```sql
-- B-tree (default, para comparaciones =, <, >)
CREATE INDEX idx_pacientes_fecha_nac ON pacientes(fecha_nacimiento);

-- Hash (solo para =)
CREATE INDEX idx_usuarios_username ON usuarios USING hash(username);

-- GIN (para full-text search, JSON, arrays)
CREATE INDEX idx_pacientes_busqueda ON pacientes 
USING gin(to_tsvector('spanish', nombres || ' ' || apellidos));

-- Parcial (solo filas que cumplen condición)
CREATE INDEX idx_pacientes_activos ON pacientes(created_at) 
WHERE activo = TRUE;

-- Compuesto (múltiples columnas)
CREATE INDEX idx_consultas_paciente_fecha ON consultas(paciente_id, fecha_consulta);
```

---

### Análisis de Queries
```sql
-- Ver query plan
EXPLAIN SELECT * FROM pacientes WHERE apellidos = 'García';

-- Ver query plan con costos reales
EXPLAIN ANALYZE SELECT * FROM pacientes WHERE apellidos = 'García';

-- Identificar queries lentas (configurar primero)
-- En postgresql.conf:
-- shared_preload_libraries = 'pg_stat_statements'
-- pg_stat_statements.track = all

SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

### Mantenimiento
```sql
-- Vacuum (limpiar espacio muerto)
VACUUM pacientes;

-- Vacuum completo (más agresivo, bloquea tabla)
VACUUM FULL pacientes;

-- Analyze (actualizar estadísticas para query planner)
ANALYZE pacientes;

-- Vacuum + Analyze
VACUUM ANALYZE pacientes;

-- Reindex (reconstruir índices)
REINDEX TABLE pacientes;
```

**Automatizar con pg_cron** (futuro):
```sql
-- Instalar extensión
CREATE EXTENSION pg_cron;

-- Vacuum automático cada noche a las 2 AM
SELECT cron.schedule('vacuum-diario', '0 2 * * *', 'VACUUM ANALYZE');
```

---

## 🌱 Seeds y Datos de Prueba

### Script de Inicialización (Sprint 1)

**Archivo**: `backend/init_database.py` (ya existe)

Crea:
- 4 roles
- Permisos básicos
- Usuario admin

---

### Seeds para Testing (Futuro)

**Archivo**: `backend/seeds/pacientes_test.py`
```python
from app.db.database import SessionLocal
from app.models.paciente import Paciente
from datetime import date, timedelta
import random

def seed_pacientes_test():
    db = SessionLocal()
    
    nombres = ["Juan", "María", "Carlos", "Ana", "Luis", "Carmen", "Pedro", "Rosa"]
    apellidos = ["García", "López", "Martínez", "Pérez", "González", "Rodríguez"]
    
    for i in range(50):
        paciente = Paciente(
            numero_expediente=f"EXP-{i+1:06d}",
            dpi=f"1234567890{i:03d}",
            nombres=random.choice(nombres),
            apellidos=f"{random.choice(apellidos)} {random.choice(apellidos)}",
            fecha_nacimiento=date.today() - timedelta(days=random.randint(365*5, 365*80)),
            sexo=random.choice(['M', 'F']),
            telefono1=f"{random.randint(3000, 5999)}{random.randint(0000, 9999):04d}",
            tiene_igss=random.choice([True, False]),
            activo=True
        )
        db.add(paciente)
    
    db.commit()
    print("✅ 50 pacientes de prueba creados")

if __name__ == "__main__":
    seed_pacientes_test()
```

**Ejecutar**:
```bash
python seeds/pacientes_test.py
```

---

## 📊 Monitoring (Futuro)

### Extensiones Útiles
```sql
-- Ver extensiones disponibles
SELECT * FROM pg_available_extensions;

-- Instalar pg_stat_statements
CREATE EXTENSION pg_stat_statements;

-- Instalar uuid-ossp (para UUIDs)
CREATE EXTENSION "uuid-ossp";

-- Instalar pg_trgm (para búsqueda difusa)
CREATE EXTENSION pg_trgm;
```

---

## 🔐 Seguridad

### Permisos de Usuario
```sql
-- Crear usuario de solo lectura (para reportes)
CREATE USER clinica_readonly WITH PASSWORD 'readonly2025!';
GRANT CONNECT ON DATABASE clinica_db TO clinica_readonly;
GRANT USAGE ON SCHEMA public TO clinica_readonly;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO clinica_readonly;

-- Revocar permisos
REVOKE INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public FROM clinica_readonly;
```

---

## 📚 Recursos

- PostgreSQL Docs: https://www.postgresql.org/docs/
- Alembic Docs: https://alembic.sqlalchemy.org/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/
- pgAdmin: https://www.pgadmin.org/
- DBeaver: https://dbeaver.io/

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0 - Sprint 1  
**Base de Datos**: PostgreSQL 18.1  
**ORM**: SQLAlchemy 2.0.36  
**Migraciones**: Alembic 1.14.0
```

---

# 🎉 ¡DOCUMENTACIÓN COMPLETA!

Hemos creado **6 documentos esenciales** para el desarrollo continuo del proyecto:

1. ✅ **README.md** - Visión general y setup
2. ✅ **INSTALLATION.md** - Guía paso a paso de instalación
3. ✅ **API_DOCUMENTATION.md** - Endpoints del backend
4. ✅ **ARCHITECTURE.md** - Decisiones técnicas y arquitectura
5. ✅ **DEVELOPMENT.md** - Cómo desarrollar nuevas features
6. ✅ **DATABASE.md** - Esquema de BD y migraciones

---

## 📝 Resumen Final del Sprint 1
```
╔════════════════════════════════════════════════════╗
║           SPRINT 1 - COMPLETADO ✅                 ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  Backend:                                          ║
║    ✅ FastAPI + PostgreSQL                        ║
║    ✅ JWT Authentication                          ║
║    ✅ 4 roles + permisos                          ║
║    ✅ 8 endpoints funcionales                     ║
║    ✅ Swagger UI documentación                    ║
║                                                    ║
║  Frontend:                                         ║
║    ✅ Next.js 14 + TypeScript                     ║
║    ✅ Login con branding MEDGAR                   ║
║    ✅ Dashboard operativo                         ║
║    ✅ Middleware autenticación                    ║
║    ✅ Diseño responsive                           ║
║                                                    ║
║  Documentación:                                    ║
║    ✅ README.md                                    ║
║    ✅ INSTALLATION.md                             ║
║    ✅ API_DOCUMENTATION.md                        ║
║    ✅ ARCHITECTURE.md                             ║
║    ✅ DEVELOPMENT.md                              ║
║    ✅ DATABASE.md                                 ║
║                                                    ║
║  Sistema funcionando en:                           ║
║    🌐 http://localhost:3000                       ║
║    🌐 http://192.168.1.10:3000                    ║
║                                                    ║
║  Credenciales:                                     ║
║    👤 Usuario: admin                              ║
║    🔑 Password: admin123                          ║
║                                                    ║
╠════════════════════════════════════════════════════╣
║  ESTADO: LISTO PARA SPRINT 2 🚀                    ║
╚════════════════════════════════════════════════════╝