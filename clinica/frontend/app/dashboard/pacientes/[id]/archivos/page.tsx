// app/dashboard/pacientes/[id]/archivos/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { pacientesService } from '@/lib/pacientes';
import {
  Paciente,
  ArchivoPaciente,
  CategoriaArchivoEnum,
  nombreCompleto,
} from '@/types/paciente';
import { validarTamanoArchivo } from '@/lib/pacientes';

interface PageProps {
  params: {
    id: string;
  };
}

export default function ArchivosPage({ params }: PageProps) {
  const router = useRouter();
  const pacienteId = parseInt(params.id);

  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [archivos, setArchivos] = useState<ArchivoPaciente[]>([]);
  const [categoriaFiltro, setCategoriaFiltro] = useState<CategoriaArchivoEnum | 'todos'>('todos');
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Modal de subida
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadCategoria, setUploadCategoria] = useState<CategoriaArchivoEnum>(
    CategoriaArchivoEnum.OTRO
  );
  const [uploadDescripcion, setUploadDescripcion] = useState('');

  useEffect(() => {
    cargarDatos();
  }, [pacienteId, categoriaFiltro]);

  const cargarDatos = async () => {
    try {
      setLoading(true);
      const [pacienteData, archivosData] = await Promise.all([
        pacientesService.obtenerPorId(pacienteId),
        pacientesService.listarArchivos(
          pacienteId,
          categoriaFiltro === 'todos' ? undefined : categoriaFiltro
        ),
      ]);
      setPaciente(pacienteData);
      setArchivos(archivosData);
    } catch (error) {
      console.error('Error cargando datos:', error);
      setError('Error al cargar los archivos. Intenta recargar la página.');
    } finally {
      setLoading(false);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const validacion = validarTamanoArchivo(file, uploadCategoria);
    if (!validacion.valido) {
      setError(validacion.error!);
      return;
    }

    setSelectedFile(file);
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Por favor selecciona un archivo');
      return;
    }

    setUploading(true);
    setError('');

    try {
      await pacientesService.subirArchivo(
        pacienteId,
        uploadCategoria,
        selectedFile,
        uploadDescripcion
      );

      setSuccessMessage('Archivo subido exitosamente');
      setShowUploadModal(false);
      setSelectedFile(null);
      setUploadDescripcion('');
      setUploadCategoria(CategoriaArchivoEnum.OTRO);
      
      // Recargar archivos
      await cargarDatos();

      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error: any) {
      console.error('Error subiendo archivo:', error);
      setError(
        error.response?.data?.detail || 'Error al subir el archivo. Intenta de nuevo.'
      );
    } finally {
      setUploading(false);
    }
  };

  const handleDelete = async (archivoId: number) => {
    if (!confirm('¿Estás seguro de que deseas eliminar este archivo?')) {
      return;
    }

    try {
      await pacientesService.eliminarArchivo(pacienteId, archivoId);
      setSuccessMessage('Archivo eliminado exitosamente');
      await cargarDatos();
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error) {
      console.error('Error eliminando archivo:', error);
      setError('Error al eliminar el archivo. Intenta de nuevo.');
    }
  };

  const handleDownload = (archivo: ArchivoPaciente) => {
    const url = `http://localhost:8000/static/${archivo.ruta_archivo}`;
    window.open(url, '_blank');
  };

  const getCategoriaLabel = (categoria: CategoriaArchivoEnum): string => {
    const labels: Record<CategoriaArchivoEnum, string> = {
      [CategoriaArchivoEnum.FOTO]: 'Foto',
      [CategoriaArchivoEnum.LABORATORIO]: 'Laboratorio',
      [CategoriaArchivoEnum.IMAGEN]: 'Imagen Médica',
      [CategoriaArchivoEnum.RECETA]: 'Receta',
      [CategoriaArchivoEnum.EKG]: 'EKG',
      [CategoriaArchivoEnum.VIDEO]: 'Video',
      [CategoriaArchivoEnum.OTRO]: 'Otro',
    };
    return labels[categoria];
  };

  const getCategoriaIcon = (categoria: CategoriaArchivoEnum): string => {
    const icons: Record<CategoriaArchivoEnum, string> = {
      [CategoriaArchivoEnum.FOTO]: '📷',
      [CategoriaArchivoEnum.LABORATORIO]: '🔬',
      [CategoriaArchivoEnum.IMAGEN]: '🩻',
      [CategoriaArchivoEnum.RECETA]: '💊',
      [CategoriaArchivoEnum.EKG]: '❤️',
      [CategoriaArchivoEnum.VIDEO]: '🎥',
      [CategoriaArchivoEnum.OTRO]: '📄',
    };
    return icons[categoria];
  };

  const getCategoriaColor = (categoria: CategoriaArchivoEnum): string => {
    const colors: Record<CategoriaArchivoEnum, string> = {
      [CategoriaArchivoEnum.FOTO]: 'bg-blue-100 text-blue-800 border-blue-200',
      [CategoriaArchivoEnum.LABORATORIO]: 'bg-green-100 text-green-800 border-green-200',
      [CategoriaArchivoEnum.IMAGEN]: 'bg-purple-100 text-purple-800 border-purple-200',
      [CategoriaArchivoEnum.RECETA]: 'bg-pink-100 text-pink-800 border-pink-200',
      [CategoriaArchivoEnum.EKG]: 'bg-red-100 text-red-800 border-red-200',
      [CategoriaArchivoEnum.VIDEO]: 'bg-orange-100 text-orange-800 border-orange-200',
      [CategoriaArchivoEnum.OTRO]: 'bg-gray-100 text-gray-800 border-gray-200',
    };
    return colors[categoria];
  };

  const formatBytes = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando archivos...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => router.push(`/dashboard/pacientes/${pacienteId}`)}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <svg
              className="w-6 h-6 text-gray-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M10 19l-7-7m0 0l7-7m-7 7h18"
              />
            </svg>
          </button>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">
              Archivos de {paciente ? nombreCompleto(paciente) : 'Paciente'}
            </h1>
            <p className="text-gray-600 mt-1">
              Laboratorios, imágenes, recetas y documentos médicos
            </p>
          </div>
        </div>

        <button
          onClick={() => setShowUploadModal(true)}
          className="inline-flex items-center px-4 py-2.5 border border-transparent rounded-lg text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 transition-colors shadow-sm hover:shadow-md"
        >
          <svg
            className="-ml-1 mr-2 h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
            />
          </svg>
          Subir Archivo
        </button>
      </div>

      {/* Mensajes */}
      {successMessage && (
        <div className="bg-green-50 border border-green-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 text-green-800">
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
            <span className="text-sm font-medium">{successMessage}</span>
          </div>
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <svg className="h-5 w-5 text-red-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div className="flex-1">
              <p className="text-sm text-red-800">{error}</p>
            </div>
            <button onClick={() => setError('')} className="text-red-600 hover:text-red-800">
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Filtros */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div className="flex items-center space-x-2 overflow-x-auto">
          <button
            onClick={() => setCategoriaFiltro('todos')}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
              categoriaFiltro === 'todos'
                ? 'bg-purple-100 text-purple-800 border border-purple-300'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            📁 Todos ({archivos.length})
          </button>
          {Object.values(CategoriaArchivoEnum).map((cat) => {
            const count = archivos.filter((a) => a.categoria === cat).length;
            return (
              <button
                key={cat}
                onClick={() => setCategoriaFiltro(cat)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
                  categoriaFiltro === cat
                    ? getCategoriaColor(cat) + ' border'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {getCategoriaIcon(cat)} {getCategoriaLabel(cat)} ({count})
              </button>
            );
          })}
        </div>
      </div>

      {/* Lista de Archivos */}
      {archivos.length === 0 ? (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-12">
          <div className="text-center">
            <svg
              className="mx-auto h-16 w-16 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z"
              />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900">
              No hay archivos
            </h3>
            <p className="mt-2 text-sm text-gray-500">
              {categoriaFiltro === 'todos'
                ? 'Este paciente no tiene archivos subidos'
                : `No hay archivos en la categoría ${getCategoriaLabel(categoriaFiltro)}`}
            </p>
            <button
              onClick={() => setShowUploadModal(true)}
              className="mt-6 inline-flex items-center px-4 py-2 border border-transparent rounded-lg text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 transition-colors"
            >
              <svg
                className="-ml-1 mr-2 h-5 w-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                />
              </svg>
              Subir Primer Archivo
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {archivos.map((archivo) => (
            <div
              key={archivo.id}
              className="bg-white rounded-xl shadow-sm border border-gray-200 p-4 hover:shadow-md transition-shadow"
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <span
                  className={`inline-flex items-center px-2.5 py-1 rounded-lg text-xs font-medium border ${getCategoriaColor(
                    archivo.categoria
                  )}`}
                >
                  {getCategoriaIcon(archivo.categoria)} {getCategoriaLabel(archivo.categoria)}
                </span>
                <button
                  onClick={() => handleDelete(archivo.id)}
                  className="p-1 text-gray-400 hover:text-red-600 transition-colors"
                  title="Eliminar archivo"
                >
                  <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                    />
                  </svg>
                </button>
              </div>

              {/* Nombre del Archivo */}
              <h3 className="text-sm font-medium text-gray-900 truncate mb-2">
                {archivo.nombre_archivo}
              </h3>

              {/* Descripción */}
              {archivo.descripcion && (
                <p className="text-xs text-gray-600 mb-3 line-clamp-2">
                  {archivo.descripcion}
                </p>
              )}

              {/* Metadata */}
              <div className="space-y-1 mb-3">
                <p className="text-xs text-gray-500">
                  📦 {formatBytes(archivo.tamano_bytes)}
                </p>
                <p className="text-xs text-gray-500">
                  📅 {new Date(archivo.created_at).toLocaleDateString('es-GT')}
                </p>
              </div>

              {/* Botón de Descarga */}
              <button
                onClick={() => handleDownload(archivo)}
                className="w-full px-3 py-2 bg-purple-50 text-purple-700 rounded-lg text-sm font-medium hover:bg-purple-100 transition-colors flex items-center justify-center space-x-2"
              >
                <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                  />
                </svg>
                <span>Descargar / Ver</span>
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Modal de Subida */}
      {showUploadModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto">
          <div className="flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center sm:block sm:p-0">
            {/* Overlay */}
            <div
              className="fixed inset-0 transition-opacity bg-gray-500 bg-opacity-75"
              onClick={() => setShowUploadModal(false)}
            ></div>

            {/* Modal */}
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div className="bg-white px-6 pt-6 pb-4">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Subir Nuevo Archivo
                  </h3>
                  <button
                    onClick={() => setShowUploadModal(false)}
                    className="text-gray-400 hover:text-gray-600"
                  >
                    <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M6 18L18 6M6 6l12 12"
                      />
                    </svg>
                  </button>
                </div>

                <div className="space-y-4">
                  {/* Categoría */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Categoría <span className="text-red-500">*</span>
                    </label>
                    <select
                      value={uploadCategoria}
                      onChange={(e) => setUploadCategoria(e.target.value as CategoriaArchivoEnum)}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    >
                      {Object.values(CategoriaArchivoEnum)
                        .filter((cat) => cat !== CategoriaArchivoEnum.FOTO)
                        .map((cat) => (
                          <option key={cat} value={cat}>
                            {getCategoriaIcon(cat)} {getCategoriaLabel(cat)}
                          </option>
                        ))}
                    </select>
                  </div>

                  {/* Archivo */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Archivo <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="file"
                      onChange={handleFileSelect}
                      className="w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
                    />
                    <p className="mt-1 text-xs text-gray-500">
                      Máximo:{' '}
                      {uploadCategoria === CategoriaArchivoEnum.VIDEO ? '50 MB' : '5 MB'}
                    </p>
                  </div>

                  {/* Descripción */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Descripción (opcional)
                    </label>
                    <textarea
                      value={uploadDescripcion}
                      onChange={(e) => setUploadDescripcion(e.target.value)}
                      rows={3}
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      placeholder="Ej: Hemograma completo del 15/01/2025"
                    />
                  </div>

                  {/* Preview del archivo seleccionado */}
                  {selectedFile && (
                    <div className="bg-purple-50 border border-purple-200 rounded-lg p-3">
                      <div className="flex items-center space-x-3">
                        <svg className="h-8 w-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                        </svg>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {selectedFile.name}
                          </p>
                          <p className="text-xs text-gray-600">
                            {formatBytes(selectedFile.size)}
                          </p>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>

              {/* Botones */}
              <div className="bg-gray-50 px-6 py-4 flex justify-end space-x-3">
                <button
                  type="button"
                  onClick={() => setShowUploadModal(false)}
                  disabled={uploading}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleUpload}
                  disabled={!selectedFile || uploading}
                  className="px-4 py-2 border border-transparent rounded-lg text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed inline-flex items-center"
                >
                  {uploading ? (
                    <>
                      <svg
                        className="animate-spin -ml-1 mr-2 h-4 w-4 text-white"
                        xmlns="http://www.w3.org/2000/svg"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      Subiendo...
                    </>
                  ) : (
                    <>
                      <svg
                        className="-ml-1 mr-2 h-5 w-5"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
                        />
                      </svg>
                      Subir Archivo
                    </>
                  )}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}