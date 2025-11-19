from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema Clínico Dra. García - MEDGAR",
    description="API completa para gestión clínica integral",
    version="2.0.0",
    debug=True
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://192.168.1.10:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# IMPORTAR TODOS LOS ROUTERS
# ============================================================================

from app.routers import (
    pacientes,
    citas,
    medicamentos,
    consultas,
    antecedentes,
    recetas,
    hospitalizacion,
    notas_medicas,
    ordenes_medicas,
    laboratorios,
    vacunas,
    lista_espera,
    interconsultas,
    caja,
    farmacia,
    reportes
)

# ============================================================================
# REGISTRAR TODOS LOS ROUTERS
# ============================================================================

# Módulo: Pacientes
app.include_router(pacientes.router, prefix="/api", tags=["Pacientes"])

# Módulo: Citas y Agenda
app.include_router(citas.router, prefix="/api", tags=["Citas"])
app.include_router(lista_espera.router, prefix="/api", tags=["Lista de Espera"])

# Módulo: Medicamentos
app.include_router(medicamentos.router, prefix="/api", tags=["Medicamentos"])

# Módulo: Consultas e Historia Clínica
app.include_router(consultas.router, prefix="/api", tags=["Consultas"])
app.include_router(antecedentes.router, prefix="/api", tags=["Antecedentes"])
app.include_router(vacunas.router, prefix="/api", tags=["Vacunación"])
app.include_router(interconsultas.router, prefix="/api", tags=["Interconsultas"])

# Módulo: Recetas
app.include_router(recetas.router, prefix="/api", tags=["Recetas"])

# Módulo: Hospitalización
app.include_router(hospitalizacion.router, prefix="/api", tags=["Hospitalización"])
app.include_router(notas_medicas.router, prefix="/api", tags=["Notas Médicas"])
app.include_router(ordenes_medicas.router, prefix="/api", tags=["Órdenes Médicas"])

# Módulo: Laboratorios
app.include_router(laboratorios.router, prefix="/api", tags=["Laboratorios"])

# Módulo: Caja y Facturación
app.include_router(caja.router, prefix="/api", tags=["Caja y Facturación"])

# Módulo: Farmacia e Inventario
app.include_router(farmacia.router, prefix="/api", tags=["Farmacia e Inventario"])

# Módulo: Reportes
app.include_router(reportes.router, prefix="/api", tags=["Reportes"])

# ============================================================================
# ENDPOINTS RAÍZ
# ============================================================================

@app.get("/")
def read_root():
    return {
        "message": "🏥 API Sistema Clínico MEDGAR - COMPLETO",
        "version": "2.0.0",
        "status": "✅ online",
        "docs": "/docs",
        "modulos_completos": [
            "✅ Pacientes (9 endpoints)",
            "✅ Citas (7 endpoints)",
            "✅ Lista de Espera (4 endpoints)",
            "✅ Medicamentos (5 endpoints)",
            "✅ Consultas (5 endpoints)",
            "✅ Antecedentes (5 endpoints)",
            "✅ Vacunación (4 endpoints)",
            "✅ Interconsultas (4 endpoints)",
            "✅ Recetas (4 endpoints)",
            "✅ Hospitalización (11 endpoints)",
            "✅ Notas Médicas (3 endpoints)",
            "✅ Órdenes Médicas (3 endpoints)",
            "✅ Laboratorios (6 endpoints)",
            "✅ Caja y Facturación (13 endpoints)",
            "✅ Farmacia e Inventario (15 endpoints)",
            "✅ Reportes (5 endpoints)"
        ],
        "total_endpoints": 103
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "database": "PostgreSQL",
        "tables": 31,
        "modules": 16
    }

@app.get("/api/info")
def api_info():
    """Información detallada de la API"""
    return {
        "nombre": "Sistema Clínico MEDGAR",
        "version": "2.0.0",
        "descripcion": "Sistema COMPLETO de gestión clínica - Todos los módulos implementados",
        "cliente": "Dra. Estephanny García",
        "tecnologias": {
            "backend": "FastAPI + Python 3.11",
            "database": "PostgreSQL 15",
            "orm": "SQLAlchemy",
            "validation": "Pydantic v2"
        },
        "modulos": {
            "pacientes": "/api/pacientes",
            "citas": "/api/citas",
            "lista_espera": "/api/lista-espera",
            "medicamentos": "/api/medicamentos",
            "consultas": "/api/consultas",
            "antecedentes": "/api/antecedentes",
            "vacunas": "/api/vacunas",
            "interconsultas": "/api/interconsultas",
            "recetas": "/api/recetas",
            "hospitalizacion": "/api/hospitalizacion",
            "notas_medicas": "/api/notas-medicas",
            "ordenes_medicas": "/api/ordenes-medicas",
            "laboratorios": "/api/laboratorios",
            "caja": "/api/caja",
            "farmacia": "/api/farmacia",
            "reportes": "/api/reportes"
        },
        "documentacion": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "estadisticas": {
            "total_tablas": 31,
            "total_endpoints": 103,
            "total_modulos": 16
        }
    }