'use client';

import { useState, useEffect, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { pacientesService } from '@/lib/pacientes';
import { Paciente, EstadisticasPacientes } from '@/types/paciente';
import PacienteCard from '@/components/pacientes/PacienteCard';
import BuscarPaciente from '@/components/pacientes/BuscarPaciente';

export default function PacientesPage() {
  const router = useRouter();
  const [pacientes, setPacientes] = useState<Paciente[]>([]);
  const [estadisticas, setEstadisticas] = useState<EstadisticasPacientes | null>(null);
  const [loading, setLoading] = useState(true);
  const [searching, setSearching] = useState(false);
  const [error, setError] = useState('');

  // useCallback para evitar re-crear la función en cada render
  const cargarDatos = useCallback(async () => {
    try {
      setLoading(true);
      setError('');
      const [pacientesData, estadisticasData] = await Promise.all([
        pacientesService.listar({ limit: 100 }),
        pacientesService.estadisticas(),
      ]);
      setPacientes(pacientesData);
      setEstadisticas(estadisticasData);
    } catch (error) {
      console.error('Error cargando datos:', error);
      setError('Error al cargar los pacientes. Intenta recargar la página.');
    } finally {
      setLoading(false);
    }
  }, []); // ← Sin dependencias, función estable

  // Cargar datos solo una vez al montar el componente
  useEffect(() => {
    cargarDatos();
  }, [cargarDatos]); // ← Ahora cargarDatos es estable gracias a useCallback

  // useCallback para handleBuscar también
  const handleBuscar = useCallback(async (query: string) => {
    if (query.length === 0) {
      cargarDatos();
      return;
    }

    try {
      setSearching(true);
      setError('');
      const resultados = await pacientesService.listar({ buscar: query, limit: 50 });
      setPacientes(resultados);
    } catch (error) {
      console.error('Error buscando pacientes:', error);
      setError('Error en la búsqueda. Intenta de nuevo.');
    } finally {
      setSearching(false);
    }
  }, [cargarDatos]); // ← Depende de cargarDatos (que es estable)

  const handleVerPaciente = useCallback((pacienteId: number) => {
    router.push(`/dashboard/pacientes/${pacienteId}`);
  }, [router]);

  const handleNuevoPaciente = useCallback(() => {
    router.push('/dashboard/pacientes/nuevo');
  }, [router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Cargando pacientes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Pacientes</h1>
          <p className="text-gray-600 mt-1">
            Gestión de expedientes médicos
          </p>
        </div>
        <button
          onClick={handleNuevoPaciente}
          className="inline-flex items-center px-4 py-2.5 border border-transparent rounded-lg text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 transition-colors shadow-sm hover:shadow-md"
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
              d="M12 4v16m8-8H4"
            />
          </svg>
          Nuevo Paciente
        </button>
      </div>

      {/* Estadísticas */}
      {estadisticas && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Pacientes</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {estadisticas.total_pacientes}
                </p>
              </div>
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center text-2xl">
                👥
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Activos</p>
                <p className="text-3xl font-bold text-green-600 mt-1">
                  {estadisticas.pacientes_activos}
                </p>
              </div>
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center text-2xl">
                ✅
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Nuevos Este Mes</p>
                <p className="text-3xl font-bold text-purple-600 mt-1">
                  {estadisticas.nuevos_este_mes}
                </p>
              </div>
              <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center text-2xl">
                ⭐
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Masculino / Femenino</p>
                <p className="text-xl font-bold text-gray-900 mt-1">
                  {estadisticas.por_genero['Masculino'] || 0} / {estadisticas.por_genero['Femenino'] || 0}
                </p>
              </div>
              <div className="h-12 w-12 bg-orange-100 rounded-lg flex items-center justify-center text-2xl">
                ⚥
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Buscador */}
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
        <BuscarPaciente
          onBuscar={handleBuscar}
          placeholder="Buscar por nombre, apellido o DPI..."
        />
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-center space-x-2 text-red-800">
            <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span className="text-sm font-medium">{error}</span>
          </div>
        </div>
      )}

      {/* Lista de Pacientes */}
      {searching ? (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600 mx-auto"></div>
            <p className="mt-2 text-sm text-gray-600">Buscando...</p>
          </div>
        </div>
      ) : pacientes.length === 0 ? (
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
                d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
              />
            </svg>
            <h3 className="mt-4 text-lg font-medium text-gray-900">
              No se encontraron pacientes
            </h3>
            <p className="mt-2 text-sm text-gray-500">
              Intenta con otros términos de búsqueda o crea un nuevo paciente.
            </p>
            <button
              onClick={handleNuevoPaciente}
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
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Crear Primer Paciente
            </button>
          </div>
        </div>
      ) : (
        <div>
          <div className="flex items-center justify-between mb-4">
            <p className="text-sm text-gray-600">
              Mostrando <span className="font-medium text-gray-900">{pacientes.length}</span>{' '}
              {pacientes.length === 1 ? 'paciente' : 'pacientes'}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {pacientes.map((paciente) => (
              <PacienteCard
                key={paciente.id}
                paciente={paciente}
                onClick={() => handleVerPaciente(paciente.id)}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}