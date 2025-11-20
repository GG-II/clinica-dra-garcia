'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { pacientesService } from '@/lib/services/pacientes.service';
import { Paciente } from '@/types';
import PacienteForm from '@/components/pacientes/PacienteForm';

export default function EditarPacientePage() {
  const params = useParams();
  const pacienteId = parseInt(params.id as string);
  const [paciente, setPaciente] = useState<Paciente | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPaciente();
  }, [pacienteId]);

  const loadPaciente = async () => {
    try {
      setLoading(true);
      const data = await pacientesService.getById(pacienteId);
      setPaciente(data);
    } catch (error) {
      console.error('Error al cargar paciente:', error);
    } finally {
      setLoading(false);
    }
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
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900">Editar Paciente</h2>
        <p className="text-sm text-gray-500 mt-1">
          {paciente.nombres} {paciente.apellidos}
        </p>
      </div>

      <PacienteForm paciente={paciente} isEdit={true} />
    </div>
  );
}