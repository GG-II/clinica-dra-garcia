'use client';

import PacienteForm from '@/components/pacientes/PacienteForm';

export default function NuevoPacientePage() {
  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-xl font-bold text-gray-900">Registrar Nuevo Paciente</h2>
        <p className="text-sm text-gray-500 mt-1">
          Complete la información del paciente. Los campos marcados con * son obligatorios.
        </p>
      </div>
      
      <PacienteForm />
    </div>
  );
}