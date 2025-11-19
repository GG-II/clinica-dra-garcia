# 🔌 Documentación de API - Sistema Clínico MEDGAR

Documentación completa de los endpoints del backend.

## 📋 Información General

**Base URL**: `http://localhost:8000/api/v1`  
**Red Local**: `http://192.168.1.10:8000/api/v1`  
**Swagger UI**: `http://localhost:8000/docs`  
**Autenticación**: JWT Bearer Token

---

## 🔐 Autenticación

### POST /auth/login

Iniciar sesión y obtener token JWT.

**Endpoint**: `POST /api/v1/auth/login`

**Headers**:
```
Content-Type: application/x-www-form-urlencoded
```

**Body** (form-urlencoded):
```
username: admin
password: admin123
```

**Response 200**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Errores**:
- `401`: Usuario o contraseña incorrectos
- `401`: Usuario inactivo

**Ejemplo cURL**:
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

**Ejemplo JavaScript/Axios**:
```javascript
const formData = new URLSearchParams();
formData.append('username', 'admin');
formData.append('password', 'admin123');

const response = await axios.post(
  'http://localhost:8000/api/v1/auth/login',
  formData,
  {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  }
);

const token = response.data.access_token;
```

---

### POST /auth/logout

Cerrar sesión (endpoint informativo, el token se elimina en el cliente).

**Endpoint**: `POST /api/v1/auth/logout`

**Response 200**:
```json
{
  "message": "Sesión cerrada exitosamente"
}
```

---

### GET /auth/me

Obtener información del usuario autenticado.

**Endpoint**: `GET /api/v1/auth/me`

**Headers**:
```
Authorization: Bearer {token}
```

**Response 200**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@clinica.com",
  "nombres": "Administrador",
  "apellidos": "Sistema",
  "rol_id": 1,
  "activo": true
}
```

**Errores**:
- `401`: Token inválido o expirado
- `401`: Usuario no encontrado

**Ejemplo cURL**:
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer {tu_token_aqui}"
```

---

## 👥 Usuarios

### GET /usuarios/roles

Obtener lista de roles del sistema.

**Endpoint**: `GET /api/v1/usuarios/roles`

**Response 200**:
```json
[
  {
    "id": 1,
    "nombre": "Administrador",
    "descripcion": "Acceso total al sistema",
    "created_at": "2025-11-19T01:25:30.873629-06:00"
  },
  {
    "id": 2,
    "nombre": "Médico",
    "descripcion": "Acceso a pacientes, historia clínica, agenda propia, recetas, hospitalización y laboratorios",
    "created_at": "2025-11-19T01:25:30.873629-06:00"
  },
  {
    "id": 3,
    "nombre": "Enfermera",
    "descripcion": "Acceso a pacientes, signos vitales, medicamentos, notas de enfermería y hospitalización",
    "created_at": "2025-11-19T01:25:30.873629-06:00"
  },
  {
    "id": 4,
    "nombre": "Recepcionista",
    "descripcion": "Acceso a agenda, citas, caja y datos básicos de pacientes",
    "created_at": "2025-11-19T01:25:30.873629-06:00"
  }
]
```

---

### GET /usuarios/

Obtener lista de usuarios (con paginación).

**Endpoint**: `GET /api/v1/usuarios/`

**Query Parameters**:
- `skip`: Número de registros a saltar (default: 0)
- `limit`: Número máximo de registros (default: 100, max: 100)

**Headers**:
```
Authorization: Bearer {token}
```

**Response 200**:
```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@clinica.com",
    "nombres": "Administrador",
    "apellidos": "Sistema",
    "rol_id": 1,
    "activo": true,
    "created_at": "2025-11-19T01:25:30.887639-06:00"
  }
]
```

**Ejemplo**:
```bash
curl -X GET "http://localhost:8000/api/v1/usuarios/?skip=0&limit=10" \
  -H "Authorization: Bearer {token}"
```

---

### GET /usuarios/{usuario_id}

Obtener un usuario específico por ID.

**Endpoint**: `GET /api/v1/usuarios/{usuario_id}`

**Headers**:
```
Authorization: Bearer {token}
```

**Response 200**:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@clinica.com",
  "nombres": "Administrador",
  "apellidos": "Sistema",
  "rol_id": 1,
  "activo": true,
  "created_at": "2025-11-19T01:25:30.887639-06:00"
}
```

**Errores**:
- `404`: Usuario no encontrado

---

### POST /usuarios/

Crear un nuevo usuario.

**Endpoint**: `POST /api/v1/usuarios/`

**Headers**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body**:
```json
{
  "username": "doctor1",
  "email": "doctor1@clinica.com",
  "password": "password123",
  "nombres": "Juan",
  "apellidos": "Pérez López",
  "rol_id": 2
}
```

**Response 201**:
```json
{
  "id": 2,
  "username": "doctor1",
  "email": "doctor1@clinica.com",
  "nombres": "Juan",
  "apellidos": "Pérez López",
  "rol_id": 2,
  "activo": true,
  "created_at": "2025-11-19T10:30:00.000000-06:00"
}
```

**Errores**:
- `400`: El username ya existe
- `400`: El email ya existe

**Validaciones**:
- `username`: 3-50 caracteres
- `email`: Email válido
- `password`: Mínimo 8 caracteres
- `nombres`: 2-100 caracteres
- `apellidos`: 2-100 caracteres
- `rol_id`: Debe existir en la tabla roles

---

### PUT /usuarios/{usuario_id}

Actualizar un usuario existente.

**Endpoint**: `PUT /api/v1/usuarios/{usuario_id}`

**Headers**:
```
Authorization: Bearer {token}
Content-Type: application/json
```

**Body** (todos los campos son opcionales):
```json
{
  "email": "nuevo_email@clinica.com",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez López",
  "rol_id": 2,
  "activo": false
}
```

**Response 200**:
```json
{
  "id": 2,
  "username": "doctor1",
  "email": "nuevo_email@clinica.com",
  "nombres": "Juan Carlos",
  "apellidos": "Pérez López",
  "rol_id": 2,
  "activo": false,
  "created_at": "2025-11-19T10:30:00.000000-06:00"
}
```

**Errores**:
- `404`: Usuario no encontrado

---

### DELETE /usuarios/{usuario_id}

Eliminar un usuario (borrado físico).

**Endpoint**: `DELETE /api/v1/usuarios/{usuario_id}`

**Headers**:
```
Authorization: Bearer {token}
```

**Response 204**: No Content

**Errores**:
- `404`: Usuario no encontrado

⚠️ **NOTA**: Este es un borrado permanente. Considerar cambiar a soft delete (activo=false) en producción.

---

## 🔑 Autenticación y Autorización

### Cómo Usar Tokens

1. **Obtener token** mediante `/auth/login`
2. **Guardar token** en cookie o localStorage
3. **Incluir en headers** de cada request:
```
   Authorization: Bearer {token}
```
4. **Renovar token** cuando expire (30 minutos por default)

### Ejemplo de Flujo Completo
```javascript
// 1. Login
const loginResponse = await axios.post('/auth/login', formData);
const token = loginResponse.data.access_token;

// 2. Guardar token
localStorage.setItem('token', token);

// 3. Configurar axios para incluir token automáticamente
axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;

// 4. Hacer requests protegidos
const usuarios = await axios.get('/usuarios/');

// 5. Obtener usuario actual
const me = await axios.get('/auth/me');

// 6. Logout
await axios.post('/auth/logout');
localStorage.removeItem('token');
```

---

## 📊 Modelos de Datos

### Usuario
```typescript
interface Usuario {
  id: number;
  username: string;        // Único, 3-50 caracteres
  email: string;          // Único, email válido
  password_hash: string;  // Encriptado con bcrypt
  nombres: string;        // 2-100 caracteres
  apellidos: string;      // 2-100 caracteres
  rol_id: number;         // FK a roles
  activo: boolean;        // true por default
  created_at: datetime;
  updated_at: datetime;
}
```

### Rol
```typescript
interface Rol {
  id: number;
  nombre: string;         // Único
  descripcion: string;
  created_at: datetime;
}
```

---

## 🚨 Códigos de Error

### Códigos HTTP

- `200`: OK
- `201`: Created
- `204`: No Content
- `400`: Bad Request (validación fallida)
- `401`: Unauthorized (no autenticado o token inválido)
- `403`: Forbidden (no tiene permisos)
- `404`: Not Found
- `422`: Unprocessable Entity (validación Pydantic)
- `500`: Internal Server Error

### Formato de Error
```json
{
  "detail": "Descripción del error"
}
```

O para errores de validación:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## 🧪 Testing con Swagger UI

1. Abrir: http://localhost:8000/docs
2. Click en "Authorize" (arriba a la derecha)
3. Login en `/auth/login` para obtener token
4. Copiar el `access_token`
5. Pegarlo en el campo "Value" del Authorize
6. Click "Authorize" y "Close"
7. Ahora todos los endpoints protegidos funcionarán

---

## 🔄 Rate Limiting

Actualmente **NO** hay rate limiting implementado.

**Recomendación para producción**:
- Implementar rate limiting por IP
- Límite sugerido: 100 requests/minuto por IP
- Usar middleware de FastAPI o proxy reverso (nginx)

---

## 📝 Notas Importantes

1. **Tokens JWT**:
   - Expiran en 30 minutos
   - No se pueden revocar (son stateless)
   - Para logout, eliminar del cliente

2. **Passwords**:
   - Se encriptan con bcrypt
   - Nunca se retornan en responses
   - Mínimo 8 caracteres requeridos

3. **CORS**:
   - Configurado para localhost:3000 y 192.168.1.10:3000
   - Cambiar en `.env` si necesitas otros orígenes

4. **Paginación**:
   - Default: skip=0, limit=100
   - Máximo: limit=100
   - Para más resultados, usar skip

---

## 🚀 Próximos Endpoints (Sprint 2)

- `POST /pacientes/` - Crear paciente
- `GET /pacientes/` - Listar pacientes
- `GET /pacientes/{id}` - Obtener paciente
- `PUT /pacientes/{id}` - Actualizar paciente
- `DELETE /pacientes/{id}` - Eliminar paciente
- `POST /pacientes/{id}/archivos` - Subir archivo
- `GET /pacientes/buscar?q={query}` - Búsqueda

---

**Última actualización**: Noviembre 2025  
**Versión API**: 1.0.0  
**Sprint**: 1/12