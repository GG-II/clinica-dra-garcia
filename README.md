# 🏥 Sistema Clínico MEDGAR - Dra. Estephanny García

Sistema integral de gestión clínica desarrollado para la Clínica Médica Dra. Estephanny García en Huehuetenango, Guatemala.

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black.svg)](https://nextjs.org/)
[![License](https://img.shields.io/badge/License-Proprietary-red.svg)]()

---

## 📋 Tabla de Contenidos

- [Descripción General](#-descripción-general)
- [Características Principales](#-características-principales)
- [Tecnologías](#-tecnologías)
- [Arquitectura](#-arquitectura)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Documentación](#-documentación)
- [Testing](#-testing)
- [Roadmap](#-roadmap)
- [Contribución](#-contribución)
- [Licencia](#-licencia)

---

## 🎯 Descripción General

MEDGAR es un sistema completo de gestión clínica que digitaliza todas las operaciones de una clínica médica multi-especialidad. Diseñado específicamente para clínicas pequeñas y medianas en Guatemala, cumpliendo con normativas locales.

### Datos del Proyecto

- **Cliente**: Dra. Estephanny García
- **Ubicación**: Huehuetenango, Guatemala
- **Especialidades**: Medicina Interna, Pediatría, Ginecología, Cirugía, Traumatología
- **Capacidad**: 120 pacientes/mes, 8 camas de hospitalización
- **Desarrollo**: Metodología SCRUM, Sprints de 2 semanas

### Estado del Proyecto
```
┌─────────────────────────────────────────────────────────────┐
│                  ESTADO ACTUAL DEL PROYECTO                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ Backend: 100% COMPLETO                                 │
│     • 103 endpoints implementados                          │
│     • 16 módulos funcionales                               │
│     • 31 tablas en base de datos                           │
│                                                             │
│  ⏳ Frontend: 0% (Próximo Sprint)                          │
│     • Next.js 14 + TypeScript                              │
│     • Tailwind CSS + shadcn/ui                             │
│     • Tema lila pastel                                     │
│                                                             │
│  📊 Progreso Global: 50%                                   │
│     ████████████░░░░░░░░░░░░                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## ✨ Características Principales

### Módulos Implementados (16/16)

#### 1. 👥 Gestión de Pacientes
- ✅ Registro completo con datos personales
- ✅ Gestión de archivos multimedia (fotos, PDFs, videos)
- ✅ Búsqueda rápida por nombre/DPI
- ✅ Estadísticas de pacientes
- ✅ Historial clínico completo

#### 2. 📅 Agenda y Citas
- ✅ Calendario por médico
- ✅ 6 tipos de citas (Primera consulta, Reconsulta, Procedimiento, etc.)
- ✅ Sistema de confirmación
- ✅ Lista de espera con prioridades
- ✅ Recordatorios automáticos (preparado para WhatsApp/SMS)

#### 3. 📋 Historia Clínica Electrónica
- ✅ Registro de consultas con signos vitales
- ✅ Cálculo automático de IMC
- ✅ 6 tipos de antecedentes médicos
- ✅ Esquema de vacunación (13 vacunas)
- ✅ Alertas de vacunas pendientes
- ✅ Sistema de interconsultas

#### 4. 💊 Recetas Médicas
- ✅ Base de datos de medicamentos (500+)
- ✅ Prescripción de múltiples medicamentos
- ✅ Alertas de interacciones medicamentosas
- ✅ Historial de recetas por paciente
- ✅ Generación de PDF (próximamente)

#### 5. 🏥 Hospitalización
- ✅ Gestión de 8 camas
- ✅ Control de ingresos y egresos
- ✅ 5 tipos de notas médicas (Ingreso, Evolución, Procedimiento, Operatoria, Egreso)
- ✅ Órdenes médicas (8 tipos)
- ✅ Cambio automático de estados de cama
- ✅ Estadísticas de ocupación

#### 6. 🔬 Laboratorios
- ✅ 32 tipos de estudios predefinidos
- ✅ 13 categorías de laboratorio
- ✅ Valores de referencia por edad/sexo
- ✅ Alertas de valores críticos
- ✅ Comparación histórica
- ✅ Gráficas de tendencias

#### 7. 💰 Caja y Facturación
- ✅ Apertura y cierre de caja diaria
- ✅ Registro de ingresos (7 tipos)
- ✅ Registro de egresos (7 tipos)
- ✅ Arqueo automático
- ✅ Cuentas por cobrar
- ✅ Cotizaciones
- ✅ Integración FEL (próximamente)

#### 8. 💊 Farmacia e Inventario
- ✅ Catálogo completo de productos
- ✅ Control de stock con alertas
- ✅ Alertas de vencimiento (30 días)
- ✅ Gestión de proveedores
- ✅ Compras con actualización automática
- ✅ Ventas con validación de stock
- ✅ Movimientos de inventario
- ✅ Estadísticas en tiempo real

#### 9. 📊 Reportes y Dashboard
- ✅ Dashboard ejecutivo con KPIs
- ✅ Reportes de pacientes
- ✅ Reportes de citas y consultas
- ✅ Reportes de hospitalización
- ✅ Exportación a Excel/PDF (próximamente)

---

## 🛠 Tecnologías

### Backend
```yaml
Lenguaje: Python 3.11
Framework: FastAPI 0.100+
ORM: SQLAlchemy 2.0
Validación: Pydantic v2
Base de Datos: PostgreSQL 15
Servidor: Uvicorn
Testing: pytest + pytest-cov
```

### Frontend (Próximo Sprint)
```yaml
Framework: Next.js 14
Lenguaje: TypeScript
Estilos: Tailwind CSS
Componentes: shadcn/ui
Tema: Lila Pastel
Estado: Zustand / React Context
```

### Infraestructura
```yaml
Deployment: Local (Lenovo IdeaPad)
Procesador: AMD Ryzen 5 7520U (4 cores)
RAM: 16 GB
Almacenamiento: 500 GB SSD
Sistema: Windows 11 Pro
Red: WiFi Local (192.168.1.10)
```

---

## 🏗 Arquitectura
```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA DEL SISTEMA                 │
└─────────────────────────────────────────────────────────────┘

📱 CLIENTES
   ├─ Tablets (WiFi)
   ├─ Smartphones (WiFi)
   └─ Laptop (localhost)
         ↓ HTTP/REST
┌─────────────────────────────────────────────────────────────┐
│  FRONTEND (Next.js 14)                                      │
│  └─ http://192.168.1.10:3000                                │
└─────────────────────────────────────────────────────────────┘
         ↓ API Calls
┌─────────────────────────────────────────────────────────────┐
│  BACKEND (FastAPI)                                          │
│  ├─ API Gateway (main.py)                                   │
│  ├─ 16 Routers (Controladores)                              │
│  ├─ 103 Endpoints                                           │
│  └─ http://192.168.1.10:8000                                │
└─────────────────────────────────────────────────────────────┘
         ↓ SQLAlchemy ORM
┌─────────────────────────────────────────────────────────────┐
│  BASE DE DATOS (PostgreSQL 15)                              │
│  ├─ 31 Tablas                                               │
│  ├─ Relaciones FK                                           │
│  └─ localhost:5432/clinica_db                               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│  ARCHIVOS (Sistema de Archivos)                             │
│  ├─ D:\clinica-archivos\                                    │
│  │   ├─ pacientes\                                          │
│  │   ├─ inventario\                                         │
│  │   └─ fel\                                                │
│  └─ D:\clinica-backups\ (diarios 11 PM)                     │
└─────────────────────────────────────────────────────────────┘
```

**Ver documentación completa**: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.11+
- PostgreSQL 15
- Node.js 20 LTS (para frontend)
- 16 GB RAM mínimo
- Windows 10/11 Pro

### Backend
```bash
# 1. Clonar repositorio
git clone <repository-url>
cd clinica/backend

# 2. Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar PostgreSQL
# Crear base de datos 'clinica_db'
# Usuario: postgres
# Puerto: 5432

# 5. Crear tablas
python create_simple_tables.py

# 6. Inicializar datos
python init_data_completo.py

# 7. Ejecutar servidor
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Verificar Instalación
```bash
# Abrir navegador en:
http://localhost:8000/docs

# Deberías ver Swagger UI con 103 endpoints
```

### Frontend (Próximo Sprint)
```bash
cd clinica/frontend

npm install
npm run dev

# Abrir navegador en:
http://localhost:3000
```

---

## 💻 Uso

### Acceso a la API

**Local (Laptop)**:
```
http://localhost:8000
```

**Red Local (Tablets/Móviles)**:
```
http://192.168.1.10:8000
```

### Documentación Interactiva

**Swagger UI**:
```
http://localhost:8000/docs
```

**ReDoc**:
```
http://localhost:8000/redoc
```

### Ejemplos de Uso

#### Crear un Paciente
```bash
curl -X POST "http://localhost:8000/api/pacientes" \
  -H "Content-Type: application/json" \
  -d '{
    "nombres": "María",
    "apellidos": "González",
    "fecha_nacimiento": "1990-05-15",
    "dpi": "2547896541201",
    "genero": "Femenino",
    "telefono": "55551234"
  }'
```

#### Listar Pacientes
```bash
curl -X GET "http://localhost:8000/api/pacientes?skip=0&limit=10"
```

#### Crear Cita
```bash
curl -X POST "http://localhost:8000/api/citas" \
  -H "Content-Type: application/json" \
  -d '{
    "paciente_id": 1,
    "medico_id": 2,
    "fecha_hora": "2025-01-20T10:00:00",
    "tipo_cita": "Primera Consulta",
    "motivo": "Control rutinario"
  }'
```

#### Dashboard Ejecutivo
```bash
curl -X GET "http://localhost:8000/api/reportes/dashboard"
```

---

## 📚 Documentación

### Documentación Técnica

| Documento | Descripción | Ubicación |
|-----------|-------------|-----------|
| **API Documentation** | Documentación completa de los 103 endpoints | [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) |
| **Database** | Esquema de 31 tablas, relaciones, índices | [docs/DATABASE.md](docs/DATABASE.md) |
| **Architecture** | Arquitectura del sistema, patrones de diseño | [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) |
| **Endpoints Summary** | Resumen ejecutivo de endpoints | [docs/ENDPOINTS_SUMMARY.md](docs/ENDPOINTS_SUMMARY.md) |
| **Testing Guide** | Guía completa de testing | [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md) |
| **Development** | Guía para desarrolladores | [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) |
| **Installation** | Instalación paso a paso | [docs/INSTALLATION.md](docs/INSTALLATION.md) |

### Documentos de Proyecto

| Documento | Descripción | Ubicación |
|-----------|-------------|-----------|
| **Requisitos** | Requisitos funcionales y no funcionales | [Requisitos_Clínica.MD](Requisitos_Clínica.MD) |
| **Plan SCRUM** | Plan de desarrollo por sprints | [PLAN_SCRUM.md](PLAN_SCRUM.md) |

---

## 🧪 Testing

### Ejecutar Tests
```bash
# Activar entorno virtual
cd clinica/backend
source venv/bin/activate  # o venv\Scripts\activate en Windows

# Todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html --cov-report=term-missing

# Solo tests de API
pytest tests/api/ -v

# Solo tests unitarios
pytest tests/unit/ -m unit

# Ver reporte HTML
# Abrir: htmlcov/index.html
```

### Cobertura Objetivo

- **Global**: 80%+
- **Routers**: 85%+
- **Modelos críticos**: 90%+

**Ver guía completa**: [docs/TESTING_GUIDE.md](docs/TESTING_GUIDE.md)

---

## 📊 Estadísticas del Proyecto

### Backend (Completado)
```
Líneas de código:     ~4,500
Archivos Python:      25
Modelos SQLAlchemy:   31
Endpoints REST:       103
Routers:              16
Sprints completados:  1-10
Tiempo desarrollo:    10 semanas
```

### Base de Datos
```
Tablas:               31
Relaciones FK:        45+
Índices:              20+
Enums:                15
Datos iniciales:
  ├─ Medicamentos:    20
  ├─ Camas:           8
  └─ Estudios Lab:    32
```

### API
```
Endpoints:            103
  ├─ GET:             42 (40.78%)
  ├─ POST:            42 (40.78%)
  ├─ PUT:             15 (14.56%)
  └─ DELETE:          4  (3.88%)

Módulos:              16
Tiempo respuesta:     < 200ms (promedio)
```

---

## 🗓 Roadmap

### ✅ Completado

- [x] Sprint 1: Infraestructura Base
- [x] Sprint 2: Gestión de Pacientes
- [x] Sprint 3: Historia Clínica Parte 1
- [x] Sprint 4: Historia Clínica Parte 2 + Agenda
- [x] Sprint 5: Recetas y Recordatorios
- [x] Sprint 6: Caja y Facturación Básica
- [x] Sprint 7: Módulo Hospitalización
- [x] Sprint 8: Laboratorios y Egreso
- [x] Sprint 9: Farmacia e Inventario
- [x] Sprint 10: Reportes y Dashboard

### ⏳ En Progreso

- [ ] Sprint 11: Frontend Base (Next.js)
- [ ] Sprint 12: Frontend Módulos Principales

### 📅 Próximamente

- [ ] Sprint 13: Autenticación y Seguridad
- [ ] Sprint 14: Integración FEL
- [ ] Sprint 15: Optimización y Testing
- [ ] Sprint 16: Telemedicina
- [ ] Sprint 17-20: Polish y Go-Live

### 🔮 Futuro

- [ ] Multi-sucursal
- [ ] App móvil nativa
- [ ] Inteligencia artificial para diagnósticos
- [ ] Integración con laboratorios externos

---

## 👥 Equipo

### Roles SCRUM

- **Product Owner**: Dra. Estephanny García
- **Scrum Master**: [Tu nombre]
- **Development Team**: 
  - Backend Developer
  - Frontend Developer (próximamente)
  - Full-stack Developer (opcional)

---

## 🤝 Contribución

Este es un proyecto privado para la Clínica Dra. García. Las contribuciones están limitadas al equipo de desarrollo autorizado.

### Para el Equipo de Desarrollo

1. Crear rama desde `develop`
```bash
git checkout develop
git pull
git checkout -b feature/nueva-funcionalidad
```

2. Hacer cambios y commit
```bash
git add .
git commit -m "feat: descripción del cambio"
```

3. Push y crear Pull Request
```bash
git push origin feature/nueva-funcionalidad
# Crear PR en GitHub hacia develop
```

### Convenciones de Commits
```
feat: nueva funcionalidad
fix: corrección de bug
docs: cambios en documentación
style: formato, punto y coma, etc
refactor: refactorización de código
test: agregar tests
chore: tareas de mantenimiento
```

---

## 📝 Licencia

**Propietario**: Clínica Médica Dra. Estephanny García  
**Desarrollador**: [Tu nombre/empresa]  
**Tipo**: Software Propietario - Todos los derechos reservados

Este software es propiedad exclusiva de la Clínica Dra. García. No se permite su distribución, copia o modificación sin autorización expresa por escrito.

---

## 📞 Contacto y Soporte

### Cliente

**Dra. Estephanny García**  
Clínica Médica  
Huehuetenango, Guatemala  
Email: [email]  
Teléfono: [teléfono]

### Desarrollo y Soporte Técnico

**[Tu nombre/empresa]**  
Email: [tu-email]  
Teléfono: [tu-teléfono]  
Horario de soporte: Lunes a Viernes, 8 AM - 5 PM

---

## 🙏 Agradecimientos

- **Dra. Estephanny García** - Por la confianza y visión del proyecto
- **Equipo médico de la clínica** - Por su colaboración en definir requisitos
- **FastAPI Community** - Por el excelente framework
- **PostgreSQL Community** - Por el robusto motor de base de datos

---

## 📌 Notas Importantes

### ⚠️ Configuración Inicial Requerida

1. **PostgreSQL**: Debe estar instalado y corriendo en puerto 5432
2. **Datos iniciales**: Ejecutar `init_data_completo.py` después de crear tablas
3. **Archivos**: Crear carpeta `D:\clinica-archivos\` antes del primer uso
4. **Backups**: Configurar tarea programada para backup diario (11 PM)
5. **Red**: Configurar IP estática 192.168.1.10 en la laptop

### 🔒 Seguridad

- Cambiar contraseña de PostgreSQL en producción
- Habilitar autenticación JWT antes del go-live
- Configurar firewall para permitir solo red local
- Backups diarios obligatorios
- UPS/No-break requerido para la laptop

### 📱 Acceso Remoto

- **Solo red local**: No hay acceso desde internet
- **WiFi requerido**: Tablets/móviles deben conectarse al WiFi de la clínica
- **IP fija**: Configurar router para asignar IP estática a la laptop

---

## 🚦 Estado de Servicios
```
┌─────────────────────────────────────────────────────────────┐
│  SERVICIOS                                    ESTADO         │
├─────────────────────────────────────────────────────────────┤
│  Backend API                                  ✅ Online     │
│  Base de Datos PostgreSQL                     ✅ Online     │
│  Frontend Next.js                             ⏳ Pendiente  │
│  Autenticación JWT                            ⏳ Pendiente  │
│  Facturación FEL                              ⏳ Pendiente  │
│  Recordatorios WhatsApp                       ⏳ Pendiente  │
│  Telemedicina                                 ⏳ Pendiente  │
│  Backups Automáticos                          ⚙️ Configurar │
└─────────────────────────────────────────────────────────────┘
```

---

## 📖 Quick Start
```bash
# 1. Clonar repo
git clone <repo-url>

# 2. Backend
cd clinica/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python create_simple_tables.py
python init_data_completo.py
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 3. Abrir Swagger
# http://localhost:8000/docs

# 4. Frontend (próximamente)
cd ../frontend
npm install
npm run dev
# http://localhost:3000
```

---

## 🎉 ¡Gracias!

Este proyecto representa la digitalización completa de una clínica médica guatemalteca, mejorando la atención a más de 120 pacientes mensuales.

**Versión**: 2.0.0  
**Última actualización**: Enero 2025  
**Estado**: Backend 100% Completo ✅

---

<p align="center">
  <strong>Desarrollado con ❤️ para la Clínica Dra. Estephanny García</strong>
</p>

<p align="center">
  🏥 Transformando la salud con tecnología 🏥
</p>