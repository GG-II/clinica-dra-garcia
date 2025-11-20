// lib/pacientes.ts

import api from './api';
import {
  Paciente,
  PacienteCreate,
  PacienteUpdate,
  PacienteListItem,
  ArchivoPaciente,
  EstadisticasPacientes,
  CategoriaArchivoEnum
} from '@/types/paciente';

/**
 * Servicio para interactuar con la API de Pacientes
 */
export const pacientesService = {
  /**
   * Crear un nuevo paciente
   */
  async crear(data: PacienteCreate): Promise<Paciente> {
    const response = await api.post<Paciente>('/pacientes/', data);
    return response.data;
  },

  /**
   * Listar todos los pacientes con búsqueda y paginación
   */
  async listar(params?: {
    skip?: number;
    limit?: number;
    buscar?: string;
  }): Promise<Paciente[]> {
    const response = await api.get<Paciente[]>('/pacientes/', { params });
    return response.data;
  },

  /**
   * Obtener estadísticas de pacientes
   */
  async estadisticas(): Promise<EstadisticasPacientes> {
    const response = await api.get<EstadisticasPacientes>('/pacientes/estadisticas');
    return response.data;
  },

  /**
   * Obtener un paciente por ID
   */
  async obtenerPorId(id: number): Promise<Paciente> {
    const response = await api.get<Paciente>(`/pacientes/${id}`);
    return response.data;
  },

  /**
   * Actualizar un paciente
   */
  async actualizar(id: number, data: PacienteUpdate): Promise<Paciente> {
    const response = await api.put<Paciente>(`/pacientes/${id}`, data);
    return response.data;
  },

  /**
   * Desactivar un paciente (borrado lógico)
   */
  async eliminar(id: number): Promise<void> {
    await api.delete(`/pacientes/${id}`);
  },

  // ==================== ARCHIVOS ====================

  /**
   * Subir foto del paciente
   */
  async subirFoto(pacienteId: number, archivo: File): Promise<ArchivoPaciente> {
    const formData = new FormData();
    formData.append('foto', archivo);

    const response = await api.post<ArchivoPaciente>(
      `/pacientes/${pacienteId}/foto`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  /**
   * Subir documento del paciente (laboratorio, imagen, receta, etc.)
   */
  async subirArchivo(
    pacienteId: number,
    categoria: CategoriaArchivoEnum,
    archivo: File,
    descripcion?: string
  ): Promise<ArchivoPaciente> {
    const formData = new FormData();
    formData.append('archivo', archivo);
    formData.append('categoria', categoria);
    if (descripcion) {
      formData.append('descripcion', descripcion);
    }

    const response = await api.post<ArchivoPaciente>(
      `/pacientes/${pacienteId}/archivos`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  },

  /**
   * Listar archivos del paciente
   */
  async listarArchivos(
    pacienteId: number,
    categoria?: CategoriaArchivoEnum
  ): Promise<ArchivoPaciente[]> {
    const params = categoria ? { categoria } : undefined;
    const response = await api.get<ArchivoPaciente[]>(
      `/pacientes/${pacienteId}/archivos`,
      { params }
    );
    return response.data;
  },

  /**
   * Eliminar archivo del paciente
   */
  async eliminarArchivo(pacienteId: number, archivoId: number): Promise<void> {
    await api.delete(`/pacientes/${pacienteId}/archivos/${archivoId}`);
  },
};

// ==================== VALIDACIONES CLIENTE ====================

/**
 * Validar DPI guatemalteco (13 dígitos)
 */
export function validarDPI(dpi: string): { valido: boolean; error?: string } {
  // Remover espacios
  const dpiLimpio = dpi.replace(/\s/g, '');

  if (!/^\d+$/.test(dpiLimpio)) {
    return { valido: false, error: 'El DPI debe contener solo números' };
  }

  if (dpiLimpio.length !== 13) {
    return { valido: false, error: 'El DPI debe tener exactamente 13 dígitos' };
  }

  return { valido: true };
}

/**
 * Validar teléfono guatemalteco (8 dígitos)
 */
export function validarTelefono(telefono: string): { valido: boolean; error?: string } {
  // Remover espacios y guiones
  const telefonoLimpio = telefono.replace(/[\s-]/g, '');

  if (!/^\d+$/.test(telefonoLimpio)) {
    return { valido: false, error: 'El teléfono debe contener solo números' };
  }

  if (telefonoLimpio.length !== 8) {
    return { valido: false, error: 'El teléfono debe tener 8 dígitos' };
  }

  return { valido: true };
}

/**
 * Validar edad mínima (0 años) y máxima (120 años)
 */
export function validarFechaNacimiento(fecha: string): { valido: boolean; error?: string } {
  const nacimiento = new Date(fecha);
  const hoy = new Date();

  if (nacimiento > hoy) {
    return { valido: false, error: 'La fecha de nacimiento no puede ser futura' };
  }

  const edad = hoy.getFullYear() - nacimiento.getFullYear();

  if (edad > 120) {
    return { valido: false, error: 'La fecha de nacimiento no es válida' };
  }

  return { valido: true };
}

/**
 * Validar tamaño de archivo
 */
export function validarTamanoArchivo(
  archivo: File,
  categoria: CategoriaArchivoEnum
): { valido: boolean; error?: string } {
  const MAX_IMAGE_SIZE = 5 * 1024 * 1024; // 5 MB
  const MAX_VIDEO_SIZE = 50 * 1024 * 1024; // 50 MB
  const MAX_DOC_SIZE = 5 * 1024 * 1024; // 5 MB

  if (categoria === CategoriaArchivoEnum.VIDEO) {
    if (archivo.size > MAX_VIDEO_SIZE) {
      return { valido: false, error: 'El video no puede ser mayor a 50 MB' };
    }
  } else {
    if (archivo.size > MAX_DOC_SIZE) {
      return { valido: false, error: 'El archivo no puede ser mayor a 5 MB' };
    }
  }

  return { valido: true };
}

/**
 * Validar tipo de archivo para foto
 */
export function validarTipoFoto(archivo: File): { valido: boolean; error?: string } {
  const tiposPermitidos = ['image/jpeg', 'image/png', 'image/jpg'];

  if (!tiposPermitidos.includes(archivo.type)) {
    return { valido: false, error: 'Solo se permiten imágenes JPG o PNG' };
  }

  if (archivo.size > 5 * 1024 * 1024) {
    return { valido: false, error: 'La imagen no puede ser mayor a 5 MB' };
  }

  return { valido: true };
}