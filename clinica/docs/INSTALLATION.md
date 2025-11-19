# 🚀 Guía de Instalación - Sistema Clínico MEDGAR

Guía paso a paso para configurar el ambiente de desarrollo desde cero.

## 📋 Índice
1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación de Software Base](#instalación-de-software-base)
3. [Configuración de PostgreSQL](#configuración-de-postgresql)
4. [Setup del Backend](#setup-del-backend)
5. [Setup del Frontend](#setup-del-frontend)
6. [Inicialización de Datos](#inicialización-de-datos)
7. [Verificación de Instalación](#verificación-de-instalación)
8. [Solución de Problemas Comunes](#solución-de-problemas-comunes)

---

## 💻 Requisitos del Sistema

### Hardware Mínimo
- **CPU**: 4 cores @ 2.0 GHz
- **RAM**: 8 GB (16 GB recomendado)
- **Disco**: 50 GB libres (SSD recomendado)
- **Red**: WiFi o Ethernet

### Hardware Actual del Proyecto
```yaml
Dispositivo: Lenovo IdeaPad Slim 3 15AMN8
CPU: AMD Ryzen 5 7520U (4 cores @ 2.8GHz)
RAM: 16 GB
Storage: 500 GB SSD
OS: Windows 11 Pro
Estado: ✅ APTO
```

---

## 📦 Instalación de Software Base

### 1. Node.js 20 LTS

**Descargar**: https://nodejs.org/
```powershell
# Verificar instalación
node --version
# Esperado: v20.x.x o superior

npm --version
# Esperado: 10.x.x o superior
```

### 2. Python 3.13

**Descargar**: https://www.python.org/downloads/

⚠️ **IMPORTANTE**: Marcar "Add Python to PATH" durante instalación
```powershell
# Verificar instalación
python --version
# Esperado: Python 3.13.x

pip --version
# Esperado: pip 25.x
```

### 3. PostgreSQL 18

**Descargar**: https://www.postgresql.org/download/windows/

**Durante instalación**:
- Puerto: `5432` (default)
- Contraseña de postgres: **Anótala bien**
- Instalar Stack Builder: No necesario
- Locale: Spanish, Guatemala (opcional)
```powershell
# Verificar instalación
psql --version
# Esperado: psql (PostgreSQL) 18.x
```

**Si `psql` no se reconoce**:

1. Agregar al PATH de Windows:
   - `C:\Program Files\PostgreSQL\18\bin`
2. Reiniciar PowerShell

### 4. Git

**Descargar**: https://git-scm.com/
```powershell
# Verificar instalación
git --version
# Esperado: git version 2.x
```

### 5. GitHub Desktop (Opcional pero recomendado)

**Descargar**: https://desktop.github.com/

---

## 🗄️ Configuración de PostgreSQL

### Paso 1: Conectar a PostgreSQL
```powershell
psql -U postgres
# Ingresar contraseña que configuraste
```

### Paso 2: Crear Base de Datos y Usuario
```sql
-- Crear base de datos
CREATE DATABASE clinica_db;

-- Crear usuario
CREATE USER clinica_user WITH PASSWORD 'clinica2025!';

-- Dar permisos
GRANT ALL PRIVILEGES ON DATABASE clinica_db TO clinica_user;

-- Conectar a la base de datos
\c clinica_db

-- Dar permisos al schema
GRANT ALL ON SCHEMA public TO clinica_user;

-- Salir
\q
```

### Paso 3: Verificar Conexión
```powershell
psql -U clinica_user -d clinica_db -h localhost
# Contraseña: clinica2025!
```

Si conecta exitosamente:
```
clinica_db=>
```

Escribir `\q` para salir.

---

## 🔧 Setup del Backend

### Paso 1: Navegar a la carpeta
```powershell
cd C:\Users\[TU_USUARIO]\Documents\GitHub\clinica-dra-garcia\clinica\backend
```

### Paso 2: Crear entorno virtual
```powershell
python -m venv venv
```

### Paso 3: Activar entorno virtual

#### Windows PowerShell:
```powershell
.\venv\Scripts\Activate
```

**Si da error de permisos**, ejecutar como Administrador:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Deberías ver `(venv)` al inicio de tu terminal.

### Paso 4: Instalar dependencias
```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

**Tiempo aproximado**: 2-3 minutos

### Paso 5: Crear archivo .env

Crear archivo `clinica/backend/.env`:
```env
# Database
DATABASE_URL=postgresql://clinica_user:clinica2025!@localhost:5432/clinica_db

# Security
SECRET_KEY=tu_super_secret_key_cambiar_en_produccion_123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Server
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
ALLOWED_ORIGINS=["http://localhost:3000","http://192.168.1.10:3000"]
```

⚠️ **IMPORTANTE**: Cambiar `SECRET_KEY` en producción

### Paso 6: Verificar configuración
```powershell
python -c "from app.core.config import settings; print(settings.PROJECT_NAME)"
```

**Esperado**: `Sistema Clínico Dra. García`

---

## 🎨 Setup del Frontend

### Paso 1: Navegar a la carpeta
```powershell
cd C:\Users\[TU_USUARIO]\Documents\GitHub\clinica-dra-garcia\clinica\frontend
```

### Paso 2: Instalar dependencias
```powershell
npm install
```

**Tiempo aproximado**: 3-5 minutos

### Paso 3: Crear archivo .env.local

Crear archivo `clinica/frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

### Paso 4: Agregar logos

Copiar los archivos de logos en:
- `public/logo-medgar.png` (logo completo)
- `public/icon-medgar.png` (solo ícono)

### Paso 5: Verificar configuración
```powershell
npm run build
```

Si compila sin errores, está bien configurado.

---

## 🌱 Inicialización de Datos

### Paso 1: Volver al backend
```powershell
cd C:\Users\[TU_USUARIO]\Documents\GitHub\clinica-dra-garcia\clinica\backend
.\venv\Scripts\Activate
```

### Paso 2: Ejecutar script de inicialización
```powershell
python init_database.py
```

**Salida esperada**:
```
🚀 Inicializando base de datos...

📋 Creando roles...
✅ Rol creado: Administrador
✅ Rol creado: Médico
✅ Rol creado: Enfermera
✅ Rol creado: Recepcionista

🔐 Creando permisos...
✅ Permiso creado: pacientes.ver
✅ Permiso creado: pacientes.crear
... (más permisos)

👤 Creando usuario administrador...
✅ Usuario administrador creado
   Username: admin
   Password: admin123

✅ Base de datos inicializada correctamente
```

### Paso 3: Verificar en PostgreSQL
```powershell
psql -U clinica_user -d clinica_db -h localhost
```
```sql
-- Ver roles
SELECT * FROM roles;

-- Ver usuarios
SELECT id, username, email, nombres, apellidos FROM usuarios;

-- Salir
\q
```

---

## ✅ Verificación de Instalación

### 1. Iniciar Backend

**Terminal 1**:
```powershell
cd clinica/backend
.\venv\Scripts\Activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Verificar**:
- Abrir: http://localhost:8000
- Deberías ver:
```json
{
  "message": "Bienvenido a Sistema Clínico Dra. García",
  "version": "1.0.0",
  "status": "online"
}
```

- Abrir: http://localhost:8000/docs
- Deberías ver Swagger UI

### 2. Iniciar Frontend

**Terminal 2** (nueva ventana):
```powershell
cd clinica/frontend
npm run dev
```

**Verificar**:
- Abrir: http://localhost:3000
- Deberías ver la página de login con logo MEDGAR

### 3. Probar Login

1. Usuario: `admin`
2. Contraseña: `admin123`
3. Click "Iniciar Sesión"
4. Deberías ver el Dashboard

### 4. Probar Logout

1. Click en "Cerrar Sesión"
2. Deberías volver al login

---

## 🐛 Solución de Problemas Comunes

### Error: "psql no se reconoce"

**Solución**:
1. Agregar a PATH: `C:\Program Files\PostgreSQL\18\bin`
2. Reiniciar terminal

### Error: "No se puede activar venv en PowerShell"

**Solución**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Error: "email-validator no instalado"

**Solución**:
```powershell
cd clinica/backend
.\venv\Scripts\Activate
pip install email-validator
```

### Error: "CORS policy" en frontend

**Solución**:
Verificar que en `backend/.env`:
```env
ALLOWED_ORIGINS=["http://localhost:3000","http://192.168.1.10:3000"]
```

### Error: "Cannot connect to database"

**Solución**:
1. Verificar que PostgreSQL esté corriendo
2. Verificar credenciales en `.env`
3. Probar conexión:
```powershell
psql -U clinica_user -d clinica_db -h localhost
```

### Error: Puerto 3000 o 8000 en uso

**Solución**:
```powershell
# Ver qué está usando el puerto
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Matar proceso (reemplazar PID)
taskkill /PID [número] /F
```

### Frontend no carga logos

**Solución**:
1. Verificar archivos en `public/`
2. Reiniciar servidor Next.js
3. Limpiar caché: `npm run build`

---

## 🎯 Checklist Final

Marca cada item cuando esté completado:

- [ ] Node.js instalado y verificado
- [ ] Python instalado y verificado
- [ ] PostgreSQL instalado y verificado
- [ ] Git instalado y verificado
- [ ] Base de datos `clinica_db` creada
- [ ] Usuario `clinica_user` creado
- [ ] Backend: venv creado y activado
- [ ] Backend: dependencias instaladas
- [ ] Backend: archivo .env creado
- [ ] Frontend: dependencias instaladas
- [ ] Frontend: archivo .env.local creado
- [ ] Frontend: logos agregados
- [ ] Script init_database.py ejecutado exitosamente
- [ ] Backend corriendo en http://localhost:8000
- [ ] Frontend corriendo en http://localhost:3000
- [ ] Login funcional con admin/admin123
- [ ] Dashboard visible después de login
- [ ] Logout funcional

---

## 📞 Siguiente Paso

Una vez completada la instalación, continúa con:
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) - Documentación de endpoints
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Guía de desarrollo

---

**Última actualización**: Noviembre 2025  
**Versión**: 1.0 - Sprint 1