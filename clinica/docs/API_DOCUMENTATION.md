# 📘 Documentación de API - Sistema Clínico MEDGAR

## Información General

- **Versión**: 2.0.0
- **Base URL**: `http://localhost:8000/api`
- **Documentación Interactiva**: `http://localhost:8000/docs`
- **Total de Endpoints**: 103
- **Total de Módulos**: 16

---

## 🔐 Autenticación

_(Por implementar en Sprint 11)_

Todos los endpoints requerirán autenticación JWT excepto `/health` y endpoints públicos.

---

## 📋 Índice de Módulos

1. [Pacientes](#1-pacientes)
2. [Citas y Agenda](#2-citas-y-agenda)
3. [Lista de Espera](#3-lista-de-espera)
4. [Medicamentos](#4-medicamentos)
5. [Consultas](#5-consultas)
6. [Antecedentes](#6-antecedentes)
7. [Vacunación](#7-vacunación)
8. [Interconsultas](#8-interconsultas)
9. [Recetas](#9-recetas)
10. [Hospitalización](#10-hospitalización)
11. [Notas Médicas](#11-notas-médicas)
12. [Órdenes Médicas](#12-órdenes-médicas)
13. [Laboratorios](#13-laboratorios)
14. [Caja y Facturación](#14-caja-y-facturación)
15. [Farmacia e Inventario](#15-farmacia-e-inventario)
16. [Reportes](#16-reportes)

---

## 1. Pacientes

### 1.1 Crear Paciente
```http
POST /api/pacientes
```

**Request Body:**
```json
{
  "nombres": "María",
  "apellidos": "González López",
  "fecha_nacimiento": "1990-05-15",
  "dpi": "2547896541201",
  "genero": "Femenino",
  "direccion": "4ta calle 5-20 zona 1, Huehuetenango",
  "telefono": "55551234",
  "religion": "Católica",
  "estado_civil": "Casada",
  "tiene_igss": true,
  "contacto_emergencia_nombre": "Juan González",
  "contacto_emergencia_telefono": "55554321"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "nombres": "María",
  "apellidos": "González López",
  "fecha_nacimiento": "1990-05-15",
  "dpi": "2547896541201",
  "genero": "Femenino",
  "edad": 34,
  "activo": true,
  "created_at": "2025-01-15T10:30:00"
}
```

### 1.2 Listar Pacientes
```http
GET /api/pacientes?skip=0&limit=100&buscar=María
```

### 1.3 Obtener Paciente
```http
GET /api/pacientes/{paciente_id}
```

### 1.4 Actualizar Paciente
```http
PUT /api/pacientes/{paciente_id}
```

### 1.5 Eliminar Paciente (Lógico)
```http
DELETE /api/pacientes/{paciente_id}
```

### 1.6 Subir Foto de Perfil
```http
POST /api/pacientes/{paciente_id}/foto
Content-Type: multipart/form-data
```

### 1.7 Subir Archivo
```http
POST /api/pacientes/{paciente_id}/archivos
Content-Type: multipart/form-data

categoria: "Laboratorios" | "Imagenes" | "Recetas" | "EKG" | "Otros"
```

### 1.8 Listar Archivos del Paciente
```http
GET /api/pacientes/{paciente_id}/archivos?categoria=Laboratorios
```

### 1.9 Estadísticas de Pacientes
```http
GET /api/pacientes/estadisticas
```

**Response:**
```json
{
  "total": 150,
  "activos": 148,
  "inactivos": 2,
  "nuevos_mes": 12,
  "por_genero": {
    "Masculino": 65,
    "Femenino": 85
  }
}
```

---

## 2. Citas y Agenda

### 2.1 Crear Cita
```http
POST /api/citas
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_id": 2,
  "fecha_hora": "2025-01-20T10:00:00",
  "tipo_cita": "Primera Consulta",
  "duracion_minutos": 20,
  "motivo": "Control rutinario",
  "notas": "Paciente refiere dolor de cabeza"
}
```

**Tipos de Cita:**
- `Primera Consulta`
- `Reconsulta`
- `Procedimiento`
- `Control Embarazo`
- `Control Niño Sano`
- `Emergencia`

**Estados:**
- `Programada`
- `Confirmada`
- `En Curso`
- `Completada`
- `Cancelada`
- `No Asistió`

### 2.2 Listar Citas
```http
GET /api/citas?medico_id=2&fecha=2025-01-20&estado=Programada
```

### 2.3 Obtener Agenda del Día
```http
GET /api/citas/agenda/{medico_id}/{fecha}
```

**Response:**
```json
{
  "medico_id": 2,
  "medico_nombre": "Dr. Carlos Méndez",
  "fecha": "2025-01-20",
  "total_citas": 8,
  "citas": [
    {
      "id": 1,
      "hora": "10:00",
      "paciente": "María González",
      "tipo": "Primera Consulta",
      "estado": "Confirmada"
    }
  ]
}
```

### 2.4 Obtener Cita
```http
GET /api/citas/{cita_id}
```

### 2.5 Actualizar Cita
```http
PUT /api/citas/{cita_id}
```

### 2.6 Cancelar Cita
```http
DELETE /api/citas/{cita_id}
```

### 2.7 Confirmar Cita
```http
POST /api/citas/{cita_id}/confirmar
```

---

## 3. Lista de Espera

### 3.1 Agregar a Lista de Espera
```http
POST /api/lista-espera
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_id": 2,
  "tipo_cita": "Reconsulta",
  "motivo": "Control de presión arterial",
  "prioridad": 5
}
```

### 3.2 Listar Lista de Espera
```http
GET /api/lista-espera?medico_id=2&activo=true
```

### 3.3 Actualizar Item
```http
PUT /api/lista-espera/{item_id}
```

**Request Body:**
```json
{
  "prioridad": 10,
  "notificado": true
}
```

### 3.4 Remover de Lista
```http
DELETE /api/lista-espera/{item_id}
```

---

## 4. Medicamentos

### 4.1 Crear Medicamento
```http
POST /api/medicamentos
```

**Request Body:**
```json
{
  "nombre_generico": "Paracetamol",
  "nombre_comercial": "Tylenol",
  "presentacion": "Tableta",
  "concentracion": "500 mg",
  "via_administracion": "Oral",
  "contraindicaciones": "Insuficiencia hepática severa",
  "interacciones": "Warfarina, alcohol"
}
```

### 4.2 Listar Medicamentos
```http
GET /api/medicamentos?buscar=paracetamol
```

### 4.3 Obtener Medicamento
```http
GET /api/medicamentos/{medicamento_id}
```

### 4.4 Actualizar Medicamento
```http
PUT /api/medicamentos/{medicamento_id}
```

### 4.5 Eliminar Medicamento
```http
DELETE /api/medicamentos/{medicamento_id}
```

---

## 5. Consultas

### 5.1 Crear Consulta
```http
POST /api/consultas
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_id": 2,
  "cita_id": 5,
  "motivo_consulta": "Dolor de cabeza intenso",
  "historia_enfermedad_actual": "Paciente refiere cefalea de 3 días de evolución...",
  "presion_sistolica": 120,
  "presion_diastolica": 80,
  "frecuencia_cardiaca": 72,
  "temperatura": 36.5,
  "saturacion_oxigeno": 98,
  "frecuencia_respiratoria": 16,
  "peso": 65.5,
  "talla": 165,
  "examen_fisico": "Consciente, orientada, normocéfala...",
  "diagnostico": "Cefalea tensional",
  "plan_tratamiento": "Analgésicos, relajación"
}
```

**Response incluye IMC calculado:**
```json
{
  "id": 1,
  "imc": 24.05,
  ...
}
```

### 5.2 Listar Consultas
```http
GET /api/consultas?paciente_id=1&medico_id=2
```

### 5.3 Obtener Consulta
```http
GET /api/consultas/{consulta_id}
```

### 5.4 Actualizar Consulta
```http
PUT /api/consultas/{consulta_id}
```

### 5.5 Obtener Historial del Paciente
```http
GET /api/consultas/paciente/{paciente_id}/historial
```

---

## 6. Antecedentes

### 6.1 Crear Antecedente
```http
POST /api/antecedentes
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "tipo": "Medicos",
  "descripcion": "Hipertensión arterial diagnosticada en 2020"
}
```

**Tipos de Antecedente:**
- `Medicos`
- `Quirurgicos`
- `Traumaticos`
- `Alergicos`
- `Ginecologicos`
- `Obstetricos`

### 6.2 Listar Antecedentes del Paciente
```http
GET /api/antecedentes/paciente/{paciente_id}?tipo=Medicos&activo=true
```

### 6.3 Obtener Antecedente
```http
GET /api/antecedentes/{antecedente_id}
```

### 6.4 Actualizar Antecedente
```http
PUT /api/antecedentes/{antecedente_id}
```

### 6.5 Desactivar Antecedente
```http
DELETE /api/antecedentes/{antecedente_id}
```

---

## 7. Vacunación

### 7.1 Registrar Vacuna
```http
POST /api/vacunas
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "tipo_vacuna": "BCG",
  "dosis": "Dosis única",
  "fecha_aplicacion": "2024-03-15",
  "lote": "LOT123456",
  "lugar_aplicacion": "Brazo derecho",
  "medico_id": 2,
  "observaciones": "Sin reacciones adversas"
}
```

**Tipos de Vacuna:**
- `BCG`, `Hepatitis B`, `Pentavalente`, `Rotavirus`, `Neumococo`
- `Influenza`, `SRP`, `Varicela`, `Hepatitis A`, `DPT`, `OPV`, `COVID-19`

### 7.2 Listar Vacunas del Paciente
```http
GET /api/vacunas/paciente/{paciente_id}?tipo_vacuna=BCG
```

### 7.3 Obtener Esquema de Vacunación
```http
GET /api/vacunas/paciente/{paciente_id}/esquema
```

**Response:**
```json
{
  "paciente_id": 1,
  "edad_meses": 6,
  "vacunas_aplicadas": [...],
  "vacunas_pendientes": [
    {
      "tipo_vacuna": "Pentavalente",
      "dosis": "3ra dosis",
      "edad_recomendada_meses": 6,
      "atrasada": false
    }
  ]
}
```

### 7.4 Obtener Vacuna
```http
GET /api/vacunas/{vacuna_id}
```

---

## 8. Interconsultas

### 8.1 Crear Interconsulta
```http
POST /api/interconsultas
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "consulta_id": 5,
  "medico_solicitante_id": 2,
  "especialidad_solicitada": "Cardiología",
  "motivo": "Evaluación de soplo cardíaco"
}
```

**Estados:**
- `Solicitada`
- `En Proceso`
- `Completada`
- `Cancelada`

### 8.2 Listar Interconsultas
```http
GET /api/interconsultas?paciente_id=1&estado=Solicitada
```

### 8.3 Obtener Interconsulta
```http
GET /api/interconsultas/{interconsulta_id}
```

### 8.4 Responder Interconsulta
```http
PUT /api/interconsultas/{interconsulta_id}
```

**Request Body:**
```json
{
  "medico_consultor_id": 3,
  "hallazgos": "Soplo sistólico grado II/VI...",
  "recomendaciones": "Ecocardiograma, control en 3 meses",
  "estado": "Completada"
}
```

---

## 9. Recetas

### 9.1 Crear Receta
```http
POST /api/recetas
```

**Request Body:**
```json
{
  "consulta_id": 5,
  "paciente_id": 1,
  "medico_id": 2,
  "indicaciones_generales": "Tomar con alimentos",
  "medicamentos": [
    {
      "medicamento_id": 1,
      "medicamento_texto": "Paracetamol",
      "presentacion": "Tableta 500mg",
      "dosis": "1 tableta",
      "frecuencia": "Cada 8 horas",
      "duracion": "5 días",
      "via_administracion": "Oral",
      "indicaciones": "Si hay dolor o fiebre"
    }
  ]
}
```

### 9.2 Listar Recetas
```http
GET /api/recetas?paciente_id=1&medico_id=2
```

### 9.3 Obtener Receta
```http
GET /api/recetas/{receta_id}
```

### 9.4 Obtener Historial de Recetas
```http
GET /api/recetas/paciente/{paciente_id}/historial
```

---

## 10. Hospitalización

### 10.1 Listar Camas
```http
GET /api/hospitalizacion/camas
```

**Response:**
```json
[
  {
    "id": 1,
    "numero": 1,
    "estado": "Ocupada",
    "ubicacion": "Habitación 1",
    "paciente_actual": "María González"
  }
]
```

**Estados de Cama:**
- `Disponible`
- `Ocupada`
- `Limpieza`
- `Mantenimiento`

### 10.2 Listar Camas Disponibles
```http
GET /api/hospitalizacion/camas/disponibles
```

### 10.3 Cambiar Estado de Cama
```http
PUT /api/hospitalizacion/camas/{cama_id}/estado
```

**Request Body:**
```json
{
  "nuevo_estado": "Limpieza"
}
```

### 10.4 Crear Ingreso Hospitalario
```http
POST /api/hospitalizacion/ingresos
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_responsable_id": 2,
  "cama_id": 3,
  "diagnostico_ingreso": "Neumonía adquirida en comunidad",
  "motivo": "Dificultad respiratoria, fiebre"
}
```

### 10.5 Listar Hospitalizaciones
```http
GET /api/hospitalizacion/ingresos?activa=true&paciente_id=1
```

### 10.6 Listar Hospitalizaciones Activas
```http
GET /api/hospitalizacion/ingresos/activos
```

### 10.7 Obtener Hospitalización
```http
GET /api/hospitalizacion/ingresos/{hospitalizacion_id}
```

### 10.8 Actualizar Hospitalización
```http
PUT /api/hospitalizacion/ingresos/{hospitalizacion_id}
```

### 10.9 Dar Egreso
```http
POST /api/hospitalizacion/ingresos/{hospitalizacion_id}/egreso
```

### 10.10 Estadísticas de Hospitalización
```http
GET /api/hospitalizacion/estadisticas
```

**Response:**
```json
{
  "total_camas": 8,
  "camas_ocupadas": 5,
  "camas_disponibles": 2,
  "camas_limpieza": 1,
  "camas_mantenimiento": 0,
  "porcentaje_ocupacion": 62.5,
  "hospitalizaciones_activas": 5
}
```

---

## 11. Notas Médicas

### 11.1 Crear Nota Médica
```http
POST /api/notas-medicas
```

**Request Body (Nota de Evolución):**
```json
{
  "hospitalizacion_id": 1,
  "medico_id": 2,
  "tipo": "Evolución",
  "contenido": "Día 3 de hospitalización. Paciente afebril, saturando 96%..."
}
```

**Request Body (Nota Operatoria):**
```json
{
  "hospitalizacion_id": 1,
  "medico_id": 2,
  "tipo": "Operatoria",
  "contenido": "Bajo anestesia general...",
  "cirugia_realizada": "Colecistectomía laparoscópica",
  "cirujano_id": 2,
  "anestesiologo": "Dr. Pedro Ramírez",
  "tipo_anestesia": "General balanceada",
  "diagnostico_preoperatorio": "Colelitiasis sintomática",
  "diagnostico_postoperatorio": "Colelitiasis",
  "hallazgos": "Vesícula distendida con múltiples cálculos",
  "complicaciones": "Ninguna",
  "sangrado_estimado": "50 ml",
  "especimenes_patologia": "Vesícula biliar",
  "pronostico": "Bueno"
}
```

**Tipos de Nota:**
- `Ingreso`
- `Evolución`
- `Procedimiento`
- `Operatoria`
- `Egreso`

### 11.2 Listar Notas de Hospitalización
```http
GET /api/notas-medicas/hospitalizacion/{hospitalizacion_id}?tipo=Evolución
```

### 11.3 Obtener Nota
```http
GET /api/notas-medicas/{nota_id}
```

---

## 12. Órdenes Médicas

### 12.1 Crear Orden Médica
```http
POST /api/ordenes-medicas
```

**Request Body (Medicamento):**
```json
{
  "hospitalizacion_id": 1,
  "medico_id": 2,
  "tipo": "Medicamento",
  "descripcion": "Ampicilina 1g IV cada 6 horas",
  "medicamento_id": 5,
  "dosis": "1g",
  "frecuencia": "Cada 6 horas",
  "via": "Intravenosa",
  "duracion": "7 días"
}
```

**Request Body (Dieta):**
```json
{
  "hospitalizacion_id": 1,
  "medico_id": 2,
  "tipo": "Dieta",
  "descripcion": "Dieta blanda, sin irritantes"
}
```

**Tipos de Orden:**
- `Medicamento`
- `Dieta`
- `Signos Vitales`
- `Laboratorio`
- `Estudio de Imagen`
- `Interconsulta`
- `Cuidados de Enfermería`
- `Otro`

**Estados:**
- `Activa`
- `Suspendida`
- `Completada`

### 12.2 Listar Órdenes de Hospitalización
```http
GET /api/ordenes-medicas/hospitalizacion/{hospitalizacion_id}?estado=Activa
```

### 12.3 Actualizar Estado de Orden
```http
PUT /api/ordenes-medicas/{orden_id}
```

**Request Body:**
```json
{
  "estado": "Completada"
}
```

---

## 13. Laboratorios

### 13.1 Crear Tipo de Estudio
```http
POST /api/laboratorios/tipos-estudio
```

**Request Body:**
```json
{
  "nombre": "Hemograma Completo",
  "categoria": "Hematología",
  "descripcion": "Conteo completo de células sanguíneas"
}
```

**Categorías:**
- `Hematología`, `Química Sanguínea`, `Función Hepática`, `Función Renal`
- `Perfil Lipídico`, `Pruebas Tiroideas`, `Diabetes`, `Marcadores Tumorales`
- `Inmunología`, `Grupo Sanguíneo`, `Orina y Heces`, `Microbiología`, `Estudios de Imagen`

### 13.2 Listar Tipos de Estudio
```http
GET /api/laboratorios/tipos-estudio?categoria=Hematología&activo=true
```

### 13.3 Crear Resultado de Laboratorio
```http
POST /api/laboratorios/resultados
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "consulta_id": 5,
  "tipo_estudio_id": 1,
  "fecha_toma": "2025-01-15T08:00:00",
  "resultado": "{\"hemoglobina\": 14.5, \"leucocitos\": 7500, \"plaquetas\": 250000}",
  "valor_minimo": "12",
  "valor_maximo": "16",
  "unidad": "g/dL",
  "valor_critico": false,
  "laboratorio_externo": "Lab Central",
  "observaciones": "Valores dentro de parámetros normales"
}
```

### 13.4 Listar Resultados del Paciente
```http
GET /api/laboratorios/resultados/paciente/{paciente_id}?tipo_estudio_id=1
```

### 13.5 Obtener Resultado
```http
GET /api/laboratorios/resultados/{resultado_id}
```

### 13.6 Listar Valores Críticos
```http
GET /api/laboratorios/resultados/criticos/paciente/{paciente_id}
```

---

## 14. Caja y Facturación

### 14.1 Abrir Caja
```http
POST /api/caja/apertura
```

**Request Body:**
```json
{
  "usuario_id": 1,
  "monto_inicial": 500.00
}
```

### 14.2 Obtener Caja Actual
```http
GET /api/caja/actual
```

### 14.3 Cerrar Caja
```http
POST /api/caja/cierre/{caja_id}
```

**Request Body:**
```json
{
  "monto_final": 1250.00
}
```

**Response:**
```json
{
  "id": 1,
  "fecha_cierre": "2025-01-15T18:00:00",
  "monto_inicial": 500.00,
  "monto_final": 1250.00,
  "total_ingresos": 800.00,
  "total_egresos": 50.00,
  "diferencia": 0.00,
  "cerrada": true
}
```

### 14.4 Listar Historial de Cajas
```http
GET /api/caja/historial?fecha_desde=2025-01-01&fecha_hasta=2025-01-31
```

### 14.5 Registrar Movimiento
```http
POST /api/caja/movimientos
```

**Request Body (Ingreso):**
```json
{
  "caja_id": 1,
  "tipo_movimiento": "Ingreso",
  "tipo_ingreso": "Consulta Médica",
  "paciente_id": 1,
  "concepto": "Consulta medicina general",
  "monto": 150.00,
  "forma_pago": "Efectivo",
  "usuario_id": 1
}
```

**Request Body (Egreso):**
```json
{
  "caja_id": 1,
  "tipo_movimiento": "Egreso",
  "tipo_egreso": "Compra Medicamentos",
  "proveedor": "Farmacia San José",
  "concepto": "Compra de antibióticos",
  "monto": 50.00,
  "forma_pago": "Efectivo",
  "numero_documento": "F-001234",
  "usuario_id": 1
}
```

### 14.6 Listar Movimientos de Caja
```http
GET /api/caja/movimientos/caja/{caja_id}
```

### 14.7 Crear Cuenta por Cobrar
```http
POST /api/caja/cuentas-por-cobrar
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "concepto": "Cirugía laparoscópica",
  "monto_total": 5000.00,
  "fecha_emision": "2025-01-15",
  "fecha_vencimiento": "2025-02-15",
  "observaciones": "Pago en 3 cuotas"
}
```

### 14.8 Listar Cuentas por Cobrar
```http
GET /api/caja/cuentas-por-cobrar?pagado=false&vencidas=true
```

### 14.9 Abonar a Cuenta
```http
PUT /api/caja/cuentas-por-cobrar/{cuenta_id}/abonar
```

**Request Body:**
```json
{
  "monto_pagado": 1000.00
}
```

### 14.10 Crear Cotización
```http
POST /api/caja/cotizaciones
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "medico_id": 2,
  "vigencia_dias": 30,
  "servicios": "[{\"servicio\": \"Cirugía\", \"precio\": 3000}, {\"servicio\": \"Consulta pre-op\", \"precio\": 150}]",
  "total": 3150.00,
  "condiciones": "50% anticipo, saldo al momento de la cirugía"
}
```

### 14.11 Listar Cotizaciones
```http
GET /api/caja/cotizaciones?paciente_id=1&aceptada=false
```

### 14.12 Aceptar Cotización
```http
PUT /api/caja/cotizaciones/{cotizacion_id}/aceptar
```

---

## 15. Farmacia e Inventario

### 15.1 Crear Proveedor
```http
POST /api/farmacia/proveedores
```

**Request Body:**
```json
{
  "nombre": "Distribuidora Médica S.A.",
  "nit": "1234567-8",
  "direccion": "5ta avenida 10-20 zona 9",
  "telefono": "23456789",
  "email": "ventas@distmedica.com",
  "contacto": "Juan Pérez"
}
```

### 15.2 Listar Proveedores
```http
GET /api/farmacia/proveedores?activo=true
```

### 15.3 Crear Producto
```http
POST /api/farmacia/productos
```

**Request Body:**
```json
{
  "medicamento_id": 1,
  "codigo_interno": "MED-001",
  "nombre": "Paracetamol 500mg",
  "tipo": "Medicamento",
  "presentacion": "Tableta",
  "lote": "LOT123456",
  "fecha_vencimiento": "2026-12-31",
  "proveedor_id": 1,
  "stock_actual": 100,
  "stock_minimo": 20,
  "precio_compra": 0.50,
  "precio_venta": 1.00,
  "ubicacion": "Estante A-1"
}
```

### 15.4 Listar Productos
```http
GET /api/farmacia/productos?buscar=paracetamol&stock_bajo=true
```

### 15.5 Obtener Producto
```http
GET /api/farmacia/productos/{producto_id}
```

### 15.6 Actualizar Producto
```http
PUT /api/farmacia/productos/{producto_id}
```

### 15.7 Registrar Movimiento de Inventario
```http
POST /api/farmacia/movimientos
```

**Request Body:**
```json
{
  "producto_id": 1,
  "tipo": "Entrada",
  "cantidad": 50,
  "motivo": "Compra a proveedor",
  "usuario_id": 1
}
```

**Tipos:**
- `Entrada`
- `Salida`
- `Ajuste`

### 15.8 Listar Movimientos del Producto
```http
GET /api/farmacia/movimientos/producto/{producto_id}
```

### 15.9 Crear Compra
```http
POST /api/farmacia/compras
```

**Request Body:**
```json
{
  "proveedor_id": 1,
  "fecha_compra": "2025-01-15",
  "numero_factura": "F-001234",
  "usuario_id": 1,
  "observaciones": "Compra mensual",
  "productos": [
    {
      "producto_id": 1,
      "cantidad": 100,
      "precio_unitario": 0.50
    },
    {
      "producto_id": 2,
      "cantidad": 50,
      "precio_unitario": 1.20
    }
  ]
}
```

### 15.10 Listar Compras
```http
GET /api/farmacia/compras?proveedor_id=1&fecha_desde=2025-01-01
```

### 15.11 Crear Venta
```http
POST /api/farmacia/ventas
```

**Request Body:**
```json
{
  "paciente_id": 1,
  "receta_id": 5,
  "descuento": 5.00,
  "usuario_id": 1,
  "productos": [
    {
      "producto_id": 1,
      "cantidad": 10,
      "precio_unitario": 1.00
    }
  ]
}
```

### 15.12 Listar Ventas
```http
GET /api/farmacia/ventas?paciente_id=1&fecha_desde=2025-01-01
```

### 15.13 Estadísticas de Farmacia
```http
GET /api/farmacia/estadisticas
```

**Response:**
```json
{
  "total_productos": 150,
  "productos_stock_bajo": 12,
  "productos_por_vencer": 5,
  "valor_inventario": 25450.50
}
```

---

## 16. Reportes

### 16.1 Dashboard Ejecutivo
```http
GET /api/reportes/dashboard
```

**Response:**
```json
{
  "total_pacientes": 150,
  "pacientes_nuevos_mes": 12,
  "citas_hoy": 8,
  "citas_semana": 45,
  "citas_pendientes": 15,
  "consultas_hoy": 6,
  "consultas_mes": 78,
  "camas_ocupadas": 5,
  "total_camas": 8,
  "porcentaje_ocupacion": 62.5,
  "recetas_mes": 65
}
```

### 16.2 Reporte de Pacientes
```http
GET /api/reportes/pacientes
```

**Response:**
```json
{
  "total": 150,
  "activos": 148,
  "inactivos": 2,
  "por_genero": {
    "Masculino": 65,
    "Femenino": 85
  },
  "nuevos_por_mes": {
    "Enero 2025": 12,
    "Diciembre 2024": 8
  }
}
```

### 16.3 Reporte de Citas
```http
GET /api/reportes/citas?fecha_desde=2025-01-01&fecha_hasta=2025-01-31
```

**Response:**
```json
{
  "total_mes": 120,
  "por_tipo": {
    "Primera Consulta": 45,
    "Reconsulta": 60,
    "Procedimiento": 15
  },
  "por_estado": {
    "Completada": 100,
    "No Asistió": 10,
    "Cancelada": 10
  },
  "por_medico": [
    {
      "medico_id": 2,
      "nombre": "Dr. Carlos Méndez",
      "total_citas": 75
    }
  ],
  "tasa_asistencia": 83.33
}
```

### 16.4 Reporte de Consultas
```http
GET /api/reportes/consultas?fecha_desde=2025-01-01&fecha_hasta=2025-01-31
```

### 16.5 Reporte de Hospitalización
```http
GET /api/reportes/hospitalizacion?fecha_desde=2025-01-01&fecha_hasta=2025-01-31
```

**Response:**
```json
{
  "total_mes": 15,
  "promedio_estancia": 4.5,
  "ocupacion_promedio": 65.5,
  "ingresos_por_dia": {
    "2025-01-15": 2,
    "2025-01-16": 1
  }
}
```

---

## 📊 Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Eliminación exitosa
- `400 Bad Request` - Error en los datos enviados
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 🔄 Paginación

Los endpoints de listado soportan paginación:
```http
GET /api/pacientes?skip=0&limit=100
```

- `skip`: Número de registros a saltar (default: 0)
- `limit`: Máximo de registros a retornar (default: 100)

---

## 🔍 Filtros y Búsquedas

La mayoría de endpoints de listado soportan filtros específicos. Ver cada sección para detalles.

---

## 📝 Notas Importantes

1. **Fechas**: Formato ISO 8601 (`YYYY-MM-DDTHH:MM:SS`)
2. **IDs**: Todos los IDs son enteros
3. **Booleanos**: `true` o `false`
4. **Archivos**: Usar `multipart/form-data` para uploads
5. **JSON**: Algunos campos almacenan JSON como string

---

## 🚀 Próximas Implementaciones

- Autenticación JWT
- Generación de PDF para recetas
- Integración FEL (Facturación Electrónica)
- Gráficas OMS para pediatría
- Sistema de notificaciones en tiempo real
- Telemedicina

---

**Última actualización**: Enero 2025  
**Versión**: 2.0.0