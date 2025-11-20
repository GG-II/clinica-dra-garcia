// components/pacientes/PacienteCard.tsx
'use client';

import { Paciente } from '@/types/paciente';
import { calcularEdad, formatearTelefono } from '@/types/paciente';
import Image from 'next/image';

interface PacienteCardProps {
  paciente: Paciente;
  onClick: () => void;
}

export default function PacienteCard({ paciente, onClick }: PacienteCardProps) {
  const edad = calcularEdad(paciente.fecha_nacimiento);

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md hover:border-purple-300 transition-all cursor-pointer group"
    >
      <div className="flex items-center space-x-4">
        {/* Foto del paciente */}
        <div className="relative h-16 w-16 rounded-full overflow-hidden bg-gradient-to-br from-purple-100 to-purple-200 flex-shrink-0">
          {paciente.foto_url ? (
            <Image
              src={`http://localhost:8000/static/${paciente.foto_url}`}
              alt={`${paciente.nombres} ${paciente.apellidos}`}
              fill
              className="object-cover"
              onError={(e) => {
                // Si falla la carga, mostrar ícono por defecto
                e.currentTarget.style.display = 'none';
              }}
            />
          ) : (
            <div className="h-full w-full flex items-center justify-center text-purple-500 text-2xl">
              {paciente.genero === 'Masculino' ? '👨' : '👩'}
            </div>
          )}
        </div>

        {/* Información del paciente */}
        <div className="flex-1 min-w-0">
          {/* Nombre */}
          <h3 className="font-semibold text-gray-900 text-lg truncate group-hover:text-purple-600 transition-colors">
            {paciente.nombres} {paciente.apellidos}
          </h3>

          {/* DPI */}
          <p className="text-sm text-gray-500 mt-0.5">
            DPI: {paciente.dpi}
          </p>

          {/* Info adicional */}
          <div className="flex items-center space-x-4 mt-2">
            <span className="inline-flex items-center text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
              <svg className="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {edad} años
            </span>

            <span className="inline-flex items-center text-xs text-gray-600 bg-gray-100 px-2 py-1 rounded">
              <svg className="w-3.5 h-3.5 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
              </svg>
              {formatearTelefono(paciente.telefono_principal)}
            </span>

            {paciente.tiene_igss && (
              <span className="inline-flex items-center text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded font-medium">
                IGSS
              </span>
            )}
          </div>
        </div>

        {/* Flecha indicadora */}
        <div className="flex-shrink-0">
          <svg
            className="w-6 h-6 text-gray-400 group-hover:text-purple-600 group-hover:translate-x-1 transition-all"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </div>
      </div>

      {/* Observaciones (si existen) */}
      {paciente.observaciones && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <p className="text-xs text-gray-600 italic line-clamp-2">
            📝 {paciente.observaciones}
          </p>
        </div>
      )}
    </div>
  );
}