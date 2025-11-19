from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from datetime import date, datetime
from pydantic import BaseModel
from create_simple_tables import Vacuna, TipoVacunaEnum, Paciente, Usuario

# ============================================================================
# SCHEMAS
# ============================================================================

class VacunaBase(BaseModel):
    paciente_id: int
    tipo_vacuna: TipoVacunaEnum
    dosis: str
    fecha_aplicacion: date
    lote: Optional[str] = None
    lugar_aplicacion: Optional[str] = None
    medico_id: Optional[int] = None
    observaciones: Optional[str] = None

class VacunaCreate(VacunaBase):
    pass

class VacunaResponse(VacunaBase):
    id: int
    created_at: datetime
    medico_nombre: Optional[str] = None

    class Config:
        from_attributes = True

class EsquemaVacunacion(BaseModel):
    paciente_id: int
    edad_meses: int
    vacunas_aplicadas: List[VacunaResponse]
    vacunas_pendientes: List[dict]

# ============================================================================
# ROUTER
# ============================================================================

router = APIRouter(
    prefix="/vacunas",
    tags=["Vacunación"]
)

# ============================================================================
# ENDPOINTS
# ============================================================================

@router.post("/", response_model=VacunaResponse, status_code=status.HTTP_201_CREATED)
def registrar_vacuna(vacuna: VacunaCreate, db: Session = Depends(get_db)):
    """Registrar aplicación de vacuna"""
    
    # Verificar paciente
    paciente = db.query(Paciente).filter(Paciente.id == vacuna.paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    db_vacuna = Vacuna(**vacuna.model_dump())
    db.add(db_vacuna)
    db.commit()
    db.refresh(db_vacuna)
    
    response = VacunaResponse.model_validate(db_vacuna)
    
    if db_vacuna.medico_id:
        medico = db.query(Usuario).filter(Usuario.id == db_vacuna.medico_id).first()
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    
    return response

@router.get("/paciente/{paciente_id}", response_model=List[VacunaResponse])
def listar_vacunas_paciente(
    paciente_id: int,
    tipo_vacuna: Optional[TipoVacunaEnum] = None,
    db: Session = Depends(get_db)
):
    """Listar vacunas de un paciente"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    query = db.query(Vacuna).filter(Vacuna.paciente_id == paciente_id)
    
    if tipo_vacuna:
        query = query.filter(Vacuna.tipo_vacuna == tipo_vacuna)
    
    vacunas = query.order_by(Vacuna.fecha_aplicacion.desc()).all()
    
    result = []
    for vac in vacunas:
        response = VacunaResponse.model_validate(vac)
        if vac.medico_id:
            medico = db.query(Usuario).filter(Usuario.id == vac.medico_id).first()
            if medico:
                response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        result.append(response)
    
    return result

@router.get("/paciente/{paciente_id}/esquema", response_model=EsquemaVacunacion)
def obtener_esquema_vacunacion(paciente_id: int, db: Session = Depends(get_db)):
    """Obtener esquema de vacunación del paciente con pendientes"""
    
    paciente = db.query(Paciente).filter(Paciente.id == paciente_id).first()
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")
    
    # Calcular edad en meses
    hoy = date.today()
    edad_meses = (hoy.year - paciente.fecha_nacimiento.year) * 12 + (hoy.month - paciente.fecha_nacimiento.month)
    
    # Obtener vacunas aplicadas
    vacunas = db.query(Vacuna).filter(Vacuna.paciente_id == paciente_id).order_by(Vacuna.fecha_aplicacion).all()
    
    vacunas_aplicadas = []
    for vac in vacunas:
        response = VacunaResponse.model_validate(vac)
        if vac.medico_id:
            medico = db.query(Usuario).filter(Usuario.id == vac.medico_id).first()
            if medico:
                response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
        vacunas_aplicadas.append(response)
    
    # Esquema de vacunación según edad (simplificado)
    esquema_completo = {
        0: [
            {"tipo": "BCG", "dosis": "Dosis única"},
            {"tipo": "Hepatitis B", "dosis": "1ra dosis"}
        ],
        2: [
            {"tipo": "Pentavalente", "dosis": "1ra dosis"},
            {"tipo": "Rotavirus", "dosis": "1ra dosis"},
            {"tipo": "Neumococo", "dosis": "1ra dosis"}
        ],
        4: [
            {"tipo": "Pentavalente", "dosis": "2da dosis"},
            {"tipo": "Rotavirus", "dosis": "2da dosis"},
            {"tipo": "Neumococo", "dosis": "2da dosis"}
        ],
        6: [
            {"tipo": "Pentavalente", "dosis": "3ra dosis"},
            {"tipo": "Influenza", "dosis": "1ra dosis"}
        ],
        12: [
            {"tipo": "SRP (Sarampión, Rubéola, Paperas)", "dosis": "1ra dosis"},
            {"tipo": "Varicela", "dosis": "1ra dosis"}
        ],
        18: [
            {"tipo": "Pentavalente", "dosis": "Refuerzo"},
            {"tipo": "SRP (Sarampión, Rubéola, Paperas)", "dosis": "2da dosis"}
        ]
    }
    
    # Determinar vacunas pendientes
    vacunas_pendientes = []
    vacunas_aplicadas_set = {(v.tipo_vacuna.value, v.dosis) for v in vacunas}
    
    for mes, vacunas_mes in esquema_completo.items():
        if edad_meses >= mes:
            for vac in vacunas_mes:
                if (vac["tipo"], vac["dosis"]) not in vacunas_aplicadas_set:
                    vacunas_pendientes.append({
                        "tipo_vacuna": vac["tipo"],
                        "dosis": vac["dosis"],
                        "edad_recomendada_meses": mes,
                        "atrasada": edad_meses > mes + 2  # Atrasada si pasaron más de 2 meses
                    })
    
    return {
        "paciente_id": paciente_id,
        "edad_meses": edad_meses,
        "vacunas_aplicadas": vacunas_aplicadas,
        "vacunas_pendientes": vacunas_pendientes
    }

@router.get("/{vacuna_id}", response_model=VacunaResponse)
def obtener_vacuna(vacuna_id: int, db: Session = Depends(get_db)):
    """Obtener una vacuna por ID"""
    
    vacuna = db.query(Vacuna).filter(Vacuna.id == vacuna_id).first()
    if not vacuna:
        raise HTTPException(status_code=404, detail="Vacuna no encontrada")
    
    response = VacunaResponse.model_validate(vacuna)
    if vacuna.medico_id:
        medico = db.query(Usuario).filter(Usuario.id == vacuna.medico_id).first()
        if medico:
            response.medico_nombre = f"{medico.nombres} {medico.apellidos}"
    
    return response