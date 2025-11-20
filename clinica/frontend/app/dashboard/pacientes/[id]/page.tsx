// app/dashboard/pacientes/[id]/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { pacientesService } from '@/lib/pacientes';
import { Paciente, calcularEdad, formatearDPI, formatearTelefono } from '@/types/paciente';
import PacienteForm from '@/components/pacientes/PacienteForm';
import SubirFoto from '@/components/pacientes/SubirFoto';
import Image from 'next/image';

interface PageProps {
  params: {
    id: string;
  };
}

export default function PacientePage({ params }: PageProps) {
  const router = useRouter();
  const pacienteId = parseInt(params.id);
  
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [loading, setLoading] = useState(true);
  const [isEditing, setIsEditing] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Cargar datos del paciente
  useEffect(() => {
    cargarPaciente();
  }, [pacienteId]);

  const cargarPaciente = async () => {
    try {
      setLoading(true);
      const data = await pacientesService.obtenerPorId(pacienteId);
      setPaciente(data);
    } catch (error: any) {
      console.error('Error cargando paciente:', error);
      if (error.response?.status === 404) {
        setError('Paciente no encontrado');
      } else {
        setError('Error al cargar el paciente. Intenta recargar la página.');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleUpdate = async (data: any) => {
    setSaving(true);
    setError('');
    setSuccessMessage('');

    try {
      const actualizado = await pacientesService.actualizar(pacienteId, data);
      setPaciente(actualizado);
      setIsEditing(false);
      setSuccessMessage('Paciente actualizado exitosamente');
      
      // Limpiar mensaje después de 3 segundos
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error: any) {
      console.error('Error actualizando paciente:', error);
      if (error.response?.status === 400) {
        const detail = error.response?.data?.detail;
        if (detail?.includes('DPI')) {
          setError('Ya existe otro paciente registrado con este DPI');
        } else {
          setError(detail || 'Error al actualizar el paciente. Verifica los datos.');
        }
      } else {
        setError('Error al actualizar el paciente. Intenta de nuevo.');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async () => {
    if (!confirm('¿Estás seguro de que deseas desactivar este paciente?')) {
      return;
    }

    try {
      await pacientesService.eliminar(pacienteId);
      router.push('/dashboard/pacientes');
    } catch (error) {
      console.error('Error eliminando paciente:', error);
      setError('Error al desactivar el paciente. Intenta de nuevo.');
    }
  };

  const handleFotoSuccess = (nuevaFotoUrl: string) => {
    if (paciente) {
      setPaciente({ ...paciente, foto_url: nuevaFotoUrl });
      setSuccessMessage('Foto actualizada exitosamente');
      setTimeout(() => setSuccessMessage(''), 3000);
    }
  };

  const handleFotoError = (error: string) => {
    setError(error);
    setTimeout(() => setError(''), 5000);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando paciente...</p>
        </div>
      </div>
    );
  }

  if (error && !paciente) {
    return (
      <div className="max-w-2xl mx-auto mt-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
          <svg
            className="mx-auto h-12 w-12 text-red-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <h3 className="mt-4 text-lg font-medium text-red-800">{error}</h3>
          <button
            onClick={() => router.back()}
            className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700"
          >
            Volver
          </button>
        </div>
      </div>
    );
  }

  if (!paciente) return null;

  const edad = calcularEdad(paciente.fecha_nacimiento);

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <button
            onClick={() => router.back()}
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
              {paciente.nombres} {paciente.apellidos}
            </h1>
            <p className="text-gray-600 mt-1">
              {edad} años • {paciente.genero} • DPI: {formatearDPI(paciente.dpi)}
            </p>
          </div>
          {!paciente.activo && (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-100 text-red-800">
              Inactivo
            </span>
          )}
        </div>

        {!isEditing && (
          <div className="flex space-x-3">
            <button
              onClick={() => router.push(`/dashboard/pacientes/${pacienteId}/archivos`)}
              className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 transition-colors"
            >
              <svg className="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21h10a2 2 0 002-2V9.414a1 1 0 00-.293-.707l-5.414-5.414A1 1 0 0012.586 3H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
              </svg>
              Archivos
            </button>
            <button
              onClick={() => setIsEditing(true)}
              className="inline-flex items-center px-4 py-2 border border-purple-300 rounded-lg text-sm font-medium text-purple-700 bg-white hover:bg-purple-50 transition-colors"
            >
              <svg className="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
              Editar
            </button>
            {paciente.activo && (
              <button
                onClick={handleDelete}
                className="inline-flex items-center px-4 py-2 border border-red-300 rounded-lg text-sm font-medium text-red-700 bg-white hover:bg-red-50 transition-colors"
              >
                <svg className="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
                Desactivar
              </button>
            )}
          </div>
        )}
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
            <svg className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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

      {/* Contenido */}
      {isEditing ? (
        /* MODO EDICIÓN */
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div className="mb-6">
            <h2 className="text-lg font-semibold text-gray-900">Editar Información del Paciente</h2>
            <p className="text-sm text-gray-600 mt-1">Actualiza los datos del paciente</p>
          </div>
          <PacienteForm
            paciente={paciente}
            onSubmit={handleUpdate}
            onCancel={() => {
              setIsEditing(false);
              setError('');
            }}
            isLoading={saving}
          />
        </div>
      ) : (
        /* MODO VISUALIZACIÓN */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Columna Principal */}
          <div className="lg:col-span-2 space-y-6">
            {/* Datos Personales */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                👤 Datos Personales
              </h2>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Nombres</dt>
                  <dd className="mt-1 text-sm text-gray-900">{paciente.nombres}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Apellidos</dt>
                  <dd className="mt-1 text-sm text-gray-900">{paciente.apellidos}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">DPI</dt>
                  <dd className="mt-1 text-sm text-gray-900">{formatearDPI(paciente.dpi)}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Fecha de Nacimiento</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {new Date(paciente.fecha_nacimiento).toLocaleDateString('es-GT')} ({edad} años)
                  </dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Género</dt>
                  <dd className="mt-1 text-sm text-gray-900">{paciente.genero}</dd>
                </div>
                {paciente.tipo_sangre && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Tipo de Sangre</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.tipo_sangre}</dd>
                  </div>
                )}
                {paciente.estado_civil && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Estado Civil</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.estado_civil}</dd>
                  </div>
                )}
                {paciente.religion && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Religión</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.religion}</dd>
                  </div>
                )}
                {paciente.ocupacion && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Ocupación</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.ocupacion}</dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Contacto */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                📞 Información de Contacto
              </h2>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Teléfono Principal</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {formatearTelefono(paciente.telefono_principal)}
                  </dd>
                </div>
                {paciente.telefono_secundario && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Teléfono Secundario</dt>
                    <dd className="mt-1 text-sm text-gray-900">
                      {formatearTelefono(paciente.telefono_secundario)}
                    </dd>
                  </div>
                )}
                {paciente.email && (
                  <div className="md:col-span-2">
                    <dt className="text-sm font-medium text-gray-500">Email</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.email}</dd>
                  </div>
                )}
                <div className="md:col-span-2">
                  <dt className="text-sm font-medium text-gray-500">Dirección</dt>
                  <dd className="mt-1 text-sm text-gray-900">{paciente.direccion}</dd>
                </div>
                {paciente.municipio && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Municipio</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.municipio}</dd>
                  </div>
                )}
                {paciente.departamento && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Departamento</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.departamento}</dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Seguro Médico */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                🏥 Seguro Médico
              </h2>
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  {paciente.tiene_igss ? (
                    <>
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                        ✓ IGSS
                      </span>
                      {paciente.numero_igss && (
                        <span className="text-sm text-gray-600">
                          No. {paciente.numero_igss}
                        </span>
                      )}
                    </>
                  ) : (
                    <span className="text-sm text-gray-500">Sin IGSS</span>
                  )}
                </div>
                <div className="flex items-center space-x-3">
                  {paciente.tiene_seguro_privado ? (
                    <>
                      <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-purple-100 text-purple-800">
                        ✓ Seguro Privado
                      </span>
                      {paciente.nombre_seguro && (
                        <span className="text-sm text-gray-600">
                          {paciente.nombre_seguro}
                        </span>
                      )}
                    </>
                  ) : (
                    <span className="text-sm text-gray-500">Sin Seguro Privado</span>
                  )}
                </div>
              </div>
            </div>

            {/* Contacto de Emergencia */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                🚨 Contacto de Emergencia
              </h2>
              <dl className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <dt className="text-sm font-medium text-gray-500">Nombre</dt>
                  <dd className="mt-1 text-sm text-gray-900">{paciente.emergencia_nombre}</dd>
                </div>
                <div>
                  <dt className="text-sm font-medium text-gray-500">Teléfono</dt>
                  <dd className="mt-1 text-sm text-gray-900">
                    {formatearTelefono(paciente.emergencia_telefono)}
                  </dd>
                </div>
                {paciente.emergencia_parentesco && (
                  <div>
                    <dt className="text-sm font-medium text-gray-500">Parentesco</dt>
                    <dd className="mt-1 text-sm text-gray-900">{paciente.emergencia_parentesco}</dd>
                  </div>
                )}
              </dl>
            </div>

            {/* Observaciones */}
            {paciente.observaciones && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                <h2 className="text-lg font-semibold text-gray-900 mb-4">
                  📝 Observaciones
                </h2>
                <p className="text-sm text-gray-700 whitespace-pre-wrap">
                  {paciente.observaciones}
                </p>
              </div>
            )}
          </div>

          {/* Columna Lateral */}
          <div className="space-y-6">
            {/* Foto del Paciente */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                📷 Foto del Paciente
              </h2>
              <SubirFoto
                pacienteId={pacienteId}
                fotoActual={paciente.foto_url}
                onSuccess={handleFotoSuccess}
                onError={handleFotoError}
              />
            </div>

            {/* Acciones Rápidas */}
            <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                ⚡ Acciones Rápidas
              </h2>
              <div className="space-y-3">
                <button
                  onClick={() => router.push(`/dashboard/consultas/nueva?paciente=${pacienteId}`)}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-purple-50 hover:border-purple-300 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">📋</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Nueva Consulta</p>
                      <p className="text-xs text-gray-500">Registrar atención médica</p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => router.push(`/dashboard/citas/nueva?paciente=${pacienteId}`)}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-purple-50 hover:border-purple-300 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">📅</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Agendar Cita</p>
                      <p className="text-xs text-gray-500">Programar próxima visita</p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => router.push(`/dashboard/recetas/nueva?paciente=${pacienteId}`)}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-purple-50 hover:border-purple-300 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">💊</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Nueva Receta</p>
                      <p className="text-xs text-gray-500">Prescribir medicamentos</p>
                    </div>
                  </div>
                </button>

                <button
                  onClick={() => router.push(`/dashboard/pacientes/${pacienteId}/archivos`)}
                  className="w-full text-left px-4 py-3 border border-gray-200 rounded-lg hover:bg-purple-50 hover:border-purple-300 transition-colors"
                >
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl">📁</span>
                    <div>
                      <p className="text-sm font-medium text-gray-900">Ver Archivos</p>
                      <p className="text-xs text-gray-500">Laboratorios, imágenes, etc.</p>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            {/* Información del Sistema */}
            <div className="bg-gray-50 rounded-xl border border-gray-200 p-6">
              <h2 className="text-sm font-semibold text-gray-700 mb-3">
                ℹ️ Información del Sistema
              </h2>
              <dl className="space-y-2">
                <div>
                  <dt className="text-xs text-gray-500">ID del Paciente</dt>
                  <dd className="text-xs font-mono text-gray-900">#{paciente.id}</dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Fecha de Registro</dt>
                  <dd className="text-xs text-gray-900">
                    {new Date(paciente.created_at).toLocaleString('es-GT')}
                  </dd>
                </div>
                <div>
                  <dt className="text-xs text-gray-500">Estado</dt>
                  <dd className="text-xs">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                      paciente.activo 
                        ? 'bg-green-100 text-green-800' 
                        : 'bg-red-100 text-red-800'
                    }`}>
                      {paciente.activo ? 'Activo' : 'Inactivo'}
                    </span>
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}