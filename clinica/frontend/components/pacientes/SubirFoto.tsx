// components/pacientes/SubirFoto.tsx
'use client';

import { useState, useRef } from 'react';
import { pacientesService, validarTipoFoto } from '@/lib/pacientes';
import Image from 'next/image';

interface SubirFotoProps {
  pacienteId: number;
  fotoActual?: string;
  onSuccess: (nuevaFotoUrl: string) => void;
  onError?: (error: string) => void;
}

export default function SubirFoto({
  pacienteId,
  fotoActual,
  onSuccess,
  onError,
}: SubirFotoProps) {
  const [uploading, setUploading] = useState(false);
  const [preview, setPreview] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // Validar tipo y tamaño
    const validacion = validarTipoFoto(file);
    if (!validacion.valido) {
      onError?.(validacion.error || 'Archivo no válido');
      return;
    }

    // Crear preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result as string);
    };
    reader.readAsDataURL(file);

    // Subir archivo
    setUploading(true);
    try {
      const resultado = await pacientesService.subirFoto(pacienteId, file);
      onSuccess(resultado.ruta_archivo);
      
      // Limpiar input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    } catch (error: any) {
      console.error('Error subiendo foto:', error);
      onError?.(
        error.response?.data?.detail || 'Error al subir la foto. Intenta de nuevo.'
      );
      setPreview(null);
    } finally {
      setUploading(false);
    }
  };

  const handleClick = () => {
    fileInputRef.current?.click();
  };

  const handleRemovePreview = () => {
    setPreview(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  const fotoUrl = preview || (fotoActual ? `http://localhost:8000/static/${fotoActual}` : null);

  return (
    <div className="space-y-4">
      {/* Preview de la foto */}
      <div className="flex items-center space-x-4">
        <div className="relative h-24 w-24 rounded-full overflow-hidden bg-gradient-to-br from-purple-100 to-purple-200 flex-shrink-0 border-4 border-white shadow-lg">
          {fotoUrl ? (
            <Image
              src={fotoUrl}
              alt="Preview"
              fill
              className="object-cover"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
              }}
            />
          ) : (
            <div className="h-full w-full flex items-center justify-center text-purple-500 text-4xl">
              📷
            </div>
          )}
        </div>

        <div className="flex-1">
          <p className="text-sm font-medium text-gray-700 mb-2">
            Foto del paciente
          </p>
          <p className="text-xs text-gray-500 mb-3">
            JPG o PNG, máximo 5 MB
          </p>

          {/* Botones */}
          <div className="flex space-x-2">
            <button
              type="button"
              onClick={handleClick}
              disabled={uploading}
              className="inline-flex items-center px-4 py-2 border border-purple-300 rounded-lg text-sm font-medium text-purple-700 bg-white hover:bg-purple-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {uploading ? (
                <>
                  <svg
                    className="animate-spin -ml-1 mr-2 h-4 w-4 text-purple-700"
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
                    className="-ml-1 mr-2 h-4 w-4"
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
                  {fotoActual || preview ? 'Cambiar foto' : 'Subir foto'}
                </>
              )}
            </button>

            {preview && (
              <button
                type="button"
                onClick={handleRemovePreview}
                className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 transition-colors"
              >
                <svg
                  className="h-4 w-4"
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
          </div>
        </div>
      </div>

      {/* Input oculto */}
      <input
        ref={fileInputRef}
        type="file"
        accept="image/jpeg,image/png,image/jpg"
        onChange={handleFileSelect}
        className="hidden"
      />

      {/* Indicador de subida exitosa */}
      {preview && !uploading && (
        <div className="flex items-center space-x-2 text-sm text-green-600 bg-green-50 px-3 py-2 rounded-lg">
          <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M5 13l4 4L19 7"
            />
          </svg>
          <span>Foto subida correctamente</span>
        </div>
      )}
    </div>
  );
}