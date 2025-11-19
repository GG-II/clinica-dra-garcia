# 🏥 Sistema Clínico - Clínica Familiar MEDGAR

Sistema integral de gestión clínica desarrollado con Next.js, FastAPI y PostgreSQL para deployment local.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Sprint](https://img.shields.io/badge/sprint-1%2F12-green.svg)
![Status](https://img.shields.io/badge/status-MVP%20Operativo-success.svg)

## 📋 Tabla de Contenidos

- [Sobre el Proyecto](#sobre-el-proyecto)
- [Características Actuales](#características-actuales)
- [Stack Tecnológico](#stack-tecnológico)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Roadmap](#roadmap)
- [Contribución](#contribución)

---

## 🎯 Sobre el Proyecto

Sistema de gestión clínica integral diseñado para la **Clínica Familiar MEDGAR** en Guatemala. El sistema permite la gestión completa de:

- 👥 Pacientes y expedientes clínicos
- 📅 Agenda médica y citas
- 📋 Historia clínica electrónica
- 💊 Recetas y medicamentos
- 🏥 Hospitalización (8 camas)
- 🔬 Laboratorios y estudios
- 💉 Farmacia e inventario
- 💰 Caja y facturación FEL (Guatemala)

### Contexto de la Clínica

- **Especialidades**: Medicina Interna, Pediatría, Ginecología, Cirugía, Traumatología, Medicina General
- **Médicos**: 2 activos
- **Pacientes**: ~120 mensuales
- **Sucursales**: 1 actual + 1 planificada
- **Deployment**: Local en Lenovo IdeaPad (192.168.1.10)

---

## ✨ Características Actuales (Sprint 1)

### ✅ Backend (FastAPI)
- [x] API RESTful con FastAPI 0.115
- [x] Base de datos PostgreSQL 18
- [x] Autenticación JWT
- [x] Sistema de roles y permisos
- [x] 4 roles predefinidos
- [x] Usuario administrador inicial
- [x] Documentación Swagger UI
- [x] CORS configurado
- [x] Logging de auditoría

### ✅ Frontend (Next.js)
- [x] Interfaz moderna con tema morado/lila
- [x] Login page con branding MEDGAR
- [x] Dashboard principal
- [x] Middleware de autenticación
- [x] Manejo de sesiones con cookies
- [x] Diseño responsive (desktop/tablet/móvil)
- [x] Logout funcional

### ✅ Seguridad
- [x] Passwords encriptados con bcrypt
- [x] Tokens JWT con expiración
- [x] Middleware de autenticación
- [x] CORS restringido
- [x] Variables de entorno

---

## 🛠️ Stack Tecnológico

### Backend
```yaml
Lenguaje: Python 3.13.9
Framework: FastAPI 0.115.6
ORM: SQLAlchemy 2.0.36
Migraciones: Alembic 1.14.0
Base de Datos: PostgreSQL 18.1
Autenticación: JWT (python-jose)
Passwords: bcrypt 4.2.1
```

### Frontend
```yaml
Framework: Next.js 14
Lenguaje: TypeScript
Estilos: Tailwind CSS 3
HTTP Client: Axios
Cookies: js-cookie
```

### Infraestructura
```yaml
Servidor: Lenovo IdeaPad Slim 3 15AMN8
CPU: AMD Ryzen 5 7520U (4 cores @ 2.8GHz)
RAM: 16 GB
Storage: 500 GB SSD
OS: Windows 11 Pro
Red: WiFi local (192.168.1.10)
```

---

## 📋 Requisitos Previos

### Software Necesario
- **Node.js**: 20.x LTS o superior
- **Python**: 3.11 o superior
- **PostgreSQL**: 15 o superior
- **Git**: 2.x o superior

### Conocimientos Recomendados
- TypeScript/JavaScript básico
- Python básico
- SQL básico
- Conceptos de API REST

---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/clinica-dra-garcia.git
cd clinica-dra-garcia
```

### 2. Configurar Backend
```bash
cd clinica/backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Windows)
.\venv\Scripts\Activate

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Configurar Frontend
```bash
cd clinica/frontend

# Instalar dependencias
npm install
```

### 4. Configurar Base de Datos
```bash
# Conectar a PostgreSQL
psql -U postgres

# Crear base de datos
CREATE DATABASE clinica_db;
CREATE USER clinica_user WITH PASSWORD 'clinica2025!';
GRANT ALL PRIVILEGES ON DATABASE clinica_db TO clinica_user;
\c clinica_db
GRANT ALL ON SCHEMA public TO clinica_user;
\q
```

### 5. Inicializar Datos
```bash
cd clinica/backend
python init_database.py
```

Esto creará:
- ✅ 4 roles del sistema
- ✅ Permisos básicos
- ✅ Usuario admin (admin/admin123)

---

## ⚙️ Configuración

### Backend (.env)

Crear archivo `clinica/backend/.env`:
```env
# Database
DATABASE_URL=postgresql://clinica_user:clinica2025!@localhost:5432/clinica_db

# Security
SECRET_KEY=tu_super_secret_key_aqui_cambiar_en_produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://192.168.1.10:3000"]
```

### Frontend (.env.local)

Crear archivo `clinica/frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

---

## 🎮 Uso

### Iniciar Backend
```bash
cd clinica/backend
.\venv\Scripts\Activate  # Windows
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

El backend estará disponible en:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- Red local: http://192.168.1.10:8000

### Iniciar Frontend
```bash
cd clinica/frontend
npm run dev
```

El frontend estará disponible en:
- Local: http://localhost:3000
- Red local: http://192.168.1.10:3000

### Credenciales de Prueba
```
Usuario: admin
Contraseña: admin123
Rol: Administrador
```

---

## 📁 Estructura del Proyecto
```
clinica-dra-garcia/
├── clinica/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   └── v1/
│   │   │   │       ├── endpoints/
│   │   │   │       │   ├── auth.py
│   │   │   │       │   └── usuarios.py
│   │   │   │       └── __init__.py
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   └── security.py
│   │   │   ├── db/
│   │   │   │   ├── database.py
│   │   │   │   └── init_db.py
│   │   │   ├── models/
│   │   │   │   └── usuario.py
│   │   │   └── schemas/
│   │   │       ├── auth.py
│   │   │       └── usuario.py
│   │   ├── main.py
│   │   ├── init_database.py
│   │   ├── requirements.txt
│   │   └── .env
│   │
│   └── frontend/
│       ├── app/
│       │   ├── (auth)/
│       │   │   └── login/
│       │   │       └── page.tsx
│       │   ├── dashboard/
│       │   │   ├── layout.tsx
│       │   │   └── page.tsx
│       │   ├── layout.tsx
│       │   └── page.tsx
│       ├── components/
│       ├── lib/
│       │   ├── api.ts
│       │   └── auth.ts
│       ├── public/
│       │   ├── logo-medgar.png
│       │   └── icon-medgar.png
│       ├── types/
│       │   └── index.ts
│       ├── middleware.ts
│       ├── next.config.js
│       ├── tailwind.config.ts
│       └── .env.local
│
├── clinica-archivos/
│   ├── pacientes/
│   ├── inventario/
│   ├── fel/
│   └── backups/
│
├── docs/
│   └── (documentación adicional)
│
├── README.md
├── PLAN_SCRUM.md
└── Requisitos_Clínica.MD
```

---

## 🗺️ Roadmap

### ✅ Sprint 1: Infraestructura Base (COMPLETADO)
- [x] Setup ambiente local
- [x] Backend FastAPI + PostgreSQL
- [x] Frontend Next.js
- [x] Autenticación JWT
- [x] Login y Dashboard básico

### 🔄 Sprint 2: Gestión de Pacientes (En planificación)
- [ ] Registro de pacientes
- [ ] Búsqueda de pacientes
- [ ] Gestión de archivos multimedia
- [ ] CRUD completo

### 📅 Sprint 3: Historia Clínica Parte 1
- [ ] Antecedentes médicos
- [ ] Signos vitales
- [ ] Esquema de vacunación

### 📅 Sprint 4: Historia Clínica Parte 2 + Agenda
- [ ] Plantillas por especialidad
- [ ] Curvas OMS
- [ ] Sistema de citas

### 📅 Sprint 5-12: Módulos adicionales
- Recetas y recordatorios
- Caja y facturación
- Hospitalización
- Laboratorios
- Farmacia e inventario
- FEL Guatemala
- Reportes
- Telemedicina

Ver [PLAN_SCRUM.md](./PLAN_SCRUM.md) para detalles completos.

---

## 🤝 Contribución

### Flujo de Trabajo Git
```bash
# Crear rama para nueva feature
git checkout develop
git pull origin develop
git checkout -b feature/nombre-feature

# Hacer commits
git add .
git commit -m "feat: descripción del cambio"

# Push y crear PR
git push origin feature/nombre-feature
# Crear Pull Request en GitHub a develop
```

### Convención de Commits
```
feat: Nueva funcionalidad
fix: Corrección de bug
docs: Cambios en documentación
style: Cambios de formato
refactor: Refactorización de código
test: Agregar tests
chore: Tareas de mantenimiento
```

---

## 📞 Contacto

**Proyecto**: Sistema Clínico MEDGAR  
**Cliente**: Clínica Familiar MEDGAR  
**Desarrollo**: [Tu nombre]  
**Metodología**: SCRUM (Sprints de 2 semanas)

---

## 📄 Licencia

Proyecto privado - Uso exclusivo Clínica Familiar MEDGAR

---

## 🙏 Agradecimientos

- Clínica Familiar MEDGAR por confiar en este proyecto
- Comunidad de FastAPI y Next.js por la documentación
- PostgreSQL por la robustez de la base de datos

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0.0 - Sprint 1 MVP  
**Estado**: ✅ Operativo en ambiente local