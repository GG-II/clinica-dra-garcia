export interface Usuario {
  id: number;
  username: string;
  email: string;
  nombres: string;
  apellidos: string;
  rol_id: number;
  activo: boolean;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface Rol {
  id: number;
  nombre: string;
  descripcion: string;
}

// ============================================================================
// TIPOS PARA PACIENTES (Sprint 2)
// ============================================================================

export interface Paciente {
  id: number;
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string;
  edad?: number;
  sexo: 'M' | 'F';
  dpi?: string;
  telefono?: string;
  telefono_emergencia?: string;
  direccion?: string;
  email?: string;
  estado_civil?: 'soltero' | 'casado' | 'divorciado' | 'viudo' | 'union_libre';
  religion?: string;
  ocupacion?: string;
  tiene_seguro: boolean;
  tipo_seguro?: string;
  contacto_emergencia?: string;
  foto_url?: string;
  notas?: string;
  activo: boolean;
  created_at: string;
  updated_at: string;
}

export interface PacienteCreate {
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string;
  sexo: 'M' | 'F';
  dpi?: string;
  telefono?: string;
  telefono_emergencia?: string;
  direccion?: string;
  email?: string;
  estado_civil?: 'soltero' | 'casado' | 'divorciado' | 'viudo' | 'union_libre';
  religion?: string;
  ocupacion?: string;
  tiene_seguro: boolean;
  tipo_seguro?: string;
  contacto_emergencia?: string;
  notas?: string;
}

export interface PacienteUpdate extends Partial<PacienteCreate> {}

export interface ArchivosPaciente {
  id: number;
  paciente_id: number;
  categoria: 'foto' | 'laboratorio' | 'imagen' | 'receta' | 'ekg' | 'video' | 'otro';
  nombre_archivo: string;
  ruta_archivo: string;
  tipo_mime: string;
  tamano_bytes: number;
  descripcion?: string;
  created_at: string;
}

export interface EstadisticasPacientes {
  total: number;
  nuevos_mes: number;
  activos: number;
  por_sexo: {
    masculino: number;
    femenino: number;
  };
}