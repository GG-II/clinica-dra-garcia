# 🧪 Guía de Testing - Sistema Clínico MEDGAR

## Información General

- **Framework de Testing**: pytest
- **Coverage Target**: 80%+
- **Estrategia**: Unit Tests + Integration Tests
- **CI/CD**: Por implementar

---

## 📋 Tabla de Contenidos

1. [Configuración del Entorno de Testing](#configuración-del-entorno-de-testing)
2. [Estructura de Tests](#estructura-de-tests)
3. [Tests Unitarios](#tests-unitarios)
4. [Tests de Integración](#tests-de-integración)
5. [Tests de API](#tests-de-api)
6. [Fixtures y Mocks](#fixtures-y-mocks)
7. [Cobertura de Código](#cobertura-de-código)
8. [Buenas Prácticas](#buenas-prácticas)

---

## 🔧 Configuración del Entorno de Testing

### Instalación de Dependencias
```bash
# Activar entorno virtual
cd clinica/backend
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows

# Instalar dependencias de testing
pip install pytest pytest-cov pytest-asyncio httpx faker
pip freeze > requirements-test.txt
```

### Archivo de Configuración: pytest.ini

**Crear:** `clinica\backend\pytest.ini`
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --strict-markers
    --tb=short
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --disable-warnings

markers =
    unit: Unit tests
    integration: Integration tests
    api: API endpoint tests
    slow: Slow running tests
    database: Tests that require database
```

---

## 📁 Estructura de Tests
```
clinica/backend/
│
├── app/
│   └── routers/
│       ├── pacientes.py
│       ├── citas.py
│       └── ...
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    # Fixtures compartidos
│   │
│   ├── unit/                          # Tests unitarios
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_schemas.py
│   │   └── test_utils.py
│   │
│   ├── integration/                   # Tests de integración
│   │   ├── __init__.py
│   │   ├── test_database.py
│   │   └── test_transactions.py
│   │
│   └── api/                           # Tests de API
│       ├── __init__.py
│       ├── test_pacientes_api.py
│       ├── test_citas_api.py
│       ├── test_consultas_api.py
│       ├── test_recetas_api.py
│       ├── test_hospitalizacion_api.py
│       ├── test_laboratorios_api.py
│       ├── test_caja_api.py
│       ├── test_farmacia_api.py
│       └── test_reportes_api.py
│
└── pytest.ini
```

---

## 🔬 Tests Unitarios

### Archivo: tests/conftest.py
```python
"""
Fixtures compartidos para todos los tests
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from database import Base, get_db
from create_simple_tables import *

# Base de datos en memoria para tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def test_db():
    """Crear base de datos de test en memoria"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    """Cliente de test para FastAPI"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_paciente_data():
    """Datos de ejemplo para crear paciente"""
    return {
        "nombres": "María",
        "apellidos": "González",
        "fecha_nacimiento": "1990-05-15",
        "dpi": "2547896541201",
        "genero": "Femenino",
        "direccion": "4ta calle 5-20 zona 1",
        "telefono": "55551234",
        "religion": "Católica",
        "estado_civil": "Casada",
        "tiene_igss": True,
        "contacto_emergencia_nombre": "Juan González",
        "contacto_emergencia_telefono": "55554321"
    }

@pytest.fixture
def sample_medicamento_data():
    """Datos de ejemplo para crear medicamento"""
    return {
        "nombre_generico": "Paracetamol",
        "nombre_comercial": "Tylenol",
        "presentacion": "Tableta",
        "concentracion": "500 mg",
        "via_administracion": "Oral",
        "contraindicaciones": "Insuficiencia hepática severa",
        "interacciones": "Warfarina"
    }

@pytest.fixture
def create_test_paciente(test_db, sample_paciente_data):
    """Crear paciente de prueba en BD"""
    paciente = Paciente(**sample_paciente_data)
    test_db.add(paciente)
    test_db.commit()
    test_db.refresh(paciente)
    return paciente

@pytest.fixture
def create_test_medico(test_db):
    """Crear médico de prueba"""
    from create_simple_tables import Usuario, Rol
    
    # Crear rol
    rol = Rol(nombre="Medico", descripcion="Médico")
    test_db.add(rol)
    test_db.commit()
    
    medico = Usuario(
        nombres="Carlos",
        apellidos="Méndez",
        email="carlos.mendez@clinica.com",
        password_hash="hashed_password",
        rol_id=rol.id,
        especialidad="Medicina Interna",
        registro_medico="12345"
    )
    test_db.add(medico)
    test_db.commit()
    test_db.refresh(medico)
    return medico
```

---

### Ejemplo: tests/unit/test_models.py
```python
"""
Tests unitarios para modelos
"""
import pytest
from datetime import date, datetime
from create_simple_tables import Paciente, GeneroEnum, EstadoCivilEnum

@pytest.mark.unit
class TestPacienteModel:
    """Tests para el modelo Paciente"""
    
    def test_crear_paciente(self, test_db, sample_paciente_data):
        """Test: Crear paciente exitosamente"""
        paciente = Paciente(**sample_paciente_data)
        test_db.add(paciente)
        test_db.commit()
        test_db.refresh(paciente)
        
        assert paciente.id is not None
        assert paciente.nombres == "María"
        assert paciente.apellidos == "González"
        assert paciente.genero == GeneroEnum.femenino
        assert paciente.activo is True
        assert paciente.created_at is not None
    
    def test_paciente_dpi_unico(self, test_db, sample_paciente_data):
        """Test: DPI debe ser único"""
        # Crear primer paciente
        paciente1 = Paciente(**sample_paciente_data)
        test_db.add(paciente1)
        test_db.commit()
        
        # Intentar crear segundo paciente con mismo DPI
        sample_paciente_data["nombres"] = "Ana"
        paciente2 = Paciente(**sample_paciente_data)
        test_db.add(paciente2)
        
        with pytest.raises(Exception):  # IntegrityError
            test_db.commit()
    
    def test_calcular_edad(self, test_db, sample_paciente_data):
        """Test: Cálculo de edad"""
        paciente = Paciente(**sample_paciente_data)
        test_db.add(paciente)
        test_db.commit()
        
        hoy = date.today()
        edad_esperada = hoy.year - paciente.fecha_nacimiento.year
        
        # Ajustar si aún no ha cumplido años este año
        if (hoy.month, hoy.day) < (paciente.fecha_nacimiento.month, paciente.fecha_nacimiento.day):
            edad_esperada -= 1
        
        assert edad_esperada == 34  # Nacido en 1990, edad aproximada
```

---

## 🔗 Tests de Integración

### Ejemplo: tests/integration/test_database.py
```python
"""
Tests de integración con base de datos
"""
import pytest
from create_simple_tables import Paciente, Consulta, Usuario

@pytest.mark.integration
@pytest.mark.database
class TestDatabaseIntegration:
    """Tests de integración con BD"""
    
    def test_relacion_paciente_consultas(
        self, 
        test_db, 
        create_test_paciente, 
        create_test_medico
    ):
        """Test: Relación entre paciente y consultas"""
        # Crear consulta
        consulta = Consulta(
            paciente_id=create_test_paciente.id,
            medico_id=create_test_medico.id,
            motivo_consulta="Dolor de cabeza",
            presion_sistolica=120,
            presion_diastolica=80
        )
        test_db.add(consulta)
        test_db.commit()
        
        # Verificar que la consulta está asociada al paciente
        consultas_paciente = test_db.query(Consulta).filter(
            Consulta.paciente_id == create_test_paciente.id
        ).all()
        
        assert len(consultas_paciente) == 1
        assert consultas_paciente[0].motivo_consulta == "Dolor de cabeza"
    
    def test_transaction_rollback(self, test_db, sample_paciente_data):
        """Test: Rollback en caso de error"""
        # Comenzar transacción
        paciente = Paciente(**sample_paciente_data)
        test_db.add(paciente)
        test_db.flush()
        
        paciente_id = paciente.id
        assert paciente_id is not None
        
        # Simular error y hacer rollback
        test_db.rollback()
        
        # Verificar que no se guardó
        paciente_guardado = test_db.query(Paciente).filter(
            Paciente.id == paciente_id
        ).first()
        
        assert paciente_guardado is None
```

---

## 🌐 Tests de API

### Ejemplo: tests/api/test_pacientes_api.py
```python
"""
Tests de API para módulo de pacientes
"""
import pytest

@pytest.mark.api
class TestPacientesAPI:
    """Tests para endpoints de pacientes"""
    
    def test_crear_paciente_exitoso(self, client, sample_paciente_data):
        """Test: POST /api/pacientes - Crear paciente"""
        response = client.post("/api/pacientes", json=sample_paciente_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["nombres"] == sample_paciente_data["nombres"]
        assert data["apellidos"] == sample_paciente_data["apellidos"]
        assert data["dpi"] == sample_paciente_data["dpi"]
        assert data["activo"] is True
        assert "id" in data
        assert "created_at" in data
    
    def test_crear_paciente_sin_datos_requeridos(self, client):
        """Test: POST /api/pacientes - Sin datos requeridos"""
        response = client.post("/api/pacientes", json={})
        
        assert response.status_code == 422  # Validation error
    
    def test_crear_paciente_dpi_duplicado(self, client, sample_paciente_data):
        """Test: POST /api/pacientes - DPI duplicado"""
        # Crear primer paciente
        client.post("/api/pacientes", json=sample_paciente_data)
        
        # Intentar crear segundo con mismo DPI
        response = client.post("/api/pacientes", json=sample_paciente_data)
        
        assert response.status_code == 400
        assert "DPI ya existe" in response.json()["detail"]
    
    def test_listar_pacientes(self, client, sample_paciente_data):
        """Test: GET /api/pacientes - Listar"""
        # Crear algunos pacientes
        client.post("/api/pacientes", json=sample_paciente_data)
        
        sample_paciente_data["dpi"] = "9999999999999"
        sample_paciente_data["nombres"] = "Ana"
        client.post("/api/pacientes", json=sample_paciente_data)
        
        # Listar
        response = client.get("/api/pacientes")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) >= 2
    
    def test_obtener_paciente_por_id(self, client, sample_paciente_data):
        """Test: GET /api/pacientes/{id} - Obtener por ID"""
        # Crear paciente
        response_create = client.post("/api/pacientes", json=sample_paciente_data)
        paciente_id = response_create.json()["id"]
        
        # Obtener por ID
        response = client.get(f"/api/pacientes/{paciente_id}")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["id"] == paciente_id
        assert data["nombres"] == sample_paciente_data["nombres"]
    
    def test_obtener_paciente_no_existente(self, client):
        """Test: GET /api/pacientes/{id} - Paciente no existe"""
        response = client.get("/api/pacientes/99999")
        
        assert response.status_code == 404
    
    def test_actualizar_paciente(self, client, sample_paciente_data):
        """Test: PUT /api/pacientes/{id} - Actualizar"""
        # Crear paciente
        response_create = client.post("/api/pacientes", json=sample_paciente_data)
        paciente_id = response_create.json()["id"]
        
        # Actualizar
        update_data = {"telefono": "99998888"}
        response = client.put(f"/api/pacientes/{paciente_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["telefono"] == "99998888"
    
    def test_eliminar_paciente(self, client, sample_paciente_data):
        """Test: DELETE /api/pacientes/{id} - Eliminar (lógico)"""
        # Crear paciente
        response_create = client.post("/api/pacientes", json=sample_paciente_data)
        paciente_id = response_create.json()["id"]
        
        # Eliminar
        response = client.delete(f"/api/pacientes/{paciente_id}")
        
        assert response.status_code == 204
        
        # Verificar que está inactivo
        response_get = client.get(f"/api/pacientes/{paciente_id}")
        assert response_get.json()["activo"] is False
    
    def test_buscar_pacientes_por_nombre(self, client, sample_paciente_data):
        """Test: GET /api/pacientes?buscar=... - Búsqueda"""
        # Crear paciente
        client.post("/api/pacientes", json=sample_paciente_data)
        
        # Buscar
        response = client.get("/api/pacientes?buscar=María")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) >= 1
        assert any("María" in p["nombres"] for p in data)
    
    def test_estadisticas_pacientes(self, client, sample_paciente_data):
        """Test: GET /api/pacientes/estadisticas"""
        # Crear algunos pacientes
        client.post("/api/pacientes", json=sample_paciente_data)
        
        # Obtener estadísticas
        response = client.get("/api/pacientes/estadisticas")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total" in data
        assert "activos" in data
        assert "inactivos" in data
        assert "nuevos_mes" in data
        assert "por_genero" in data
```

---

### Ejemplo: tests/api/test_consultas_api.py
```python
"""
Tests de API para módulo de consultas
"""
import pytest

@pytest.mark.api
class TestConsultasAPI:
    """Tests para endpoints de consultas"""
    
    def test_crear_consulta_con_signos_vitales(
        self, 
        client, 
        create_test_paciente,
        create_test_medico
    ):
        """Test: POST /api/consultas - Con signos vitales"""
        consulta_data = {
            "paciente_id": create_test_paciente.id,
            "medico_id": create_test_medico.id,
            "motivo_consulta": "Control rutinario",
            "presion_sistolica": 120,
            "presion_diastolica": 80,
            "frecuencia_cardiaca": 72,
            "temperatura": 36.5,
            "saturacion_oxigeno": 98,
            "peso": 65.5,
            "talla": 165
        }
        
        response = client.post("/api/consultas", json=consulta_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["motivo_consulta"] == "Control rutinario"
        assert data["presion_sistolica"] == 120
        assert "imc" in data
        assert data["imc"] == pytest.approx(24.05, rel=0.01)
    
    def test_crear_consulta_calcula_imc(
        self,
        client,
        create_test_paciente,
        create_test_medico
    ):
        """Test: POST /api/consultas - Calcula IMC automáticamente"""
        consulta_data = {
            "paciente_id": create_test_paciente.id,
            "medico_id": create_test_medico.id,
            "motivo_consulta": "Control de peso",
            "peso": 70,
            "talla": 170
        }
        
        response = client.post("/api/consultas", json=consulta_data)
        
        assert response.status_code == 201
        data = response.json()
        
        # IMC = 70 / (1.70^2) = 24.22
        assert data["imc"] == pytest.approx(24.22, rel=0.01)
    
    def test_historial_consultas_paciente(
        self,
        client,
        create_test_paciente,
        create_test_medico
    ):
        """Test: GET /api/consultas/paciente/{id}/historial"""
        # Crear varias consultas
        for i in range(3):
            consulta_data = {
                "paciente_id": create_test_paciente.id,
                "medico_id": create_test_medico.id,
                "motivo_consulta": f"Consulta {i+1}"
            }
            client.post("/api/consultas", json=consulta_data)
        
        # Obtener historial
        response = client.get(f"/api/consultas/paciente/{create_test_paciente.id}/historial")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 3
        # Verificar orden descendente por fecha
        assert data[0]["motivo_consulta"] == "Consulta 3"
```

---

### Ejemplo: tests/api/test_hospitalizacion_api.py
```python
"""
Tests de API para módulo de hospitalización
"""
import pytest

@pytest.mark.api
class TestHospitalizacionAPI:
    """Tests para endpoints de hospitalización"""
    
    def test_listar_camas(self, client):
        """Test: GET /api/hospitalizacion/camas"""
        response = client.get("/api/hospitalizacion/camas")
        
        assert response.status_code == 200
        data = response.json()
        
        assert len(data) == 8  # 8 camas
        assert all("numero" in cama for cama in data)
        assert all("estado" in cama for cama in data)
    
    def test_crear_ingreso_hospitalario(
        self,
        client,
        create_test_paciente,
        create_test_medico
    ):
        """Test: POST /api/hospitalizacion/ingresos"""
        ingreso_data = {
            "paciente_id": create_test_paciente.id,
            "medico_responsable_id": create_test_medico.id,
            "cama_id": 1,
            "diagnostico_ingreso": "Neumonía",
            "motivo": "Dificultad respiratoria"
        }
        
        response = client.post("/api/hospitalizacion/ingresos", json=ingreso_data)
        
        assert response.status_code == 201
        data = response.json()
        
        assert data["diagnostico_ingreso"] == "Neumonía"
        assert data["activa"] is True
        assert data["cama_numero"] == 1
    
    def test_cama_cambia_a_ocupada_al_ingresar(
        self,
        client,
        create_test_paciente,
        create_test_medico
    ):
        """Test: Cama cambia de estado al ingresar paciente"""
        # Verificar que cama está disponible
        response_camas = client.get("/api/hospitalizacion/camas")
        cama_1 = next(c for c in response_camas.json() if c["numero"] == 1)
        assert cama_1["estado"] == "Disponible"
        
        # Ingresar paciente
        ingreso_data = {
            "paciente_id": create_test_paciente.id,
            "medico_responsable_id": create_test_medico.id,
            "cama_id": 1,
            "diagnostico_ingreso": "Observación",
            "motivo": "Control"
        }
        client.post("/api/hospitalizacion/ingresos", json=ingreso_data)
        
        # Verificar que cama está ocupada
        response_camas = client.get("/api/hospitalizacion/camas")
        cama_1 = next(c for c in response_camas.json() if c["numero"] == 1)
        assert cama_1["estado"] == "Ocupada"
    
    def test_no_permitir_ingreso_en_cama_ocupada(
        self,
        client,
        create_test_paciente,
        create_test_medico,
        test_db
    ):
        """Test: No permitir ingresar en cama ocupada"""
        # Crear primer ingreso
        ingreso_data = {
            "paciente_id": create_test_paciente.id,
            "medico_responsable_id": create_test_medico.id,
            "cama_id": 1,
            "diagnostico_ingreso": "Observación",
            "motivo": "Control"
        }
        client.post("/api/hospitalizacion/ingresos", json=ingreso_data)
        
        # Crear segundo paciente
        from create_simple_tables import Paciente
        paciente2 = Paciente(
            nombres="Juan",
            apellidos="Pérez",
            fecha_nacimiento="1985-01-01",
            dpi="1111111111111",
            genero="Masculino"
        )
        test_db.add(paciente2)
        test_db.commit()
        test_db.refresh(paciente2)
        
        # Intentar ingresar en misma cama
        ingreso_data2 = {
            "paciente_id": paciente2.id,
            "medico_responsable_id": create_test_medico.id,
            "cama_id": 1,
            "diagnostico_ingreso": "Otro",
            "motivo": "Otro"
        }
        response = client.post("/api/hospitalizacion/ingresos", json=ingreso_data2)
        
        assert response.status_code == 400
        assert "no está disponible" in response.json()["detail"]
    
    def test_dar_egreso(
        self,
        client,
        create_test_paciente,
        create_test_medico
    ):
        """Test: POST /api/hospitalizacion/ingresos/{id}/egreso"""
        # Crear ingreso
        ingreso_data = {
            "paciente_id": create_test_paciente.id,
            "medico_responsable_id": create_test_medico.id,
            "cama_id": 2,
            "diagnostico_ingreso": "Observación",
            "motivo": "Control"
        }
        response_ingreso = client.post("/api/hospitalizacion/ingresos", json=ingreso_data)
        hospitalizacion_id = response_ingreso.json()["id"]
        
        # Dar egreso
        response = client.post(f"/api/hospitalizacion/ingresos/{hospitalizacion_id}/egreso")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "fecha_egreso" in data
        assert "dias_hospitalizacion" in data
        
        # Verificar que cama pasó a limpieza
        response_camas = client.get("/api/hospitalizacion/camas")
        cama_2 = next(c for c in response_camas.json() if c["numero"] == 2)
        assert cama_2["estado"] == "Limpieza"
    
    def test_estadisticas_hospitalizacion(self, client):
        """Test: GET /api/hospitalizacion/estadisticas"""
        response = client.get("/api/hospitalizacion/estadisticas")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "total_camas" in data
        assert "camas_ocupadas" in data
        assert "camas_disponibles" in data
        assert "porcentaje_ocupacion" in data
        assert data["total_camas"] == 8
```

---

## 🧩 Fixtures y Mocks

### Ejemplo: Fixtures Avanzados
```python
# En conftest.py

@pytest.fixture
def create_cama(test_db):
    """Crear cama de prueba"""
    from create_simple_tables import Cama, EstadoCamaEnum
    
    def _create_cama(numero=1, estado=EstadoCamaEnum.disponible):
        cama = Cama(numero=numero, estado=estado, ubicacion=f"Habitación {numero}")
        test_db.add(cama)
        test_db.commit()
        test_db.refresh(cama)
        return cama
    
    return _create_cama

@pytest.fixture
def create_medicamento(test_db):
    """Crear medicamento de prueba"""
    from create_simple_tables import Medicamento
    
    def _create_medicamento(nombre="Paracetamol"):
        medicamento = Medicamento(
            nombre_generico=nombre,
            nombre_comercial="Test Med",
            presentacion="Tableta",
            concentracion="500mg",
            via_administracion="Oral"
        )
        test_db.add(medicamento)
        test_db.commit()
        test_db.refresh(medicamento)
        return medicamento
    
    return _create_medicamento

@pytest.fixture
def mock_twilio():
    """Mock para servicio de Twilio (recordatorios)"""
    from unittest.mock import Mock, patch
    
    with patch('app.services.twilio_service.send_sms') as mock_sms:
        mock_sms.return_value = {"status": "sent", "sid": "SM123456"}
        yield mock_sms
```

---

## 📊 Cobertura de Código

### Ejecutar Tests con Cobertura
```bash
# Todos los tests con cobertura
pytest --cov=app --cov-report=html --cov-report=term-missing

# Solo tests de API
pytest tests/api/ --cov=app/routers --cov-report=html

# Solo tests unitarios
pytest tests/unit/ -m unit

# Generar reporte HTML
pytest --cov=app --cov-report=html
# Ver en: htmlcov/index.html
```

### Interpretar Resultados
```
----------- coverage: platform linux, python 3.11.0 -----------
Name                            Stmts   Miss  Cover   Missing
-------------------------------------------------------------
app/routers/pacientes.py          150     10    93%   45-47, 89
app/routers/citas.py              120      8    93%   34, 67-69
app/routers/consultas.py          100      5    95%   78-80
app/routers/hospitalizacion.py    200     15    92%   145-150
-------------------------------------------------------------
TOTAL                            1500     75    95%
```

**Target**: 80%+ de cobertura en routers principales

---

## ✅ Buenas Prácticas

### 1. Nombres Descriptivos
```python
# ❌ Mal
def test_1():
    pass

# ✅ Bien
def test_crear_paciente_con_datos_validos():
    pass
```

### 2. Arrange-Act-Assert (AAA)
```python
def test_actualizar_telefono_paciente(client):
    # Arrange (Preparar)
    paciente = client.post("/api/pacientes", json=sample_data)
    paciente_id = paciente.json()["id"]
    
    # Act (Ejecutar)
    response = client.put(
        f"/api/pacientes/{paciente_id}",
        json={"telefono": "99998888"}
    )
    
    # Assert (Verificar)
    assert response.status_code == 200
    assert response.json()["telefono"] == "99998888"
```

### 3. Un Test, Una Cosa
```python
# ❌ Mal - Test hace muchas cosas
def test_paciente_completo(client):
    # Crea, actualiza, elimina, estadísticas...
    pass

# ✅ Bien - Tests separados
def test_crear_paciente(client):
    pass

def test_actualizar_paciente(client):
    pass

def test_eliminar_paciente(client):
    pass
```

### 4. Tests Independientes
```python
# ✅ Cada test crea sus propios datos
def test_listar_pacientes(client):
    # Crear datos para este test
    client.post("/api/pacientes", json=data1)
    client.post("/api/pacientes", json=data2)
    
    # Hacer el test
    response = client.get("/api/pacientes")
    assert len(response.json()) >= 2
```

### 5. Usar Fixtures para Datos Comunes
```python
# ✅ Reusar fixtures
def test_consulta(client, create_test_paciente, create_test_medico):
    # Datos ya creados por fixtures
    consulta_data = {
        "paciente_id": create_test_paciente.id,
        "medico_id": create_test_medico.id,
        "motivo_consulta": "Control"
    }
    response = client.post("/api/consultas", json=consulta_data)
    assert response.status_code == 201
```

---

## 🚀 Comandos Útiles
```bash
# Ejecutar todos los tests
pytest

# Ejecutar con verbosidad
pytest -v

# Ejecutar tests específicos
pytest tests/api/test_pacientes_api.py

# Ejecutar un test específico
pytest tests/api/test_pacientes_api.py::TestPacientesAPI::test_crear_paciente_exitoso

# Ejecutar tests por marca
pytest -m unit
pytest -m api
pytest -m "not slow"

# Ejecutar con coverage
pytest --cov=app --cov-report=term-missing

# Ejecutar y parar en el primer fallo
pytest -x

# Ejecutar tests en paralelo (requiere pytest-xdist)
pytest -n 4

# Ver print statements
pytest -s

# Ejecutar tests que fallaron la última vez
pytest --lf

# Ver duración de tests
pytest --durations=10
```

---

## 📈 CI/CD (Futuro)

### GitHub Actions Workflow
```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        cd clinica/backend
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      run: |
        cd clinica/backend
        pytest --cov=app --cov-report=xml
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
      with:
        file: ./clinica/backend/coverage.xml
```

---

## 📝 Checklist de Testing

### Antes de Hacer Commit

- [ ] Todos los tests pasan
- [ ] Cobertura > 80%
- [ ] No hay tests marcados como skip
- [ ] Nombres de tests son descriptivos
- [ ] Tests están en el archivo correcto

### Antes de Deploy

- [ ] Tests de integración pasan
- [ ] Tests de API pasan
- [ ] No hay warnings
- [ ] Coverage report revisado

---

## 🎯 Objetivos de Cobertura por Módulo

| Módulo | Target | Actual | Estado |
|--------|--------|--------|--------|
| Pacientes | 90% | - | ⏳ |
| Citas | 85% | - | ⏳ |
| Consultas | 90% | - | ⏳ |
| Recetas | 85% | - | ⏳ |
| Hospitalización | 90% | - | ⏳ |
| Laboratorios | 85% | - | ⏳ |
| Caja | 85% | - | ⏳ |
| Farmacia | 90% | - | ⏳ |
| Reportes | 80% | - | ⏳ |

---

**Última actualización**: Enero 2025  
**Versión**: 1.0