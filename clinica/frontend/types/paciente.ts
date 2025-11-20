// types/paciente.ts

// Enums que coinciden con el backend
export enum GeneroEnum {
  MASCULINO = "Masculino",
  FEMENINO = "Femenino",
  OTRO = "Otro"
}

export enum EstadoCivilEnum {
  SOLTERO = "Soltero/a",
  CASADO = "Casado/a",
  DIVORCIADO = "Divorciado/a",
  VIUDO = "Viudo/a",
  UNION_LIBRE = "Unión Libre"
}

export enum TipoSangreEnum {
  A_POSITIVO = "A+",
  A_NEGATIVO = "A-",
  B_POSITIVO = "B+",
  B_NEGATIVO = "B-",
  AB_POSITIVO = "AB+",
  AB_NEGATIVO = "AB-",
  O_POSITIVO = "O+",
  O_NEGATIVO = "O-"
}

export enum CategoriaArchivoEnum {
  FOTO = "foto",
  LABORATORIO = "laboratorio",
  IMAGEN = "imagen",
  RECETA = "receta",
  EKG = "ekg",
  VIDEO = "video",
  OTRO = "otro"
}

// Interface base de Paciente
export interface PacienteBase {
  // Datos personales
  nombres: string;
  apellidos: string;
  fecha_nacimiento: string; // ISO date string
  genero: GeneroEnum;
  dpi: string;
  
  // Contacto
  telefono_principal: string;
  telefono_secundario?: string;
  email?: string;
  direccion: string;
  municipio?: string;
  departamento?: string;
  
  // Información adicional
  estado_civil?: EstadoCivilEnum;
  religion?: string;
  ocupacion?: string;
  tipo_sangre?: TipoSangreEnum;
  
  // Seguro
  tiene_igss: boolean;
  numero_igss?: string;
  tiene_seguro_privado: boolean;
  nombre_seguro?: string;
  
  // Emergencia
  emergencia_nombre: string;
  emergencia_telefono: string;
  emergencia_parentesco?: string;
  
  // Otros
  observaciones?: string;
}

// Para crear paciente
export interface PacienteCreate extends PacienteBase {}

// Para actualizar paciente (todos opcionales)
export interface PacienteUpdate extends Partial<PacienteBase> {
  activo?: boolean;
}

// Respuesta completa del servidor
export interface Paciente extends PacienteBase {
  id: number;
  activo: boolean;
  foto_url?: string;
  created_at: string;
}

// Para listar pacientes (vista reducida)
export interface PacienteListItem {
  id: number;
  nombres: string;
  apellidos: string;
  dpi: string;
  telefono_principal: string;
  genero: GeneroEnum;
  foto_url?: string;
  activo: boolean;
}

// Archivos del paciente
export interface ArchivoPaciente {
  id: number;
  paciente_id: number;
  categoria: CategoriaArchivoEnum;
  nombre_archivo: string;
  ruta_archivo: string;
  tipo_mime: string;
  tamano_bytes: number;
  descripcion?: string;
  created_at: string;
}

// Estadísticas
export interface EstadisticasPacientes {
  total_pacientes: number;
  pacientes_activos: number;
  pacientes_inactivos: number;
  nuevos_este_mes: number;
  por_genero: Record<string, number>;
  por_tipo_sangre: Record<string, number>;
}

// Helper para calcular edad
export function calcularEdad(fechaNacimiento: string): number {
  const hoy = new Date();
  const nacimiento = new Date(fechaNacimiento);
  let edad = hoy.getFullYear() - nacimiento.getFullYear();
  const mes = hoy.getMonth() - nacimiento.getMonth();
  
  if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
    edad--;
  }
  
  return edad;
}

// Helper para formatear nombre completo
export function nombreCompleto(paciente: { nombres: string; apellidos: string }): string {
  return `${paciente.nombres} ${paciente.apellidos}`;
}

// Helper para formatear DPI
export function formatearDPI(dpi: string): string {
  // Formato: 1234 56789 0123
  return dpi.replace(/(\d{4})(\d{5})(\d{4})/, '$1 $2 $3');
}

// Helper para formatear teléfono
export function formatearTelefono(telefono: string): string {
  // Formato: 1234-5678
  return telefono.replace(/(\d{4})(\d{4})/, '$1-$2');
}