from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from database import get_db
from datetime import datetime, date, timedelta
from pydantic import BaseModel
from typing import List, Dict, Optional, Any 
from typing import List, Dict, Optional
from create_simple_tables import (
    Paciente, Cita, Consulta, Hospitalizacion, Receta, 
    GeneroEnum, TipoCitaEnum, EstadoCitaEnum
)

# ============================================================================
# SCHEMAS
# ============================================================================

class DashboardData(BaseModel):
    # Pacientes
    total_pacientes: int
    pacientes_nuevos_mes: int
    
    # Citas
    citas_hoy: int
    citas_semana: int
    citas_pendientes: int
    
    # Consultas
    consultas_hoy: int
    consultas_mes: int
    
    # Hospitalización
    camas_ocupadas: int
    total_camas: int
    porcentaje_ocupacion: float
    
    # Recetas
    recetas_mes: int

class ReportePacientes(BaseModel):
    total: int
    activos: int
    inactivos: int
    por_genero: Dict[str, int]
    nuevos_por_mes: Dict[str, int]  # Últimos 6 meses

class ReporteCitas(BaseModel):
    total_mes: int
    por_tipo: Dict[str, int]
    por_estado: Dict[str, int]
    por_medico: List[Dict[str, Any]]
    tasa_asistencia: float

class ReporteConsultas(BaseModel):
    total_mes: int
    por_medico: List[Dict[str, Any]]
    diagnosticos_frecuentes: List[Dict[str, Any]]

class ReporteHospitalizacion(BaseModel):
    total_mes: int
    promedio_estancia: float
    ocupacion_promedio: float
    ingresos_por_dia: Dict[str, int]

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.get("/dashboard", response_model=DashboardData)
def obtener_dashboard(db: Session = Depends(get_db)):
    """Obtener datos para el dashboard principal"""
    
    hoy = date.today()
    inicio_mes = hoy.replace(day=1)
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    
    # Pacientes
    total_pacientes = db.query(Paciente).filter(Paciente.activo == True).count()
    pacientes_nuevos_mes = db.query(Paciente).filter(
        Paciente.created_at >= inicio_mes
    ).count()
    
    # Citas
    citas_hoy = db.query(Cita).filter(
        func.date(Cita.fecha_hora) == hoy
    ).count()
    
    citas_semana = db.query(Cita).filter(
        func.date(Cita.fecha_hora) >= inicio_semana,
        func.date(Cita.fecha_hora) <= hoy
    ).count()
    
    citas_pendientes = db.query(Cita).filter(
        Cita.estado.in_([EstadoCitaEnum.programada, EstadoCitaEnum.confirmada]),
        func.date(Cita.fecha_hora) >= hoy
    ).count()
    
    # Consultas
    consultas_hoy = db.query(Consulta).filter(
        func.date(Consulta.fecha_hora) == hoy
    ).count()
    
    consultas_mes = db.query(Consulta).filter(
        Consulta.created_at >= inicio_mes
    ).count()
    
    # Hospitalización
    from create_simple_tables import Cama, EstadoCamaEnum
    total_camas = db.query(Cama).count()
    camas_ocupadas = db.query(Cama).filter(Cama.estado == EstadoCamaEnum.ocupada).count()
    porcentaje_ocupacion = (camas_ocupadas / total_camas * 100) if total_camas > 0 else 0
    
    # Recetas
    recetas_mes = db.query(Receta).filter(
        Receta.created_at >= inicio_mes
    ).count()
    
    return {
        "total_pacientes": total_pacientes,
        "pacientes_nuevos_mes": pacientes_nuevos_mes,
        "citas_hoy": citas_hoy,
        "citas_semana": citas_semana,
        "citas_pendientes": citas_pendientes,
        "consultas_hoy": consultas_hoy,
        "consultas_mes": consultas_mes,
        "camas_ocupadas": camas_ocupadas,
        "total_camas": total_camas,
        "porcentaje_ocupacion": round(porcentaje_ocupacion, 2),
        "recetas_mes": recetas_mes
    }

@router.get("/pacientes", response_model=ReportePacientes)
def reporte_pacientes(db: Session = Depends(get_db)):
    """Reporte detallado de pacientes"""
    
    total = db.query(Paciente).count()
    activos = db.query(Paciente).filter(Paciente.activo == True).count()
    inactivos = total - activos
    
    # Por género
    por_genero = {}
    generos = db.query(
        Paciente.genero,
        func.count(Paciente.id)
    ).group_by(Paciente.genero).all()
    
    for genero, count in generos:
        por_genero[genero.value if genero else "No especificado"] = count
    
    # Nuevos por mes (últimos 6 meses)
    nuevos_por_mes = {}
    for i in range(6):
        fecha = datetime.now() - timedelta(days=30*i)
        mes_nombre = fecha.strftime("%B %Y")
        
        count = db.query(Paciente).filter(
            extract('year', Paciente.created_at) == fecha.year,
            extract('month', Paciente.created_at) == fecha.month
        ).count()
        
        nuevos_por_mes[mes_nombre] = count
    
    return {
        "total": total,
        "activos": activos,
        "inactivos": inactivos,
        "por_genero": por_genero,
        "nuevos_por_mes": nuevos_por_mes
    }

@router.get("/citas", response_model=ReporteCitas)
def reporte_citas(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Reporte detallado de citas"""
    
    if not fecha_desde:
        fecha_desde = datetime.now().replace(day=1).date()
    if not fecha_hasta:
        fecha_hasta = date.today()
    
    query = db.query(Cita).filter(
        func.date(Cita.fecha_hora) >= fecha_desde,
        func.date(Cita.fecha_hora) <= fecha_hasta
    )
    
    total_mes = query.count()
    
    # Por tipo
    por_tipo = {}
    tipos = query.with_entities(
        Cita.tipo_cita,
        func.count(Cita.id)
    ).group_by(Cita.tipo_cita).all()
    
    for tipo, count in tipos:
        por_tipo[tipo.value] = count
    
    # Por estado
    por_estado = {}
    estados = query.with_entities(
        Cita.estado,
        func.count(Cita.id)
    ).group_by(Cita.estado).all()
    
    for estado, count in estados:
        por_estado[estado.value] = count
    
    # Por médico
    from create_simple_tables import Usuario
    por_medico = []
    medicos = query.join(Usuario, Cita.medico_id == Usuario.id).with_entities(
        Usuario.id,
        Usuario.nombres,
        Usuario.apellidos,
        func.count(Cita.id)
    ).group_by(Usuario.id, Usuario.nombres, Usuario.apellidos).all()
    
    for medico_id, nombres, apellidos, count in medicos:
        por_medico.append({
            "medico_id": medico_id,
            "nombre": f"{nombres} {apellidos}",
            "total_citas": count
        })
    
    # Tasa de asistencia
    total_citas = query.count()
    citas_completadas = query.filter(Cita.estado == EstadoCitaEnum.completada).count()
    tasa_asistencia = (citas_completadas / total_citas * 100) if total_citas > 0 else 0
    
    return {
        "total_mes": total_mes,
        "por_tipo": por_tipo,
        "por_estado": por_estado,
        "por_medico": por_medico,
        "tasa_asistencia": round(tasa_asistencia, 2)
    }

@router.get("/consultas", response_model=ReporteConsultas)
def reporte_consultas(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Reporte detallado de consultas"""
    
    if not fecha_desde:
        fecha_desde = datetime.now().replace(day=1).date()
    if not fecha_hasta:
        fecha_hasta = date.today()
    
    query = db.query(Consulta).filter(
        func.date(Consulta.fecha_hora) >= fecha_desde,
        func.date(Consulta.fecha_hora) <= fecha_hasta
    )
    
    total_mes = query.count()
    
    # Por médico
    from create_simple_tables import Usuario
    por_medico = []
    medicos = query.join(Usuario, Consulta.medico_id == Usuario.id).with_entities(
        Usuario.id,
        Usuario.nombres,
        Usuario.apellidos,
        func.count(Consulta.id)
    ).group_by(Usuario.id, Usuario.nombres, Usuario.apellidos).all()
    
    for medico_id, nombres, apellidos, count in medicos:
        por_medico.append({
            "medico_id": medico_id,
            "nombre": f"{nombres} {apellidos}",
            "total_consultas": count
        })
    
    # Diagnósticos más frecuentes (simplificado)
    diagnosticos = query.filter(
        Consulta.diagnostico.isnot(None),
        Consulta.diagnostico != ""
    ).with_entities(
        Consulta.diagnostico,
        func.count(Consulta.id)
    ).group_by(Consulta.diagnostico).order_by(func.count(Consulta.id).desc()).limit(10).all()
    
    diagnosticos_frecuentes = []
    for diag, count in diagnosticos:
        diagnosticos_frecuentes.append({
            "diagnostico": diag,
            "cantidad": count
        })
    
    return {
        "total_mes": total_mes,
        "por_medico": por_medico,
        "diagnosticos_frecuentes": diagnosticos_frecuentes
    }

@router.get("/hospitalizacion", response_model=ReporteHospitalizacion)
def reporte_hospitalizacion(
    fecha_desde: Optional[date] = None,
    fecha_hasta: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Reporte detallado de hospitalización"""
    
    if not fecha_desde:
        fecha_desde = datetime.now().replace(day=1).date()
    if not fecha_hasta:
        fecha_hasta = date.today()
    
    query = db.query(Hospitalizacion).filter(
        func.date(Hospitalizacion.fecha_ingreso) >= fecha_desde,
        func.date(Hospitalizacion.fecha_ingreso) <= fecha_hasta
    )
    
    total_mes = query.count()
    
    # Promedio de estancia
    hospitalizaciones = query.all()
    dias_totales = 0
    count_egresos = 0
    
    for hosp in hospitalizaciones:
        if hosp.fecha_egreso:
            dias = (hosp.fecha_egreso - hosp.fecha_ingreso).days
            dias_totales += dias
            count_egresos += 1
    
    promedio_estancia = (dias_totales / count_egresos) if count_egresos > 0 else 0
    
    # Ocupación promedio (simplificado)
    from create_simple_tables import Cama, EstadoCamaEnum
    total_camas = db.query(Cama).count()
    hospitalizaciones_activas_promedio = db.query(Hospitalizacion).filter(
        Hospitalizacion.activa == True
    ).count()
    
    ocupacion_promedio = (hospitalizaciones_activas_promedio / total_camas * 100) if total_camas > 0 else 0
    
    # Ingresos por día
    ingresos_por_dia = {}
    ingresos = db.query(
        func.date(Hospitalizacion.fecha_ingreso).label('fecha'),
        func.count(Hospitalizacion.id)
    ).filter(
        func.date(Hospitalizacion.fecha_ingreso) >= fecha_desde,
        func.date(Hospitalizacion.fecha_ingreso) <= fecha_hasta
    ).group_by(func.date(Hospitalizacion.fecha_ingreso)).all()
    
    for fecha, count in ingresos:
        ingresos_por_dia[fecha.strftime("%Y-%m-%d")] = count
    
    return {
        "total_mes": total_mes,
        "promedio_estancia": round(promedio_estancia, 2),
        "ocupacion_promedio": round(ocupacion_promedio, 2),
        "ingresos_por_dia": ingresos_por_dia
    }