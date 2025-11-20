import api from '../api';
import { Paciente, PacienteCreate, PacienteUpdate, ArchivosPaciente, EstadisticasPacientes } from '@/types';

export const pacientesService = {
  /**
   * Obtener todos los pacientes
   */
  async getAll(
    skip: number = 0,
    limit: number = 100,
    search?: string,
    activo?: boolean
  ): Promise<Paciente[]> {
    const params = new URLSearchParams();
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    if (search) params.append('search', search);
    if (activo !== undefined) params.append('activo', activo.toString());

    const response = await api.get<Paciente[]>(`/pacientes?${params.toString()}`);
    return response.data;
  },

  /**
   * Buscar pacientes
   */
  async search(query: string): Promise<Paciente[]> {
    const response = await api.get<Paciente[]>(`/pacientes/buscar/${encodeURIComponent(query)}`);
    return response.data;
  },

  /**
   * Obtener un paciente por ID
   */
  async getById(id: number): Promise<Paciente> {
    const response = await api.get<Paciente>(`/pacientes/${id}`);
    return response.data;
  },

  /**
   * Crear un nuevo paciente
   */
  async create(paciente: PacienteCreate): Promise<Paciente> {
    const response = await api.post<Paciente>('/pacientes', paciente);
    return response.data;
  },

  /**
   * Actualizar un paciente
   */
  async update(id: number, paciente: PacienteUpdate): Promise<Paciente> {
    const response = await api.put<Paciente>(`/pacientes/${id}`, paciente);
    return response.data;
  },

  /**
   * Eliminar un paciente (soft delete)
   */
  async delete(id: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(`/pacientes/${id}`);
    return response.data;
  },

  /**
   * Obtener archivos de un paciente
   */
  async getArchivos(pacienteId: number): Promise<ArchivosPaciente[]> {
    const response = await api.get<ArchivosPaciente[]>(`/pacientes/${pacienteId}/archivos`);
    return response.data;
  },

  /**
   * Subir archivo para un paciente
   */
  async uploadArchivo(
    pacienteId: number,
    file: File,
    categoria: string,
    descripcion?: string
  ): Promise<ArchivosPaciente> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('categoria', categoria);
    if (descripcion) formData.append('descripcion', descripcion);

    const response = await api.post<ArchivosPaciente>(
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
   * Eliminar archivo
   */
  async deleteArchivo(pacienteId: number, archivoId: number): Promise<{ message: string }> {
    const response = await api.delete<{ message: string }>(
      `/pacientes/${pacienteId}/archivos/${archivoId}`
    );
    return response.data;
  },

  /**
   * Obtener estadísticas de pacientes
   */
  async getEstadisticas(): Promise<EstadisticasPacientes> {
    const response = await api.get<EstadisticasPacientes>('/pacientes/estadisticas');
    return response.data;
  },
};