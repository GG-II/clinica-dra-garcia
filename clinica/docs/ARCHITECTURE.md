# 🏗️ Arquitectura del Sistema - Clínica Familiar MEDGAR

Documento de decisiones técnicas y arquitectura del sistema.

## 📋 Índice

1. [Visión General](#visión-general)
2. [Decisiones Arquitectónicas](#decisiones-arquitectónicas)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Arquitectura del Backend](#arquitectura-del-backend)
5. [Arquitectura del Frontend](#arquitectura-del-frontend)
6. [Base de Datos](#base-de-datos)
7. [Seguridad](#seguridad)
8. [Deployment Local](#deployment-local)
9. [Escalabilidad](#escalabilidad)

---

## 🎯 Visión General

### Tipo de Arquitectura
**Arquitectura de 3 capas con API REST**
```
┌─────────────────────────────────────────┐
│         CAPA DE PRESENTACIÓN            │
│     (Next.js 14 + TypeScript)           │
│   - UI/UX                               │
│   - Manejo de estado local              │
│   - Validaciones de frontend            │
└─────────────────┬───────────────────────┘
                  │ HTTP/REST
                  │ JSON
┌─────────────────▼───────────────────────┐
│         CAPA DE APLICACIÓN              │
│       (FastAPI + Python)                │
│   - Lógica de negocio                   │
│   - Autenticación/Autorización          │
│   - Validaciones                        │
│   - Transformación de datos             │
└─────────────────┬───────────────────────┘
                  │ SQLAlchemy ORM
                  │ SQL
┌─────────────────▼───────────────────────┐
│         CAPA DE DATOS                   │
│         (PostgreSQL 18)                 │
│   - Persistencia                        │
│   - Integridad referencial              │
│   - Transacciones                       │
└─────────────────────────────────────────┘
```

### Principios de Diseño

1. **Separación de Responsabilidades**: Frontend, Backend y Base de Datos claramente separados
2. **API First**: El backend expone API REST documentada
3. **Stateless Backend**: El servidor no mantiene estado de sesión
4. **Client-Side State**: El frontend maneja su propio estado
5. **Security by Design**: Autenticación y autorización desde el inicio

---

## 🤔 Decisiones Arquitectónicas

### ADR-001: ¿Por qué sistema desde cero vs. software existente?

**Contexto**: 
Existen sistemas médicos como OpenMRS, FreeMedForms, OpenEMR.

**Decisión**: Construir desde cero

**Razones**:
1. ✅ **Control total**: Funcionalidades exactas requeridas
2. ✅ **Adaptación a Guatemala**: FEL, IGSS, regulaciones locales
3. ✅ **Curva de aprendizaje**: Más rápido aprender nuestro código que uno existente
4. ✅ **Mantenibilidad**: Conocemos cada línea de código
5. ✅ **Sin deuda técnica heredada**: Código limpio desde día 1

**Consecuencias**:
- ➕ Flexibilidad total
- ➕ Performance optimizado para nuestro caso de uso
- ➖ Mayor tiempo de desarrollo inicial
- ➖ Responsabilidad total del mantenimiento

---

### ADR-002: ¿Por qué FastAPI vs. Django/Flask?

**Opciones Evaluadas**:
- Django + DRF
- Flask + extensiones
- FastAPI

**Decisión**: FastAPI

**Razones**:
1. ✅ **Performance**: Uno de los frameworks Python más rápidos
2. ✅ **Type hints nativos**: Validación automática con Pydantic
3. ✅ **Documentación automática**: Swagger UI out-of-the-box
4. ✅ **Async nativo**: Preparado para operaciones asíncronas
5. ✅ **Menos boilerplate**: Código más limpio y conciso
6. ✅ **Moderno**: Usa características modernas de Python

**Comparativa**:
```python
# Django (más verboso)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
# FastAPI (más conciso)
@router.get("/usuarios/")
async def get_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()
```

---

### ADR-003: ¿Por qué Next.js vs. React SPA vs. Vue?

**Opciones Evaluadas**:
- React SPA (Create React App / Vite)
- Next.js
- Vue.js / Nuxt.js

**Decisión**: Next.js 14 (App Router)

**Razones**:
1. ✅ **SSR + CSR**: Flexibilidad de renderizado
2. ✅ **File-based routing**: Organización intuitiva
3. ✅ **Image optimization**: Optimización automática de imágenes
4. ✅ **TypeScript first-class**: Soporte nativo excelente
5. ✅ **Performance**: Carga rápida y SEO mejorado
6. ✅ **Middleware**: Fácil implementar protección de rutas
7. ✅ **API Routes**: Backend endpoints si se necesitan (no usados actualmente)

**Por qué NO React SPA**:
- ❌ Más configuración manual
- ❌ No SSR out-of-the-box
- ❌ Routing manual (React Router)

**Por qué NO Vue**:
- ❌ Menor ecosistema de librerías médicas
- ❌ Menos desarrolladores disponibles en Guatemala

---

### ADR-004: ¿Por qué PostgreSQL vs. MySQL vs. MongoDB?

**Opciones Evaluadas**:
- MySQL/MariaDB
- PostgreSQL
- MongoDB

**Decisión**: PostgreSQL 18

**Razones**:
1. ✅ **ACID completo**: Crítico para datos médicos
2. ✅ **JSON nativo**: Flexibilidad cuando se necesita
3. ✅ **Tipos de datos ricos**: Arrays, JSONB, UUID, etc.
4. ✅ **Constraints complejos**: Integridad referencial robusta
5. ✅ **Full-text search**: Búsqueda de texto integrada
6. ✅ **Open source real**: Sin sorpresas de licenciamiento
7. ✅ **Performance**: Excelente para lecturas y escrituras

**Por qué NO MySQL**:
- ❌ Menos tipos de datos nativos
- ❌ JSON menos maduro
- ❌ Historial de licenciamiento complicado (Oracle)

**Por qué NO MongoDB**:
- ❌ NoSQL no es ideal para datos relacionales médicos
- ❌ Menos maduro para transacciones complejas
- ❌ Mayor riesgo de inconsistencia de datos

---

### ADR-005: ¿Por qué deployment local vs. cloud?

**Contexto**: 
Clínica pequeña, 2 médicos, 120 pacientes/mes.

**Decisión**: Deployment local en Lenovo IdeaPad

**Razones**:
1. ✅ **Costo**: $0 mensual vs. $50-200/mes cloud
2. ✅ **Control de datos**: Datos sensibles permanecen en la clínica
3. ✅ **Sin dependencia de internet**: Funciona incluso si cae el internet
4. ✅ **Latencia**: Red local ultra rápida (< 5ms)
5. ✅ **Regulaciones**: Más fácil cumplir normativas de datos médicos
6. ✅ **Hardware existente**: Laptop ya adquirida

**Consideraciones Cloud evaluadas**:
- AWS/Azure/GCP: ❌ Costo alto para el volumen
- Heroku: ❌ $25/mes + DB, innecesario para uso local
- DigitalOcean: ❌ $12/mes, pero sin necesidad de acceso remoto

**Futuro**: Si segunda sucursal requiere acceso remoto, considerar:
- VPN entre sucursales
- Replicación de base de datos
- O migración a cloud

---

## 💻 Stack Tecnológico

### Backend Stack
```yaml
Runtime: Python 3.13.9
Framework: FastAPI 0.115.6
  ├─ Ventajas: Velocidad, type hints, documentación auto
  └─ Casos de uso: APIs REST modernas

ORM: SQLAlchemy 2.0.36
  ├─ Ventajas: Maduro, potente, flexible
  └─ Casos de uso: Mapeo objeto-relacional

Migraciones: Alembic 1.14.0
  ├─ Ventajas: Versionado de BD, reversible
  └─ Casos de uso: Cambios de esquema controlados

Base de Datos: PostgreSQL 18.1
  ├─ Ventajas: ACID, tipos ricos, performance
  └─ Casos de uso: Datos relacionales críticos

Autenticación: JWT (python-jose 3.3.0)
  ├─ Ventajas: Stateless, seguro, estándar
  └─ Casos de uso: Autenticación API REST

Passwords: bcrypt 4.2.1
  ├─ Ventajas: Resistente a ataques, lento (bueno)
  └─ Casos de uso: Hash de contraseñas

Servidor: Uvicorn 0.34.0
  ├─ Ventajas: ASGI, rápido, estable
  └─ Casos de uso: Servidor de aplicaciones Python
```

### Frontend Stack
```yaml
Framework: Next.js 14
  ├─ Ventajas: SSR, routing, optimizaciones
  └─ Casos de uso: Aplicaciones web modernas

Lenguaje: TypeScript 5
  ├─ Ventajas: Type safety, autocompletado
  └─ Casos de uso: JavaScript con tipos

Estilos: Tailwind CSS 3
  ├─ Ventajas: Utility-first, rápido, consistente
  └─ Casos de uso: Estilizado moderno

HTTP Client: Axios 1.x
  ├─ Ventajas: Interceptors, transformaciones
  └─ Casos de uso: Llamadas API

State Management: React Hooks + Cookies
  ├─ Ventajas: Simple, nativo, sin librería extra
  └─ Casos de uso: Estado local y sesión

Cookies: js-cookie 3.x
  ├─ Ventajas: Simple, cross-browser
  └─ Casos de uso: Almacenar token JWT
```

---

## 🏗️ Arquitectura del Backend

### Estructura de Carpetas
```
backend/
├── app/
│   ├── api/
│   │   └── v1/                    # Versionado de API
│   │       ├── endpoints/         # Endpoints por módulo
│   │       │   ├── auth.py       # Autenticación
│   │       │   ├── usuarios.py   # CRUD usuarios
│   │       │   └── pacientes.py  # CRUD pacientes (Sprint 2)
│   │       └── __init__.py       # Router principal v1
│   │
│   ├── core/                      # Configuración central
│   │   ├── config.py             # Settings con Pydantic
│   │   └── security.py           # JWT, bcrypt
│   │
│   ├── db/                        # Base de datos
│   │   ├── database.py           # Conexión SQLAlchemy
│   │   └── init_db.py            # Seed data inicial
│   │
│   ├── models/                    # Modelos SQLAlchemy
│   │   ├── usuario.py            # User, Role, Permission
│   │   └── paciente.py           # Patient (Sprint 2)
│   │
│   ├── schemas/                   # Schemas Pydantic
│   │   ├── auth.py               # Login, Token
│   │   └── usuario.py            # User DTO
│   │
│   └── services/                  # Lógica de negocio
│       └── (futuro)
│
├── main.py                        # Punto de entrada FastAPI
├── init_database.py              # Script inicialización
├── requirements.txt              # Dependencias Python
└── .env                          # Variables de entorno
```

### Flujo de Request
```
1. Cliente hace request → http://localhost:8000/api/v1/usuarios/
2. CORS Middleware → Valida origen
3. FastAPI Router → Encuentra endpoint
4. Dependencias → get_db(), auth
5. Endpoint Handler → Lógica de negocio
6. SQLAlchemy → Query a PostgreSQL
7. Pydantic Schema → Serialización
8. Response → JSON al cliente
```

### Patrones de Diseño Usados

1. **Repository Pattern**: 
   - SQLAlchemy models abstraen acceso a datos
   - Futuro: Crear clases Repository explícitas

2. **Dependency Injection**:
```python
   def get_usuarios(db: Session = Depends(get_db)):
       # db inyectado automáticamente
```

3. **DTO Pattern**:
   - Pydantic schemas como Data Transfer Objects
   - Separación entre modelos de BD y API

4. **Middleware Pattern**:
   - CORS middleware
   - (Futuro) Rate limiting, logging

---

## 🎨 Arquitectura del Frontend

### Estructura de Carpetas
```
frontend/
├── app/                           # Next.js App Router
│   ├── (auth)/                   # Grupo de rutas auth
│   │   └── login/
│   │       └── page.tsx          # Página login
│   │
│   ├── dashboard/                # Rutas protegidas
│   │   ├── layout.tsx            # Layout con header/footer
│   │   └── page.tsx              # Dashboard principal
│   │
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Redirect a /login
│   └── globals.css               # Estilos globales
│
├── components/                    # Componentes reutilizables
│   ├── layout/                   # Layout components
│   └── ui/                       # UI components
│
├── lib/                           # Utilidades
│   ├── api.ts                    # Axios configurado
│   └── auth.ts                   # Servicio autenticación
│
├── public/                        # Assets estáticos
│   ├── logo-medgar.png           # Logo completo
│   └── icon-medgar.png           # Ícono solo
│
├── types/                         # TypeScript types
│   └── index.ts                  # Interfaces globales
│
├── middleware.ts                  # Next.js middleware (auth)
├── next.config.js                # Config Next.js
├── tailwind.config.ts            # Config Tailwind
└── .env.local                    # Variables de entorno
```

### Flujo de Navegación
```
1. Usuario visita "/" 
   → middleware.ts → Verifica token
   → Si no hay token: Redirect /login
   → Si hay token: Permite acceso

2. Usuario en /login
   → Ingresa credenciales
   → authService.login()
   → Guarda token en cookie
   → Redirect /dashboard

3. Usuario en /dashboard
   → layout.tsx renderiza header/footer
   → page.tsx renderiza contenido
   → Todos los links usan Next.js <Link>

4. Usuario click "Cerrar Sesión"
   → authService.logout()
   → Elimina cookie
   → Redirect /login
```

### Manejo de Estado

**Estado Global**: No se usa Redux/Zustand (innecesario para Sprint 1)

**Estado Local**: React Hooks
```typescript
const [loading, setLoading] = useState(false);
const [user, setUser] = useState<Usuario | null>(null);
```

**Estado de Sesión**: Cookies + Local checks
```typescript
// Guardar
Cookies.set('token', token, { expires: 7 });
Cookies.set('user', JSON.stringify(user), { expires: 7 });

// Leer
const token = Cookies.get('token');
const user = JSON.parse(Cookies.get('user'));
```

**Futuro**: Si la app crece, considerar:
- Zustand (ligero, simple)
- React Query (cache de API calls)
- Redux Toolkit (si se vuelve muy complejo)

---

## 🗄️ Base de Datos

### Esquema ER - Sprint 1
```
┌─────────────────┐
│     roles       │
├─────────────────┤
│ id (PK)        │
│ nombre         │◄─────────┐
│ descripcion    │          │
│ created_at     │          │
└─────────────────┘          │
                             │
                             │ FK
                             │
┌─────────────────┐          │
│   usuarios      │          │
├─────────────────┤          │
│ id (PK)        │          │
│ username (UK)  │          │
│ email (UK)     │          │
│ password_hash  │          │
│ nombres        │          │
│ apellidos      │          │
│ rol_id (FK)    │──────────┘
│ activo         │
│ created_at     │
│ updated_at     │
└─────────────────┘
        │
        │
        │ FK
        │
        ▼
┌─────────────────┐
│ logs_auditoria  │
├─────────────────┤
│ id (PK)        │
│ usuario_id (FK)│
│ accion         │
│ modulo         │
│ descripcion    │
│ ip_address     │
│ created_at     │
└─────────────────┘

┌─────────────────┐
│   permisos      │
├─────────────────┤
│ id (PK)        │
│ nombre         │
│ descripcion    │
│ modulo         │
└─────────────────┘
        ▲
        │
        │
┌───────┴─────────┐
│  rol_permisos   │
├─────────────────┤
│ id (PK)        │
│ rol_id (FK)    │
│ permiso_id (FK)│
└─────────────────┘
```

### Convenciones de Nombres
```sql
-- Tablas: plural, snake_case
usuarios, pacientes, citas_medicas

-- Columnas: snake_case
created_at, fecha_nacimiento, password_hash

-- Primary Keys: id (serial)
id SERIAL PRIMARY KEY

-- Foreign Keys: [tabla_singular]_id
usuario_id, paciente_id, medico_id

-- Índices: idx_[tabla]_[columna]
idx_usuarios_email, idx_pacientes_dpi

-- Unique constraints: uk_[tabla]_[columna]
uk_usuarios_username
```

### Tipos de Datos Usados
```sql
-- IDs
SERIAL / INTEGER

-- Texto corto
VARCHAR(50), VARCHAR(100), VARCHAR(255)

-- Texto largo
TEXT

-- Fechas y horas
DATE, TIMESTAMP, TIMESTAMP WITH TIME ZONE

-- Booleanos
BOOLEAN (true/false, not 0/1)

-- Decimales
DECIMAL(10,2) para dinero
DECIMAL(5,2) para medidas (peso, talla)

-- JSON (futuro)
JSONB para datos flexibles
```

---

## 🔒 Seguridad

### Capas de Seguridad
```
┌─────────────────────────────────────────────────┐
│ 1. Red Local (192.168.1.x)                     │
│    - No expuesto a internet                     │
│    - Firewall Windows activo                    │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 2. CORS (Backend)                               │
│    - Solo permite localhost:3000 y .10:3000     │
│    - Bloquea otros orígenes                     │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 3. Middleware Next.js (Frontend)                │
│    - Verifica token antes de cada página        │
│    - Redirect a login si no autenticado         │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 4. JWT Validation (Backend)                     │
│    - Verifica firma del token                   │
│    - Verifica expiración (30 min)               │
│    - Extrae usuario del token                   │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 5. Role-Based Access (Futuro)                   │
│    - Verifica permisos por rol                  │
│    - Bloquea acciones no autorizadas            │
└─────────────────────────────────────────────────┘
                     ▼
┌─────────────────────────────────────────────────┐
│ 6. Audit Logs (Implementado parcial)            │
│    - Registra quién hizo qué                    │
│    - Timestamp + IP + acción                    │
└─────────────────────────────────────────────────┘
```

### Hashing de Passwords
```python
# Usando bcrypt (cost factor = 12)
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash (al crear usuario)
hashed = pwd_context.hash("admin123")
# Resultado: $2b$12$...

# Verify (al login)
is_valid = pwd_context.verify("admin123", hashed)
# Resultado: True/False
```

**Por qué bcrypt**:
- ✅ Diseñado para ser lento (protege contra brute force)
- ✅ Salt automático (protege contra rainbow tables)
- ✅ Cost factor ajustable (futuro-proof)
- ✅ Ampliamente probado y confiable

### JWT Tokens
```python
# Estructura del token
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "sub": "admin",           # username
    "user_id": 1,             # user ID
    "exp": 1700000000         # expiration timestamp
  },
  "signature": "..."          # HMAC SHA256
}
```

**Configuración**:
- Algorithm: HS256 (HMAC SHA-256)
- Secret: Variable de entorno `SECRET_KEY`
- Expiration: 30 minutos
- Storage: Cookie HttpOnly (futuro) o LocalStorage (actual)

**Por qué JWT**:
- ✅ Stateless (no requiere DB para validar)
- ✅ Self-contained (incluye info del usuario)
- ✅ Estándar de industria
- ✅ Funciona bien con SPA

### Pendientes de Seguridad (Futuro)

- [ ] HTTPS con certificado SSL (nginx reverse proxy)
- [ ] Rate limiting por IP
- [ ] CSRF tokens
- [ ] HttpOnly cookies para JWT
- [ ] Refresh tokens (evitar re-login frecuente)
- [ ] 2FA (autenticación de dos factores)
- [ ] Encriptación de datos sensibles en BD
- [ ] Backups encriptados
- [ ] Logs de seguridad detallados

---

## 🚀 Deployment Local

### Topología de Red
```
                     Internet
                        │
                        │ (solo para npm/pip)
                        │
                   [Router WiFi]
                   192.168.1.1
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   [Laptop Dev]    [Lenovo Server]  [Tablets]
   192.168.1.x     192.168.1.10     192.168.1.y
                        │
                        ├─ PostgreSQL :5432
                        ├─ FastAPI :8000
                        └─ Next.js :3000
```

### Configuración de Red

**IP Estática en Windows**:
1. Panel de Control → Red
2. Propiedades de WiFi
3. IPv4 → Manual
4. IP: `192.168.1.10`
5. Máscara: `255.255.255.0`
6. Gateway: `192.168.1.1`
7. DNS: `8.8.8.8`

**Firewall**:
```powershell
# Permitir puertos
New-NetFirewallRule -DisplayName "FastAPI" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
New-NetFirewallRule -DisplayName "Next.js" -Direction Inbound -LocalPort 3000 -Protocol TCP -Action Allow
```

### Scripts de Inicio

**start-backend.bat**:
```batch
@echo off
cd C:\Users\tefi1\Documents\GitHub\clinica-dra-garcia\clinica\backend
call .\venv\Scripts\Activate.bat
start "Backend FastAPI" cmd /k "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
```

**start-frontend.bat**:
```batch
@echo off
cd C:\Users\tefi1\Documents\GitHub\clinica-dra-garcia\clinica\frontend
start "Frontend Next.js" cmd /k "npm run dev"
```

**start-all.bat**:
```batch
@echo off
echo Iniciando Sistema Clínico MEDGAR...
call start-backend.bat
timeout /t 5
call start-frontend.bat
echo.
echo Sistema iniciado. Acceder a:
echo   Local: http://localhost:3000
echo   Red:   http://192.168.1.10:3000
```

---

## 📈 Escalabilidad

### Escenarios Futuros

**Escenario 1: Segunda Sucursal (Año 1)**

Opciones:
1. **Dos instancias independientes** (recomendado inicialmente)
   - Pros: Simple, sin latencia entre sucursales
   - Contras: Datos separados, no sincronizados

2. **VPN + Base de datos compartida**
   - Pros: Datos centralizados
   - Contras: Latencia, punto único de falla

3. **Migración a cloud**
   - Pros: Acceso desde cualquier lugar
   - Contras: Costo mensual, dependencia de internet

**Escenario 2: Crecimiento a 5 Médicos (Año 2)**

Sistema actual soporta:
- ✅ 5 médicos simultáneos
- ✅ 500 pacientes/mes
- ✅ 10,000+ registros en BD

Posibles cuellos de botella:
- Espacio en disco (500 GB suficiente por ~3 años)
- RAM si muchos usuarios simultáneos (16 GB OK hasta 10 usuarios)

**Escenario 3: Telemedicina Remota (Año 2)**

Requerirá:
- Servidor accesible desde internet
- Certificado SSL
- Mayor ancho de banda
- Consideración de migrar a cloud

### Mejoras de Performance (Futuro)

**Backend**:
- [ ] Caché con Redis
- [ ] Database connection pooling (ya configurado)
- [ ] Compresión de responses (gzip)
- [ ] Pagination en todos los endpoints
- [ ] Índices adicionales en BD

**Frontend**:
- [ ] Lazy loading de componentes
- [ ] Optimización de imágenes (ya con Next.js)
- [ ] Service Worker para offline
- [ ] Memoización de componentes pesados

**Base de Datos**:
- [ ] Particionamiento de tablas grandes
- [ ] Índices en columnas más consultadas
- [ ] Vacuum automático configurado
- [ ] Estadísticas de performance

---

## 📊 Monitoreo (Futuro)

### Métricas a Monitorear

**Sistema**:
- CPU usage
- RAM usage
- Disk space
- Network latency

**Aplicación**:
- Response time de API
- Número de requests/segundo
- Errores 4xx/5xx
- Usuarios concurrentes

**Base de Datos**:
- Query time
- Connection pool usage
- Deadlocks
- Slow queries

**Herramientas Sugeridas**:
- Prometheus + Grafana
- PostgreSQL pg_stat_statements
- FastAPI middleware de logging

---

## 🔄 Migraciones (Futuro)

### Plan de Migración a Cloud (Si se requiere)

**Opción AWS**:
```
RDS PostgreSQL    → $25/mes (db.t3.micro)
EC2 Backend       → $15/mes (t3.micro)
S3 Archivos       → $5/mes (50 GB)
CloudFront CDN    → $5/mes
Total             → ~$50/mes
```

**Opción DigitalOcean**:
```
Droplet           → $12/mes (2 GB RAM)
Managed DB        → $15/mes
Spaces            → $5/mes
Total             → ~$32/mes
```

**Pasos de Migración**:
1. Backup completo de BD
2. Dump de PostgreSQL
3. Setup servidor cloud
4. Restore BD en cloud
5. Deploy backend
6. Deploy frontend
7. Actualizar DNS
8. Testing exhaustivo
9. Cutover

---

## 📚 Referencias

### Documentación Oficial
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- PostgreSQL: https://www.postgresql.org/docs/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Tailwind: https://tailwindcss.com/docs

### Libros Recomendados
- "Architecture Patterns with Python" - Harry Percival
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "FastAPI for APIs" - Bill Lubanovic (cuando salga)

### Tutoriales Útiles
- FastAPI + PostgreSQL: https://testdriven.io/blog/fastapi-crud/
- Next.js Authentication: https://next-auth.js.org/
- SQLAlchemy Relationships: https://docs.sqlalchemy.org/en/14/orm/tutorial.html

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0 - Sprint 1  
**Autor**: Equipo de Desarrollo  
**Revisión**: Pendiente