# 🗄️ Documentación de Base de Datos - Sistema Clínico MEDGAR

## Información General

- **Motor**: PostgreSQL 15
- **ORM**: SQLAlchemy 2.0
- **Total de Tablas**: 31
- **Encoding**: UTF-8
- **Timezone**: UTC

---

## 📊 Diagrama de Entidades (Resumen)
```
┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO PACIENTES                             │
├─────────────────────────────────────────────────────────────────┤
│ • pacientes                                                     │
│ • archivos_paciente                                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO CONSULTAS                             │
├─────────────────────────────────────────────────────────────────┤
│ • consultas                                                     │
│ • antecedentes                                                  │
│ • vacunas                                                       │
│ • interconsultas                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO CITAS                                 │
├─────────────────────────────────────────────────────────────────┤
│ • citas                                                         │
│ • lista_espera                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO RECETAS                               │
├─────────────────────────────────────────────────────────────────┤
│ • medicamentos                                                  │
│ • recetas                                                       │
│ • receta_detalle                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO HOSPITALIZACIÓN                       │
├─────────────────────────────────────────────────────────────────┤
│ • hospitalizaciones                                             │
│ • camas                                                         │
│ • notas_medicas                                                 │
│ • ordenes_medicas                                               │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO LABORATORIOS                          │
├─────────────────────────────────────────────────────────────────┤
│ • tipos_estudio                                                 │
│ • resultados_laboratorio                                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO CAJA                                  │
├─────────────────────────────────────────────────────────────────┤
│ • caja                                                          │
│ • movimientos_caja                                              │
│ • cuentas_por_cobrar                                            │
│ • cotizaciones                                                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO FARMACIA                              │
├─────────────────────────────────────────────────────────────────┤
│ • proveedores                                                   │
│ • productos_farmacia                                            │
│ • movimientos_inventario                                        │
│ • compras_farmacia                                              │
│ • detalle_compra                                                │
│ • ventas_farmacia                                               │
│ • detalle_venta                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    MÓDULO USUARIOS                              │
├─────────────────────────────────────────────────────────────────┤
│ • usuarios                                                      │
│ • roles                                                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📋 Tablas Detalladas

### 1. TABLA: pacientes

**Descripción**: Información completa de pacientes de la clínica

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único del paciente |
| nombres | VARCHAR(100) | NOT NULL | Nombres del paciente |
| apellidos | VARCHAR(100) | NOT NULL | Apellidos del paciente |
| fecha_nacimiento | DATE | NOT NULL | Fecha de nacimiento |
| dpi | VARCHAR(20) | UNIQUE | DPI (Documento Personal de Identificación) |
| genero | ENUM | NOT NULL | Masculino, Femenino, Otro |
| direccion | TEXT | | Dirección completa |
| telefono | VARCHAR(15) | | Teléfono principal |
| religion | VARCHAR(50) | | Religión |
| estado_civil | VARCHAR(20) | | Soltero, Casado, Divorciado, Viudo |
| tiene_igss | BOOLEAN | DEFAULT FALSE | Indica si tiene seguro IGSS |
| contacto_emergencia_nombre | VARCHAR(100) | | Nombre del contacto de emergencia |
| contacto_emergencia_telefono | VARCHAR(15) | | Teléfono de emergencia |
| foto_url | VARCHAR(500) | | Ruta de la foto de perfil |
| activo | BOOLEAN | DEFAULT TRUE | Estado del registro |
| created_at | TIMESTAMP | AUTO | Fecha de creación |

**Índices**:
- `idx_pacientes_dpi` en `dpi`
- `idx_pacientes_nombres` en `nombres`
- `idx_pacientes_apellidos` en `apellidos`

**Relaciones**:
- Uno a muchos con `consultas`
- Uno a muchos con `citas`
- Uno a muchos con `archivos_paciente`
- Uno a muchos con `antecedentes`
- Uno a muchos con `vacunas`
- Uno a muchos con `hospitalizaciones`

---

### 2. TABLA: archivos_paciente

**Descripción**: Archivos multimedia asociados a pacientes

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único del archivo |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| categoria | ENUM | NOT NULL | Laboratorios, Imagenes, Recetas, EKG, Otros |
| nombre_archivo | VARCHAR(300) | NOT NULL | Nombre del archivo |
| ruta_archivo | VARCHAR(500) | NOT NULL | Ruta en el sistema de archivos |
| tipo_mime | VARCHAR(100) | | Tipo MIME del archivo |
| tamano_bytes | INTEGER | | Tamaño en bytes |
| created_at | TIMESTAMP | AUTO | Fecha de carga |

**Índices**:
- `idx_archivos_paciente_id` en `paciente_id`
- `idx_archivos_categoria` en `categoria`

---

### 3. TABLA: usuarios

**Descripción**: Usuarios del sistema (médicos, enfermeras, recepcionistas, admin)

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único del usuario |
| nombres | VARCHAR(100) | NOT NULL | Nombres |
| apellidos | VARCHAR(100) | NOT NULL | Apellidos |
| email | VARCHAR(100) | UNIQUE, NOT NULL | Email |
| password_hash | VARCHAR(200) | NOT NULL | Contraseña hasheada |
| rol_id | INTEGER | FK, NOT NULL | Referencia a roles |
| especialidad | VARCHAR(100) | | Especialidad médica |
| registro_medico | VARCHAR(50) | | Número de registro |
| activo | BOOLEAN | DEFAULT TRUE | Estado del usuario |
| created_at | TIMESTAMP | AUTO | Fecha de creación |

---

### 4. TABLA: citas

**Descripción**: Agenda de citas médicas

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único de la cita |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| medico_id | INTEGER | FK, NOT NULL | Referencia a usuarios (médico) |
| fecha_hora | TIMESTAMP | NOT NULL | Fecha y hora de la cita |
| tipo_cita | ENUM | NOT NULL | Primera Consulta, Reconsulta, Procedimiento, etc. |
| duracion_minutos | INTEGER | DEFAULT 20 | Duración en minutos |
| estado | ENUM | DEFAULT 'Programada' | Programada, Confirmada, Completada, etc. |
| motivo | TEXT | | Motivo de la cita |
| notas | TEXT | | Notas adicionales |
| created_at | TIMESTAMP | AUTO | Fecha de creación |

**Índices**:
- `idx_citas_fecha` en `fecha_hora`
- `idx_citas_medico` en `medico_id`
- `idx_citas_paciente` en `paciente_id`

---

### 5. TABLA: consultas

**Descripción**: Registro de consultas médicas con signos vitales

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único de la consulta |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| medico_id | INTEGER | FK, NOT NULL | Referencia a usuarios (médico) |
| cita_id | INTEGER | FK | Referencia a citas |
| fecha_hora | TIMESTAMP | AUTO | Fecha y hora de la consulta |
| motivo_consulta | TEXT | NOT NULL | Motivo de consulta |
| historia_enfermedad_actual | TEXT | | Historia de enfermedad actual |
| presion_sistolica | INTEGER | | Presión sistólica (mmHg) |
| presion_diastolica | INTEGER | | Presión diastólica (mmHg) |
| frecuencia_cardiaca | INTEGER | | Frecuencia cardíaca (lpm) |
| temperatura | FLOAT | | Temperatura (°C) |
| saturacion_oxigeno | INTEGER | | Saturación de oxígeno (%) |
| frecuencia_respiratoria | INTEGER | | Frecuencia respiratoria (rpm) |
| peso | FLOAT | | Peso (kg) |
| talla | FLOAT | | Talla (cm) |
| examen_fisico | TEXT | | Examen físico |
| diagnostico | TEXT | | Diagnóstico |
| plan_tratamiento | TEXT | | Plan de tratamiento |
| observaciones | TEXT | | Observaciones |
| created_at | TIMESTAMP | AUTO | Fecha de creación |

**Índices**:
- `idx_consultas_paciente` en `paciente_id`
- `idx_consultas_medico` en `medico_id`
- `idx_consultas_fecha` en `fecha_hora`

---

### 6. TABLA: antecedentes

**Descripción**: Antecedentes médicos del paciente

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| tipo | ENUM | NOT NULL | Medicos, Quirurgicos, Traumaticos, Alergicos, etc. |
| descripcion | TEXT | NOT NULL | Descripción del antecedente |
| activo | BOOLEAN | DEFAULT TRUE | Estado activo/inactivo |

**Índices**:
- `idx_antecedentes_paciente` en `paciente_id`

---

### 7. TABLA: vacunas

**Descripción**: Registro de vacunas aplicadas

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| tipo_vacuna | ENUM | NOT NULL | BCG, Hepatitis B, Pentavalente, etc. |
| dosis | VARCHAR(50) | NOT NULL | 1ra dosis, 2da dosis, Refuerzo |
| fecha_aplicacion | DATE | NOT NULL | Fecha de aplicación |
| lote | VARCHAR(100) | | Lote del medicamento |
| lugar_aplicacion | VARCHAR(100) | | Lugar anatómico |
| medico_id | INTEGER | FK | Médico que aplicó |
| observaciones | TEXT | | Observaciones |
| created_at | TIMESTAMP | AUTO | Fecha de registro |

---

### 8. TABLA: lista_espera

**Descripción**: Lista de espera para citas canceladas

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| medico_id | INTEGER | FK, NOT NULL | Referencia a usuarios |
| tipo_cita | ENUM | NOT NULL | Tipo de cita solicitada |
| motivo | TEXT | | Motivo de la solicitud |
| prioridad | INTEGER | DEFAULT 0 | Mayor número = mayor prioridad |
| fecha_solicitud | TIMESTAMP | AUTO | Fecha de solicitud |
| notificado | BOOLEAN | DEFAULT FALSE | Si fue notificado |
| activo | BOOLEAN | DEFAULT TRUE | Estado activo/inactivo |

---

### 9. TABLA: interconsultas

**Descripción**: Solicitudes de interconsulta a especialistas

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| consulta_id | INTEGER | FK | Referencia a consultas |
| hospitalizacion_id | INTEGER | FK | Referencia a hospitalizaciones |
| medico_solicitante_id | INTEGER | FK, NOT NULL | Médico que solicita |
| especialidad_solicitada | VARCHAR(100) | NOT NULL | Especialidad requerida |
| medico_consultor_id | INTEGER | FK | Médico consultor |
| motivo | TEXT | NOT NULL | Motivo de interconsulta |
| hallazgos | TEXT | | Hallazgos del consultor |
| recomendaciones | TEXT | | Recomendaciones |
| estado | ENUM | DEFAULT 'Solicitada' | Solicitada, En Proceso, Completada, Cancelada |
| fecha_solicitud | TIMESTAMP | AUTO | Fecha de solicitud |
| fecha_respuesta | TIMESTAMP | | Fecha de respuesta |

---

### 10. TABLA: medicamentos

**Descripción**: Catálogo de medicamentos

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| nombre_generico | VARCHAR(200) | NOT NULL | Nombre genérico |
| nombre_comercial | VARCHAR(200) | | Nombre comercial |
| presentacion | VARCHAR(100) | | Tableta, Cápsula, Jarabe, etc. |
| concentracion | VARCHAR(50) | | Concentración |
| via_administracion | VARCHAR(50) | | Oral, Parenteral, Tópica, etc. |
| contraindicaciones | TEXT | | Contraindicaciones |
| interacciones | TEXT | | Interacciones medicamentosas |
| activo | BOOLEAN | DEFAULT TRUE | Estado activo/inactivo |

**Índices**:
- `idx_medicamentos_nombre_generico` en `nombre_generico`

---

### 11. TABLA: recetas

**Descripción**: Recetas médicas

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| consulta_id | INTEGER | FK, NOT NULL | Referencia a consultas |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| medico_id | INTEGER | FK, NOT NULL | Referencia a usuarios |
| indicaciones_generales | TEXT | | Indicaciones generales |
| created_at | TIMESTAMP | AUTO | Fecha de creación |

---

### 12. TABLA: receta_detalle

**Descripción**: Detalle de medicamentos en receta

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| receta_id | INTEGER | FK, NOT NULL | Referencia a recetas |
| medicamento_id | INTEGER | FK | Referencia a medicamentos |
| medicamento_texto | VARCHAR(300) | NOT NULL | Texto del medicamento |
| presentacion | VARCHAR(100) | | Presentación |
| dosis | VARCHAR(100) | NOT NULL | Dosis |
| frecuencia | VARCHAR(100) | NOT NULL | Frecuencia |
| duracion | VARCHAR(100) | NOT NULL | Duración |
| via_administracion | VARCHAR(50) | | Vía de administración |
| indicaciones | TEXT | | Indicaciones específicas |

---

### 13. TABLA: camas

**Descripción**: Camas de hospitalización (8 camas)

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| numero | INTEGER | NOT NULL, UNIQUE | Número de cama (1-8) |
| estado | ENUM | NOT NULL | Disponible, Ocupada, Limpieza, Mantenimiento |
| ubicacion | VARCHAR(100) | | Ubicación física |

---

### 14. TABLA: hospitalizaciones

**Descripción**: Registros de hospitalización

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| medico_responsable_id | INTEGER | FK, NOT NULL | Médico responsable |
| cama_id | INTEGER | FK, NOT NULL | Cama asignada |
| fecha_ingreso | TIMESTAMP | AUTO | Fecha de ingreso |
| fecha_egreso | TIMESTAMP | | Fecha de egreso |
| diagnostico_ingreso | TEXT | NOT NULL | Diagnóstico de ingreso |
| motivo | TEXT | NOT NULL | Motivo de hospitalización |
| activa | BOOLEAN | DEFAULT TRUE | Hospitalización activa |

**Índices**:
- `idx_hospitalizaciones_paciente` en `paciente_id`
- `idx_hospitalizaciones_activa` en `activa`

---

### 15. TABLA: notas_medicas

**Descripción**: Notas médicas durante hospitalización

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| hospitalizacion_id | INTEGER | FK, NOT NULL | Referencia a hospitalizaciones |
| medico_id | INTEGER | FK, NOT NULL | Médico que escribe |
| tipo | ENUM | NOT NULL | Ingreso, Evolución, Procedimiento, Operatoria, Egreso |
| fecha_hora | TIMESTAMP | AUTO | Fecha y hora |
| contenido | TEXT | NOT NULL | Contenido de la nota |
| cirugia_realizada | VARCHAR(300) | | Para nota operatoria |
| cirujano_id | INTEGER | FK | Cirujano |
| anestesiologo | VARCHAR(200) | | Anestesiólogo |
| tipo_anestesia | VARCHAR(100) | | Tipo de anestesia |
| diagnostico_preoperatorio | TEXT | | Diagnóstico pre-op |
| diagnostico_postoperatorio | TEXT | | Diagnóstico post-op |
| hallazgos | TEXT | | Hallazgos quirúrgicos |
| complicaciones | TEXT | | Complicaciones |
| sangrado_estimado | VARCHAR(100) | | Sangrado estimado |
| especimenes_patologia | TEXT | | Especímenes enviados |
| pronostico | VARCHAR(200) | | Pronóstico |

---

### 16. TABLA: ordenes_medicas

**Descripción**: Órdenes médicas durante hospitalización

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| hospitalizacion_id | INTEGER | FK, NOT NULL | Referencia a hospitalizaciones |
| medico_id | INTEGER | FK, NOT NULL | Médico que ordena |
| tipo | ENUM | NOT NULL | Medicamento, Dieta, Signos Vitales, etc. |
| descripcion | TEXT | NOT NULL | Descripción de la orden |
| estado | ENUM | DEFAULT 'Activa' | Activa, Suspendida, Completada |
| fecha_hora | TIMESTAMP | AUTO | Fecha y hora |
| medicamento_id | INTEGER | FK | Para órdenes de medicamento |
| dosis | VARCHAR(100) | | Dosis |
| frecuencia | VARCHAR(100) | | Frecuencia |
| via | VARCHAR(50) | | Vía de administración |
| duracion | VARCHAR(100) | | Duración |

---

### 17. TABLA: tipos_estudio

**Descripción**: Catálogo de tipos de estudios de laboratorio

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| nombre | VARCHAR(200) | NOT NULL | Nombre del estudio |
| categoria | ENUM | NOT NULL | Hematología, Química, Función Hepática, etc. |
| descripcion | TEXT | | Descripción |
| activo | BOOLEAN | DEFAULT TRUE | Estado activo |

---

### 18. TABLA: resultados_laboratorio

**Descripción**: Resultados de estudios de laboratorio

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| consulta_id | INTEGER | FK | Referencia a consultas |
| tipo_estudio_id | INTEGER | FK, NOT NULL | Tipo de estudio |
| fecha_toma | TIMESTAMP | NOT NULL | Fecha de toma de muestra |
| fecha_resultado | TIMESTAMP | AUTO | Fecha de resultado |
| resultado | TEXT | NOT NULL | Resultado en formato JSON |
| valor_minimo | VARCHAR(50) | | Valor mínimo de referencia |
| valor_maximo | VARCHAR(50) | | Valor máximo de referencia |
| unidad | VARCHAR(50) | | Unidad de medida |
| valor_critico | BOOLEAN | DEFAULT FALSE | Si es valor crítico |
| laboratorio_externo | VARCHAR(200) | | Laboratorio externo |
| observaciones | TEXT | | Observaciones |

---

### 19. TABLA: caja

**Descripción**: Control de caja diaria

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| fecha_apertura | TIMESTAMP | AUTO | Fecha de apertura |
| fecha_cierre | TIMESTAMP | | Fecha de cierre |
| usuario_id | INTEGER | FK, NOT NULL | Usuario responsable |
| monto_inicial | FLOAT | NOT NULL | Monto inicial |
| monto_final | FLOAT | | Monto final |
| total_ingresos | FLOAT | | Total de ingresos |
| total_egresos | FLOAT | | Total de egresos |
| diferencia | FLOAT | | Diferencia (faltante/sobrante) |
| cerrada | BOOLEAN | DEFAULT FALSE | Estado de la caja |

---

### 20. TABLA: movimientos_caja

**Descripción**: Movimientos de ingreso y egreso en caja

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| caja_id | INTEGER | FK, NOT NULL | Referencia a caja |
| tipo_movimiento | ENUM | NOT NULL | Ingreso, Egreso |
| tipo_ingreso | ENUM | | Consulta, Reconsulta, Procedimiento, etc. |
| paciente_id | INTEGER | FK | Para ingresos |
| tipo_egreso | ENUM | | Compra Medicamentos, Servicios, etc. |
| proveedor | VARCHAR(200) | | Para egresos |
| concepto | VARCHAR(300) | NOT NULL | Concepto del movimiento |
| monto | FLOAT | NOT NULL | Monto |
| forma_pago | VARCHAR(50) | NOT NULL | Efectivo, Transferencia |
| numero_documento | VARCHAR(100) | | Número de factura/documento |
| fecha_hora | TIMESTAMP | AUTO | Fecha y hora |
| usuario_id | INTEGER | FK, NOT NULL | Usuario que registra |

---

### 21. TABLA: cuentas_por_cobrar

**Descripción**: Cuentas por cobrar a pacientes o convenios

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK | Paciente |
| convenio | VARCHAR(100) | | Convenio (IGSS, etc.) |
| concepto | VARCHAR(300) | NOT NULL | Concepto |
| monto_total | FLOAT | NOT NULL | Monto total |
| monto_pagado | FLOAT | DEFAULT 0 | Monto pagado |
| saldo | FLOAT | NOT NULL | Saldo pendiente |
| fecha_emision | DATE | NOT NULL | Fecha de emisión |
| fecha_vencimiento | DATE | | Fecha de vencimiento |
| pagado | BOOLEAN | DEFAULT FALSE | Estado pagado/pendiente |
| observaciones | TEXT | | Observaciones |

---

### 22. TABLA: cotizaciones

**Descripción**: Cotizaciones a pacientes

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK, NOT NULL | Referencia a pacientes |
| medico_id | INTEGER | FK | Médico |
| fecha | TIMESTAMP | AUTO | Fecha de cotización |
| vigencia_dias | INTEGER | DEFAULT 30 | Días de vigencia |
| servicios | TEXT | NOT NULL | Servicios en formato JSON |
| total | FLOAT | NOT NULL | Total |
| condiciones | TEXT | | Condiciones |
| aceptada | BOOLEAN | DEFAULT FALSE | Si fue aceptada |

---

### 23. TABLA: proveedores

**Descripción**: Proveedores de farmacia

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| nombre | VARCHAR(200) | NOT NULL | Nombre del proveedor |
| nit | VARCHAR(20) | | NIT |
| direccion | TEXT | | Dirección |
| telefono | VARCHAR(15) | | Teléfono |
| email | VARCHAR(100) | | Email |
| contacto | VARCHAR(100) | | Persona de contacto |
| activo | BOOLEAN | DEFAULT TRUE | Estado activo |

---

### 24. TABLA: productos_farmacia

**Descripción**: Productos de farmacia e inventario

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| medicamento_id | INTEGER | FK | Referencia a medicamentos |
| codigo_interno | VARCHAR(50) | UNIQUE | Código interno |
| nombre | VARCHAR(200) | NOT NULL | Nombre del producto |
| tipo | VARCHAR(50) | | Medicamento, Insumo, Material |
| presentacion | VARCHAR(100) | | Presentación |
| lote | VARCHAR(100) | | Lote |
| fecha_vencimiento | DATE | | Fecha de vencimiento |
| proveedor_id | INTEGER | FK | Proveedor |
| stock_actual | INTEGER | DEFAULT 0 | Stock actual |
| stock_minimo | INTEGER | DEFAULT 10 | Stock mínimo |
| precio_compra | FLOAT | NOT NULL | Precio de compra |
| precio_venta | FLOAT | NOT NULL | Precio de venta |
| ubicacion | VARCHAR(100) | | Ubicación en farmacia |
| activo | BOOLEAN | DEFAULT TRUE | Estado activo |
| created_at | TIMESTAMP | AUTO | Fecha de creación |

**Índices**:
- `idx_productos_nombre` en `nombre`
- `idx_productos_codigo` en `codigo_interno`

---

### 25. TABLA: movimientos_inventario

**Descripción**: Movimientos de entrada/salida de inventario

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| producto_id | INTEGER | FK, NOT NULL | Producto |
| tipo | ENUM | NOT NULL | Entrada, Salida, Ajuste |
| cantidad | INTEGER | NOT NULL | Cantidad |
| stock_anterior | INTEGER | NOT NULL | Stock antes del movimiento |
| stock_nuevo | INTEGER | NOT NULL | Stock después del movimiento |
| motivo | VARCHAR(300) | NOT NULL | Motivo del movimiento |
| usuario_id | INTEGER | FK, NOT NULL | Usuario que registra |
| fecha_hora | TIMESTAMP | AUTO | Fecha y hora |

---

### 26. TABLA: compras_farmacia

**Descripción**: Compras a proveedores

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| proveedor_id | INTEGER | FK, NOT NULL | Proveedor |
| fecha_compra | DATE | NOT NULL | Fecha de compra |
| numero_factura | VARCHAR(100) | | Número de factura |
| total | FLOAT | NOT NULL | Total de la compra |
| observaciones | TEXT | | Observaciones |
| usuario_id | INTEGER | FK, NOT NULL | Usuario que registra |
| created_at | TIMESTAMP | AUTO | Fecha de registro |

---

### 27. TABLA: detalle_compra

**Descripción**: Detalle de productos en compra

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| compra_id | INTEGER | FK, NOT NULL | Referencia a compras |
| producto_id | INTEGER | FK, NOT NULL | Producto |
| cantidad | INTEGER | NOT NULL | Cantidad |
| precio_unitario | FLOAT | NOT NULL | Precio unitario |
| subtotal | FLOAT | NOT NULL | Subtotal |

---

### 28. TABLA: ventas_farmacia

**Descripción**: Ventas de farmacia

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| paciente_id | INTEGER | FK | Paciente |
| receta_id | INTEGER | FK | Receta asociada |
| fecha_venta | TIMESTAMP | AUTO | Fecha de venta |
| total | FLOAT | NOT NULL | Total |
| descuento | FLOAT | DEFAULT 0 | Descuento aplicado |
| total_final | FLOAT | NOT NULL | Total final |
| usuario_id | INTEGER | FK, NOT NULL | Usuario que vende |

---

### 29. TABLA: detalle_venta

**Descripción**: Detalle de productos en venta

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| venta_id | INTEGER | FK, NOT NULL | Referencia a ventas |
| producto_id | INTEGER | FK, NOT NULL | Producto |
| cantidad | INTEGER | NOT NULL | Cantidad |
| precio_unitario | FLOAT | NOT NULL | Precio unitario |
| subtotal | FLOAT | NOT NULL | Subtotal |

---

### 30. TABLA: roles

**Descripción**: Roles de usuarios del sistema

| Campo | Tipo | Restricciones | Descripción |
|-------|------|---------------|-------------|
| id | INTEGER | PK, AUTO | ID único |
| nombre | VARCHAR(50) | NOT NULL, UNIQUE | Nombre del rol |
| descripcion | TEXT | | Descripción |

**Datos iniciales**:
- Médico
- Enfermera
- Recepcionista
- Administrador

---

## 🔗 Relaciones Principales
```sql
-- Pacientes → Consultas (1:N)
ALTER TABLE consultas 
ADD CONSTRAINT fk_consultas_paciente 
FOREIGN KEY (paciente_id) REFERENCES pacientes(id);

-- Pacientes → Citas (1:N)
ALTER TABLE citas 
ADD CONSTRAINT fk_citas_paciente 
FOREIGN KEY (paciente_id) REFERENCES pacientes(id);

-- Pacientes → Hospitalizaciones (1:N)
ALTER TABLE hospitalizaciones 
ADD CONSTRAINT fk_hospitalizaciones_paciente 
FOREIGN KEY (paciente_id) REFERENCES pacientes(id);

-- Hospitalizaciones → Notas Médicas (1:N)
ALTER TABLE notas_medicas 
ADD CONSTRAINT fk_notas_hospitalizacion 
FOREIGN KEY (hospitalizacion_id) REFERENCES hospitalizaciones(id);

-- Recetas → Receta Detalle (1:N)
ALTER TABLE receta_detalle 
ADD CONSTRAINT fk_detalle_receta 
FOREIGN KEY (receta_id) REFERENCES recetas(id);

-- Compras → Detalle Compra (1:N)
ALTER TABLE detalle_compra 
ADD CONSTRAINT fk_detalle_compra 
FOREIGN KEY (compra_id) REFERENCES compras_farmacia(id);

-- Ventas → Detalle Venta (1:N)
ALTER TABLE detalle_venta 
ADD CONSTRAINT fk_detalle_venta 
FOREIGN KEY (venta_id) REFERENCES ventas_farmacia(id);
```

---

## 📊 Enums Utilizados

### GeneroEnum
- `Masculino`
- `Femenino`
- `Otro`

### EstadoCivilEnum
- `Soltero`
- `Casado`
- `Divorciado`
- `Viudo`
- `Union Libre`

### TipoCitaEnum
- `Primera Consulta`
- `Reconsulta`
- `Procedimiento`
- `Control Embarazo`
- `Control Niño Sano`
- `Emergencia`

### EstadoCitaEnum
- `Programada`
- `Confirmada`
- `En Curso`
- `Completada`
- `Cancelada`
- `No Asistió`

### TipoAntecedenteEnum
- `Medicos`
- `Quirurgicos`
- `Traumaticos`
- `Alergicos`
- `Ginecologicos`
- `Obstetricos`

### TipoVacunaEnum
- `BCG`, `Hepatitis B`, `Pentavalente`, `Rotavirus`, `Neumococo`
- `Influenza`, `SRP`, `Varicela`, `Hepatitis A`, `DPT`, `OPV`, `COVID-19`, `Otra`

### EstadoCamaEnum
- `Disponible`
- `Ocupada`
- `Limpieza`
- `Mantenimiento`

### TipoNotaMedicaEnum
- `Ingreso`
- `Evolución`
- `Procedimiento`
- `Operatoria`
- `Egreso`

### TipoOrdenEnum
- `Medicamento`
- `Dieta`
- `Signos Vitales`
- `Laboratorio`
- `Estudio de Imagen`
- `Interconsulta`
- `Cuidados de Enfermería`
- `Otro`

### EstadoOrdenEnum
- `Activa`
- `Suspendida`
- `Completada`

### CategoriaLaboratorioEnum
- `Hematología`, `Química Sanguínea`, `Función Hepática`, `Función Renal`
- `Perfil Lipídico`, `Pruebas Tiroideas`, `Diabetes`, `Marcadores Tumorales`
- `Inmunología`, `Grupo Sanguíneo`, `Orina y Heces`, `Microbiología`, `Estudios de Imagen`, `Otro`

### EstadoInterconsultaEnum
- `Solicitada`
- `En Proceso`
- `Completada`
- `Cancelada`

### TipoMovimientoEnum
- `Ingreso`
- `Egreso`

### TipoIngresoEnum
- `Consulta Médica`, `Reconsulta`, `Procedimiento`, `Hospitalización`, `Venta Farmacia`, `Laboratorio`, `Otro`

### TipoEgresoEnum
- `Compra Medicamentos`, `Servicios`, `Salarios`, `Mantenimiento`, `Publicidad`, `Papelería`, `Otro`

### TipoMovimientoInventarioEnum
- `Entrada`
- `Salida`
- `Ajuste`

---

## 🔧 Mantenimiento

### Backups
```bash
# Backup completo
pg_dump -U postgres -d clinica_db -F c -f backup_$(date +%Y%m%d).dump

# Restaurar
pg_restore -U postgres -d clinica_db backup_20250115.dump
```

### Limpieza de Datos Antiguos
```sql
-- Eliminar archivos huérfanos (sin paciente)
DELETE FROM archivos_paciente 
WHERE paciente_id NOT IN (SELECT id FROM pacientes);

-- Marcar citas viejas como no asistió
UPDATE citas 
SET estado = 'No Asistió' 
WHERE estado = 'Programada' 
AND fecha_hora < NOW() - INTERVAL '1 day';
```

---

## 📈 Optimización

### Índices Recomendados
```sql
-- Índices para búsquedas frecuentes
CREATE INDEX idx_pacientes_busqueda ON pacientes USING gin(to_tsvector('spanish', nombres || ' ' || apellidos));
CREATE INDEX idx_consultas_fecha_paciente ON consultas(paciente_id, fecha_hora DESC);
CREATE INDEX idx_hospitalizaciones_activas ON hospitalizaciones(activa) WHERE activa = true;
CREATE INDEX idx_productos_stock ON productos_farmacia(stock_actual) WHERE stock_actual <= stock_minimo;
```

### Vacuum y Analyze
```sql
-- Ejecutar semanalmente
VACUUM ANALYZE;

-- Para tablas específicas con mucho movimiento
VACUUM ANALYZE movimientos_caja;
VACUUM ANALYZE movimientos_inventario;
```

---

**Última actualización**: Enero 2025  
**Versión**: 2.0.0