# 🏥 Sistema Clínico Dra. Estephanny García

Sistema integral de gestión clínica - Deployment local en Lenovo IdeaPad

## 📁 Estructura del Proyecto
```
clinica-dra-garcia/
├── clinica/
│   ├── backend/          # FastAPI + Python 3.13
│   ├── frontend/         # Next.js 25 + TypeScript
│   └── docs/            # Documentación
└── clinica-archivos/    # Archivos multimedia (no versionados)
    ├── pacientes/
    ├── inventario/
    ├── fel/
    └── backups/
```

## 🚀 Estado del Desarrollo - Sprint 1

### FASE 1: MVP - Core Médico
- [x] Estructura inicial
- [ ] PostgreSQL configurado
- [ ] Backend Base (FastAPI)
- [ ] Frontend Base (Next.js)
- [ ] Sistema de autenticación
- [ ] CRUD Usuarios

## 🛠️ Stack Tecnológico

**Backend:**
- Python 3.13.9
- FastAPI
- PostgreSQL 16
- SQLAlchemy + Alembic

**Frontend:**
- Node.js 25.2.1
- Next.js 14
- TypeScript
- Tailwind CSS + shadcn/ui

**Deployment:**
- Local: Lenovo IdeaPad Slim 3 15AMN8
- IP: 192.168.1.10:3000
- Sistema: Windows 11

## 💾 Base de Datos

**Nombre:** clinica_db  
**Usuario:** clinica_user  
**Puerto:** 5432

## 📝 Metodología

SCRUM - Sprints de 2 semanas
- Sprint actual: 1/12
- Fase actual: 1/5
```

---

## 🎯 PASO 5: Commit en GitHub Desktop

1. Abre **GitHub Desktop**
2. Verás los cambios en `.gitignore` y `README.md`
3. En el campo de commit escribe:
```
   feat: configuración inicial del proyecto
   
   - Estructura de carpetas ajustada
   - Gitignore configurado
   - README con información del stack
```
4. Click en **"Commit to feature/sprint-1-setup"**
5. Click en **"Push origin"**

---

## ✅ Checklist antes de continuar:
```
[ ] PostgreSQL agregado al PATH
[ ] Comando psql --version funciona
[ ] Base de datos clinica_db creada
[ ] Usuario clinica_user creado
[ ] Conexión a BD exitosa
[ ] Commit subido a GitHub