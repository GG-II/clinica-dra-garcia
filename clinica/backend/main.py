from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Sistema Clínico Dra. García - MEDGAR",
    description="API para gestión clínica integral",
    version="1.0.0",
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
    reportes
)

# ============================================================================
# REGISTRAR TODOS LOS ROUTERS
# ============================================================================

# Pacientes
app.include_router(pacientes.router, prefix="/api", tags=["Pacientes"])

# Citas
app.include_router(citas.router, prefix="/api", tags=["Citas"])

# Medicamentos
app.include_router(medicamentos.router, prefix="/api", tags=["Medicamentos"])

# Consultas
app.include_router(consultas.router, prefix="/api", tags=["Consultas"])

# Antecedentes
app.include_router(antecedentes.router, prefix="/api", tags=["Antecedentes"])

# Recetas
app.include_router(recetas.router, prefix="/api", tags=["Recetas"])

# Hospitalización
app.include_router(hospitalizacion.router, prefix="/api", tags=["Hospitalización"])

# Reportes
app.include_router(reportes.router, prefix="/api", tags=["Reportes"])

# ============================================================================
# ENDPOINTS RAÍZ
# ============================================================================

@app.get("/")
def read_root():
    return {
        "message": "API Sistema Clínico MEDGAR",
        "version": "1.0.0",
        "status": "online",
        "docs": "/docs",
        "modulos": [
            "Pacientes",
            "Citas",
            "Medicamentos",
            "Consultas",
            "Antecedentes",
            "Recetas",
            "Hospitalización",
            "Reportes"
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/info")
def api_info():
    """Información detallada de la API"""
    return {
        "nombre": "Sistema Clínico MEDGAR",
        "version": "1.0.0",
        "descripcion": "Sistema integral de gestión clínica",
        "endpoints_disponibles": {
            "pacientes": "/api/pacientes",
            "citas": "/api/citas",
            "medicamentos": "/api/medicamentos",
            "consultas": "/api/consultas",
            "antecedentes": "/api/antecedentes",
            "recetas": "/api/recetas",
            "hospitalizacion": "/api/hospitalizacion",
            "reportes": "/api/reportes"
        },
        "documentacion": "/docs",
        "documentacion_alternativa": "/redoc"
    }