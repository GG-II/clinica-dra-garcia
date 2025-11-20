// components/pacientes/BuscarPaciente.tsx
'use client';

import { useState, useEffect } from 'react';

interface BuscarPacienteProps {
  onBuscar: (query: string) => void | Promise<void>;
  placeholder?: string;
  delay?: number; // Milisegundos de delay para evitar muchas búsquedas
}

export default function BuscarPaciente({
  onBuscar,
  placeholder = 'Buscar por nombre, apellido o DPI...',
  delay = 500,
}: BuscarPacienteProps) {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);

  // Debounce: esperar a que el usuario termine de escribir
  useEffect(() => {
    if (query.length === 0) {
      onBuscar('');
      setIsSearching(false);
      return;
    }

    setIsSearching(true);
    const timeoutId = setTimeout(() => {
      onBuscar(query);
      setIsSearching(false);
    }, delay);

    return () => clearTimeout(timeoutId);
  }, [query, onBuscar, delay]);

  const handleClear = () => {
    setQuery('');
    onBuscar('');
  };

  return (
    <div className="relative">
      {/* Ícono de búsqueda */}
      <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
        <svg
          className={`h-5 w-5 ${isSearching ? 'text-purple-500 animate-pulse' : 'text-gray-400'}`}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={2}
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
      </div>

      {/* Input de búsqueda */}
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder}
        className="w-full pl-12 pr-12 py-3.5 border border-gray-300 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all text-gray-900 placeholder-gray-400 shadow-sm hover:shadow-md"
      />

      {/* Botón limpiar */}
      {query.length > 0 && (
        <button
          onClick={handleClear}
          className="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 transition-colors"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      )}

      {/* Indicador de búsqueda activa */}
      {isSearching && (
        <div className="absolute -bottom-6 left-0 text-xs text-purple-600 animate-pulse">
          Buscando...
        </div>
      )}

      {/* Contador de caracteres (opcional) */}
      {query.length > 0 && !isSearching && (
        <div className="absolute -bottom-6 left-0 text-xs text-gray-500">
          {query.length} caracteres
        </div>
      )}
    </div>
  );
}