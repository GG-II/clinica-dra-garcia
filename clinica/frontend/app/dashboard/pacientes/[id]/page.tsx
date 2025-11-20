'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { pacientesService } from '@/lib/services/pacientes.service';
import { Paciente, ArchivosPaciente } from '@/types';

export default function PacienteProfilePage() {
  const params = useParams();
  const router = useRouter();
  const pacienteId = parseInt(params.id as string);

  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [archivos, setArchivos] = useState<ArchivosPaciente[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'info' | 'archivos' | 'historia'>('info');
  const [uploadingFile, setUploadingFile] = useState(false);

  useEffect(() => {
    loadData();
  }, [pacienteId]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [pacienteData, archivosData] = await Promise.all([
        pacientesService.getById(pacienteId),
        pacientesService.getArchivos(pacienteId),
      ]);
      setPaciente(pacienteData);
      setArchivos(archivosData);
    } catch (error) {
      console.error('Error al cargar datos:', error);
    } finally {
      setLoading(false);
    }
  };

  const calcularEdad = (fechaNacimiento: string): number => {
    const hoy = new Date();
    const nacimiento = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - nacimiento.getFullYear();
    const mes = hoy.getMonth() - nacimiento.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < nacimiento.getDate())) {
      edad--;
    }
    return edad;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-GT', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validar tamaño
    const maxSize = file.type.startsWith('video/') ? 50 * 1024 * 1024 : 5 * 1024 * 1024;
    if (file.size > maxSize) {
      alert(
        `El archivo es muy grande. Máximo ${file.type.startsWith('video/') ? '50' : '5'} MB`
      );
      return;
    }

    try {
      setUploadingFile(true);
      const categoria = file.type.startsWith('image/')
        ? 'foto'
        : file.type === 'application/pdf'
        ? 'laboratorio'
        : 'otro';

      await pacientesService.uploadArchivo(pacienteId, file, categoria);
      await loadData(); // Recargar archivos
      alert('Archivo subido exitosamente');
    } catch (error) {
      console.error('Error al subir archivo:', error);
      alert('Error al subir el archivo');
    } finally {
      setUploadingFile(false);
    }
  };

  const handleDeleteArchivo = async (archivoId: number) => {
    if (!confirm('¿Estás seguro de eliminar este archivo?')) return;

    try {
      await pacientesService.deleteArchivo(pacienteId, archivoId);
      await loadData();
      alert('Archivo eliminado exitosamente');
    } catch (error) {
      console.error('Error al eliminar archivo:', error);
      alert('Error al eliminar el archivo');
    }
  };

  const getCategoriaColor = (categoria: string) => {
    const colors: Record<string, string> = {
      foto: 'bg-purple-100 text-purple-800',
      laboratorio: 'bg-blue-100 text-blue-800',
      imagen: 'bg-green-100 text-green-800',
      receta: 'bg-pink-100 text-pink-800',
      ekg: 'bg-red-100 text-red-800',
      video: 'bg-yellow-100 text-yellow-800',
      otro: 'bg-gray-100 text-gray-800',
    };
    return colors[categoria] || colors.otro;
  };

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12">
        <div className="flex flex-col items-center justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
          <p className="mt-4 text-gray-600">Cargando información del paciente...</p>
        </div>
      </div>
    );
  }

  if (!paciente) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12">
        <div className="text-center">
          <h3 className="text-lg font-medium text-gray-900">Paciente no encontrado</h3>
          <button
            onClick={() => router.push('/dashboard/pacientes')}
            className="mt-4 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Volver a la lista
          </button>
        </div>
      </div>
    );
  }

  const edad = calcularEdad(paciente.fecha_nacimiento);

  return (
    <div className="space-y-6">
      {/* Header con información principal */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="flex items-start justify-between">
          <div className="flex items-start space-x-6">
            {/* Avatar */}
            {paciente.foto_url ? (
              <img
                src={paciente.foto_url}
                alt={`${paciente.nombres} ${paciente.apellidos}`}
                className="w-24 h-24 rounded-full object-cover"
              />
            ) : (
              <div className="w-24 h-24 rounded-full bg-gradient-to-br from-purple-400 to-purple-600 flex items-center justify-center">
                <span className="text-3xl font-bold text-white">
                  {paciente.nombres.charAt(0)}
                  {paciente.apellidos.charAt(0)}
                </span>
              </div>
            )}

            {/* Información principal */}
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {paciente.nombres} {paciente.apellidos}
              </h1>
              <div className="flex items-center space-x-4 mt-2">
                <span
                  className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${
                    paciente.sexo === 'M'
                      ? 'bg-blue-100 text-blue-800'
                      : 'bg-pink-100 text-pink-800'
                  }`}
                >
                  {paciente.sexo === 'M' ? '♂ Masculino' : '♀ Femenino'}
                </span>
                <span className="text-gray-600">{edad} años</span>
                {paciente.tiene_seguro && (
                  <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-800">
                    <svg
                      className="w-4 h-4 mr-1"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    {paciente.tipo_seguro || 'Seguro Médico'}
                  </span>
                )}
              </div>

              {/* Datos rápidos */}
              <div className="grid grid-cols-3 gap-4 mt-4">
                {paciente.dpi && (
                  <div>
                    <p className="text-xs text-gray-500">DPI</p>
                    <p className="text-sm font-medium text-gray-900">{paciente.dpi}</p>
                  </div>
                )}
                {paciente.telefono && (
                  <div>
                    <p className="text-xs text-gray-500">Teléfono</p>
                    <p className="text-sm font-medium text-gray-900">
                      {paciente.telefono}
                    </p>
                  </div>
                )}
                <div>
                  <p className="text-xs text-gray-500">Fecha de Nacimiento</p>
                  <p className="text-sm font-medium text-gray-900">
                    {formatDate(paciente.fecha_nacimiento)}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Botones de acción */}
          <div className="flex space-x-2">
            <button
              onClick={() => router.push(`/dashboard/pacientes/${paciente.id}/editar`)}
              className="px-4 py-2 border border-purple-300 text-purple-700 rounded-lg hover:bg-purple-50 font-medium transition-colors"
            >
              Editar
            </button>
            <button
              onClick={() => router.push('/dashboard/pacientes')}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium transition-colors"
            >
              Volver
            </button>
          </div>
        </div>

        {/* Tabs */}
        <div className="mt-6 border-t border-gray-200">
          <nav className="-mb-px flex space-x-8 mt-6">
            {[
              { id: 'info', name: 'Información', icon: '📋' },
              { id: 'archivos', name: 'Archivos', icon: '📎', count: archivos.length },
              { id: 'historia', name: 'Historia Clínica', icon: '🏥' },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`
                  ${
                    activeTab === tab.id
                      ? 'border-purple-500 text-purple-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }
                  whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm transition-colors flex items-center space-x-2
                `}
              >
                <span>{tab.icon}</span>
                <span>{tab.name}</span>
                {tab.count !== undefined && (
                  <span
                    className={`ml-2 py-0.5 px-2 rounded-full text-xs ${
                      activeTab === tab.id
                        ? 'bg-purple-100 text-purple-600'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {tab.count}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>
      </div>

      {/* Contenido de tabs */}
      {activeTab === 'info' && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Información de contacto */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Contacto</h3>
            <div className="space-y-3">
              {paciente.email && (
                <div>
                  <p className="text-sm text-gray-500">Email</p>
                  <p className="text-sm font-medium text-gray-900">{paciente.email}</p>
                </div>
              )}
              {paciente.telefono_emergencia && (
                <div>
                  <p className="text-sm text-gray-500">Teléfono de Emergencia</p>
                  <p className="text-sm font-medium text-gray-900">
                    {paciente.telefono_emergencia}
                  </p>
                </div>
              )}
              {paciente.contacto_emergencia && (
                <div>
                  <p className="text-sm text-gray-500">Contacto de Emergencia</p>
                  <p className="text-sm font-medium text-gray-900">
                    {paciente.contacto_emergencia}
                  </p>
                </div>
              )}
              {paciente.direccion && (
                <div>
                  <p className="text-sm text-gray-500">Dirección</p>
                  <p className="text-sm font-medium text-gray-900">{paciente.direccion}</p>
                </div>
              )}
            </div>
          </div>

          {/* Información adicional */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Información Adicional
            </h3>
            <div className="space-y-3">
              {paciente.estado_civil && (
                <div>
                  <p className="text-sm text-gray-500">Estado Civil</p>
                  <p className="text-sm font-medium text-gray-900 capitalize">
                    {paciente.estado_civil.replace('_', ' ')}
                  </p>
                </div>
              )}
              {paciente.religion && (
                <div>
                  <p className="text-sm text-gray-500">Religión</p>
                  <p className="text-sm font-medium text-gray-900">{paciente.religion}</p>
                </div>
              )}
              {paciente.ocupacion && (
                <div>
                  <p className="text-sm text-gray-500">Ocupación</p>
                  <p className="text-sm font-medium text-gray-900">{paciente.ocupacion}</p>
                </div>
              )}
              {paciente.notas && (
                <div>
                  <p className="text-sm text-gray-500">Notas</p>
                  <p className="text-sm font-medium text-gray-900">{paciente.notas}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'archivos' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-gray-900">
              Archivos del Paciente
            </h3>
            <label className="cursor-pointer">
              <input
                type="file"
                onChange={handleFileUpload}
                disabled={uploadingFile}
                className="hidden"
                accept="image/*,application/pdf,video/mp4"
              />
              <span className="inline-flex items-center px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white font-medium rounded-lg transition-colors disabled:opacity-50">
                {uploadingFile ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Subiendo...
                  </>
                ) : (
                  <>
                    <svg
                      className="w-5 h-5 mr-2"
                      fill="none"
                      stroke="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M12 4v16m8-8H4"
                      />
                    </svg>
                    Subir Archivo
                  </>
                )}
              </span>
            </label>
          </div>

          {archivos.length === 0 ? (
            <div className="text-center py-12">
              <svg
                className="mx-auto h-12 w-12 text-gray-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <h3 className="mt-4 text-sm font-medium text-gray-900">
                No hay archivos
              </h3>
              <p className="mt-2 text-sm text-gray-500">
                Sube archivos para este paciente usando el botón de arriba
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {archivos.map((archivo) => (
                <div
                  key={archivo.id}
                  className="border border-gray-200 rounded-lg p-4 hover:border-purple-300 transition-colors"
                >
                  <div className="flex items-start justify-between mb-2">
                    <span
                      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getCategoriaColor(
                        archivo.categoria
                      )}`}
                    >
                      {archivo.categoria}
                    </span>
                    <button
                      onClick={() => handleDeleteArchivo(archivo.id)}
                      className="text-red-600 hover:text-red-800"
                    >
                      <svg
                        className="w-5 h-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                        />
                      </svg>
                    </button>
                  </div>
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {archivo.nombre_archivo}
                  </p>
                  <p className="text-xs text-gray-500 mt-1">
                    {(archivo.tamano_bytes / 1024).toFixed(2)} KB
                  </p>
                  <p className="text-xs text-gray-500">
                    {formatDate(archivo.created_at)}
                  </p>
                  {archivo.descripcion && (
                    <p className="text-xs text-gray-600 mt-2">{archivo.descripcion}</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'historia' && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="text-center py-12">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
              />
            </svg>
            <h3 className="mt-4 text-sm font-medium text-gray-900">
              Historia Clínica
            </h3>
            <p className="mt-2 text-sm text-gray-500">
              Próximamente en Sprint 3
            </p>
          </div>
        </div>
      )}
    </div>
  );
}