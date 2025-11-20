// app/dashboard/pacientes/nuevo/page.tsx
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { pacientesService } from '@/lib/pacientes';
import { PacienteCreate } from '@/types/paciente';
import PacienteForm from '@/components/pacientes/PacienteForm';

export default function NuevoPacientePage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (data: PacienteCreate) => {
    setLoading(true);
    setError('');

    try {
      const pacienteCreado = await pacientesService.crear(data);
      
      // Mostrar mensaje de éxito (opcional - puedes agregar toast notification)
      console.log('Paciente creado exitosamente:', pacienteCreado);
      
      // Redirigir a la página del paciente recién creado
      router.push(`/dashboard/pacientes/${pacienteCreado.id}`);
    } catch (error: any) {
      console.error('Error creando paciente:', error);
      
      // Manejar errores específicos
      if (error.response?.status === 400) {
        const detail = error.response?.data?.detail;
        if (detail?.includes('DPI')) {
          setError('Ya existe un paciente registrado con este DPI');
        } else {
          setError(detail || 'Error al crear el paciente. Verifica los datos.');
        }
      } else if (error.response?.status === 422) {
        setError('Datos inválidos. Revisa el formulario.');
      } else {
        setError('Error al crear el paciente. Intenta de nuevo.');
      }
      
      setLoading(false);
    }
  };

  const handleCancel = () => {
    router.back();
  };

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <button
          onClick={handleCancel}
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
          <h1 className="text-2xl font-bold text-gray-900">Nuevo Paciente</h1>
          <p className="text-gray-600 mt-1">
            Registrar un nuevo paciente en el sistema
          </p>
        </div>
      </div>

      {/* Mensaje de error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <div className="flex items-start space-x-3">
            <svg
              className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0"
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
            <div>
              <h3 className="text-sm font-medium text-red-800">
                Error al crear paciente
              </h3>
              <p className="mt-1 text-sm text-red-700">{error}</p>
            </div>
            <button
              onClick={() => setError('')}
              className="ml-auto flex-shrink-0 text-red-600 hover:text-red-800"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Instrucciones */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <div className="flex items-start space-x-3">
          <svg
            className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <div>
            <h3 className="text-sm font-medium text-blue-800">
              Información importante
            </h3>
            <div className="mt-2 text-sm text-blue-700">
              <ul className="list-disc list-inside space-y-1">
                <li>Los campos marcados con <span className="text-red-600">*</span> son obligatorios</li>
                <li>El DPI debe tener exactamente 13 dígitos</li>
                <li>Los teléfonos deben tener 8 dígitos</li>
                <li>Puedes subir la foto del paciente después de crearlo</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      {/* Formulario */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <PacienteForm
          onSubmit={handleSubmit}
          onCancel={handleCancel}
          isLoading={loading}
        />
      </div>
    </div>
  );
}