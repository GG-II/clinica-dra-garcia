// components/pacientes/PacienteForm.tsx
'use client';

import { useState, useEffect } from 'react';
import {
  Paciente,
  PacienteCreate,
  PacienteUpdate,
  GeneroEnum,
  EstadoCivilEnum,
  TipoSangreEnum,
} from '@/types/paciente';
import { validarDPI, validarTelefono, validarFechaNacimiento } from '@/lib/pacientes';

interface PacienteFormProps {
  paciente?: Paciente;
  onSubmit: (data: PacienteCreate | PacienteUpdate) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

export default function PacienteForm({
  paciente,
  onSubmit,
  onCancel,
  isLoading = false,
}: PacienteFormProps) {
  const [activeTab, setActiveTab] = useState<'personal' | 'contacto' | 'seguro' | 'emergencia'>(
    'personal'
  );
  const [errors, setErrors] = useState<Record<string, string>>({});

  // Estado del formulario
  const [formData, setFormData] = useState({
    // Personal
    nombres: paciente?.nombres || '',
    apellidos: paciente?.apellidos || '',
    fecha_nacimiento: paciente?.fecha_nacimiento || '',
    genero: paciente?.genero || GeneroEnum.MASCULINO,
    dpi: paciente?.dpi || '',
    tipo_sangre: paciente?.tipo_sangre || undefined,
    estado_civil: paciente?.estado_civil || undefined,
    religion: paciente?.religion || '',
    ocupacion: paciente?.ocupacion || '',

    // Contacto
    telefono_principal: paciente?.telefono_principal || '',
    telefono_secundario: paciente?.telefono_secundario || '',
    email: paciente?.email || '',
    direccion: paciente?.direccion || '',
    municipio: paciente?.municipio || '',
    departamento: paciente?.departamento || '',

    // Seguro
    tiene_igss: paciente?.tiene_igss || false,
    numero_igss: paciente?.numero_igss || '',
    tiene_seguro_privado: paciente?.tiene_seguro_privado || false,
    nombre_seguro: paciente?.nombre_seguro || '',

    // Emergencia
    emergencia_nombre: paciente?.emergencia_nombre || '',
    emergencia_telefono: paciente?.emergencia_telefono || '',
    emergencia_parentesco: paciente?.emergencia_parentesco || '',

    // Observaciones
    observaciones: paciente?.observaciones || '',
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value, type } = e.target;

    if (type === 'checkbox') {
      const checked = (e.target as HTMLInputElement).checked;
      setFormData((prev) => ({ ...prev, [name]: checked }));
    } else {
      setFormData((prev) => ({ ...prev, [name]: value }));
    }

    // Limpiar error del campo
    if (errors[name]) {
      setErrors((prev) => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
  };

  const validarFormulario = (): boolean => {
    const newErrors: Record<string, string> = {};

    // Validaciones de Personal
    if (!formData.nombres.trim()) {
      newErrors.nombres = 'Los nombres son requeridos';
    }
    if (!formData.apellidos.trim()) {
      newErrors.apellidos = 'Los apellidos son requeridos';
    }
    if (!formData.fecha_nacimiento) {
      newErrors.fecha_nacimiento = 'La fecha de nacimiento es requerida';
    } else {
      const validacionFecha = validarFechaNacimiento(formData.fecha_nacimiento);
      if (!validacionFecha.valido) {
        newErrors.fecha_nacimiento = validacionFecha.error!;
      }
    }
    if (!formData.dpi.trim()) {
      newErrors.dpi = 'El DPI es requerido';
    } else {
      const validacionDPI = validarDPI(formData.dpi);
      if (!validacionDPI.valido) {
        newErrors.dpi = validacionDPI.error!;
      }
    }

    // Validaciones de Contacto
    if (!formData.telefono_principal.trim()) {
      newErrors.telefono_principal = 'El teléfono principal es requerido';
    } else {
      const validacionTel = validarTelefono(formData.telefono_principal);
      if (!validacionTel.valido) {
        newErrors.telefono_principal = validacionTel.error!;
      }
    }

    if (formData.telefono_secundario.trim()) {
      const validacionTel = validarTelefono(formData.telefono_secundario);
      if (!validacionTel.valido) {
        newErrors.telefono_secundario = validacionTel.error!;
      }
    }

    if (!formData.direccion.trim()) {
      newErrors.direccion = 'La dirección es requerida';
    }

    // Validaciones de Emergencia
    if (!formData.emergencia_nombre.trim()) {
      newErrors.emergencia_nombre = 'El nombre del contacto de emergencia es requerido';
    }
    if (!formData.emergencia_telefono.trim()) {
      newErrors.emergencia_telefono = 'El teléfono de emergencia es requerido';
    } else {
      const validacionTel = validarTelefono(formData.emergencia_telefono);
      if (!validacionTel.valido) {
        newErrors.emergencia_telefono = validacionTel.error!;
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!validarFormulario()) {
      // Cambiar a la primera pestaña con errores
      if (errors.nombres || errors.apellidos || errors.dpi || errors.fecha_nacimiento) {
        setActiveTab('personal');
      } else if (errors.telefono_principal || errors.direccion) {
        setActiveTab('contacto');
      } else if (errors.emergencia_nombre || errors.emergencia_telefono) {
        setActiveTab('emergencia');
      }
      return;
    }

    // Limpiar campos opcionales vacíos
    const dataToSubmit: any = { ...formData };
    Object.keys(dataToSubmit).forEach((key) => {
      if (dataToSubmit[key] === '' || dataToSubmit[key] === undefined) {
        if (key !== 'tiene_igss' && key !== 'tiene_seguro_privado') {
          dataToSubmit[key] = undefined;
        }
      }
    });

    await onSubmit(dataToSubmit);
  };

  const tabs = [
    { id: 'personal', label: 'Datos Personales', icon: '👤' },
    { id: 'contacto', label: 'Contacto', icon: '📞' },
    { id: 'seguro', label: 'Seguro Médico', icon: '🏥' },
    { id: 'emergencia', label: 'Emergencia', icon: '🚨' },
  ];

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {/* Tabs */}
      <div className="border-b border-gray-200">
        <nav className="-mb-px flex space-x-4" aria-label="Tabs">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id as any)}
              className={`
                flex items-center space-x-2 py-3 px-4 border-b-2 font-medium text-sm transition-colors
                ${
                  activeTab === tab.id
                    ? 'border-purple-500 text-purple-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }
              `}
            >
              <span className="text-lg">{tab.icon}</span>
              <span>{tab.label}</span>
              {/* Indicador de errores */}
              {tab.id === 'personal' &&
                (errors.nombres || errors.apellidos || errors.dpi || errors.fecha_nacimiento) && (
                  <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full">
                    !
                  </span>
                )}
              {tab.id === 'contacto' &&
                (errors.telefono_principal || errors.direccion) && (
                  <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full">
                    !
                  </span>
                )}
              {tab.id === 'emergencia' &&
                (errors.emergencia_nombre || errors.emergencia_telefono) && (
                  <span className="inline-flex items-center justify-center w-5 h-5 text-xs font-bold text-white bg-red-500 rounded-full">
                    !
                  </span>
                )}
            </button>
          ))}
        </nav>
      </div>

      {/* Contenido de Tabs */}
      <div className="bg-white rounded-lg p-6 shadow-sm border border-gray-200">
        {/* TAB: Datos Personales */}
        {activeTab === 'personal' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Nombres */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nombres <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="nombres"
                value={formData.nombres}
                onChange={handleChange}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.nombres ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ej: Juan Carlos"
              />
              {errors.nombres && (
                <p className="mt-1 text-sm text-red-600">{errors.nombres}</p>
              )}
            </div>

            {/* Apellidos */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Apellidos <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="apellidos"
                value={formData.apellidos}
                onChange={handleChange}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.apellidos ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ej: López García"
              />
              {errors.apellidos && (
                <p className="mt-1 text-sm text-red-600">{errors.apellidos}</p>
              )}
            </div>

            {/* Fecha de Nacimiento */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Fecha de Nacimiento <span className="text-red-500">*</span>
              </label>
              <input
                type="date"
                name="fecha_nacimiento"
                value={formData.fecha_nacimiento}
                onChange={handleChange}
                max={new Date().toISOString().split('T')[0]}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.fecha_nacimiento ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.fecha_nacimiento && (
                <p className="mt-1 text-sm text-red-600">{errors.fecha_nacimiento}</p>
              )}
            </div>

            {/* Género */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Género <span className="text-red-500">*</span>
              </label>
              <select
                name="genero"
                value={formData.genero}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value={GeneroEnum.MASCULINO}>Masculino</option>
                <option value={GeneroEnum.FEMENINO}>Femenino</option>
                <option value={GeneroEnum.OTRO}>Otro</option>
              </select>
            </div>

            {/* DPI */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                DPI <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="dpi"
                value={formData.dpi}
                onChange={handleChange}
                maxLength={13}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.dpi ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="1234567890123"
              />
              {errors.dpi && <p className="mt-1 text-sm text-red-600">{errors.dpi}</p>}
              <p className="mt-1 text-xs text-gray-500">13 dígitos sin espacios</p>
            </div>

            {/* Tipo de Sangre */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tipo de Sangre
              </label>
              <select
                name="tipo_sangre"
                value={formData.tipo_sangre || ''}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Seleccionar...</option>
                <option value={TipoSangreEnum.A_POSITIVO}>A+</option>
                <option value={TipoSangreEnum.A_NEGATIVO}>A-</option>
                <option value={TipoSangreEnum.B_POSITIVO}>B+</option>
                <option value={TipoSangreEnum.B_NEGATIVO}>B-</option>
                <option value={TipoSangreEnum.AB_POSITIVO}>AB+</option>
                <option value={TipoSangreEnum.AB_NEGATIVO}>AB-</option>
                <option value={TipoSangreEnum.O_POSITIVO}>O+</option>
                <option value={TipoSangreEnum.O_NEGATIVO}>O-</option>
              </select>
            </div>

            {/* Estado Civil */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Estado Civil
              </label>
              <select
                name="estado_civil"
                value={formData.estado_civil || ''}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              >
                <option value="">Seleccionar...</option>
                <option value={EstadoCivilEnum.SOLTERO}>Soltero/a</option>
                <option value={EstadoCivilEnum.CASADO}>Casado/a</option>
                <option value={EstadoCivilEnum.DIVORCIADO}>Divorciado/a</option>
                <option value={EstadoCivilEnum.VIUDO}>Viudo/a</option>
                <option value={EstadoCivilEnum.UNION_LIBRE}>Unión Libre</option>
              </select>
            </div>

            {/* Religión */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Religión</label>
              <input
                type="text"
                name="religion"
                value={formData.religion}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Ej: Católica"
              />
            </div>

            {/* Ocupación */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Ocupación</label>
              <input
                type="text"
                name="ocupacion"
                value={formData.ocupacion}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Ej: Profesor"
              />
            </div>

            {/* Observaciones */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Observaciones
              </label>
              <textarea
                name="observaciones"
                value={formData.observaciones}
                onChange={handleChange}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Notas adicionales sobre el paciente..."
              />
            </div>
          </div>
        )}

        {/* TAB: Contacto */}
        {activeTab === 'contacto' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Teléfono Principal */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Teléfono Principal <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="telefono_principal"
                value={formData.telefono_principal}
                onChange={handleChange}
                maxLength={8}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.telefono_principal ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="12345678"
              />
              {errors.telefono_principal && (
                <p className="mt-1 text-sm text-red-600">{errors.telefono_principal}</p>
              )}
              <p className="mt-1 text-xs text-gray-500">8 dígitos sin guiones</p>
            </div>

            {/* Teléfono Secundario */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Teléfono Secundario
              </label>
              <input
                type="text"
                name="telefono_secundario"
                value={formData.telefono_secundario}
                onChange={handleChange}
                maxLength={8}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.telefono_secundario ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="87654321"
              />
              {errors.telefono_secundario && (
                <p className="mt-1 text-sm text-red-600">{errors.telefono_secundario}</p>
              )}
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="correo@ejemplo.com"
              />
            </div>

            {/* Departamento */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Departamento
              </label>
              <input
                type="text"
                name="departamento"
                value={formData.departamento}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Ej: Huehuetenango"
              />
            </div>

            {/* Municipio */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Municipio</label>
              <input
                type="text"
                name="municipio"
                value={formData.municipio}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Ej: Huehuetenango"
              />
            </div>

            {/* Dirección */}
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dirección Completa <span className="text-red-500">*</span>
              </label>
              <textarea
                name="direccion"
                value={formData.direccion}
                onChange={handleChange}
                rows={3}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.direccion ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ej: 4ta calle 5-20 zona 1"
              />
              {errors.direccion && (
                <p className="mt-1 text-sm text-red-600">{errors.direccion}</p>
              )}
            </div>
          </div>
        )}

        {/* TAB: Seguro Médico */}
        {activeTab === 'seguro' && (
          <div className="space-y-6">
            {/* IGSS */}
            <div className="bg-blue-50 p-6 rounded-lg border border-blue-200">
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  name="tiene_igss"
                  checked={formData.tiene_igss}
                  onChange={handleChange}
                  className="mt-1 h-5 w-5 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                />
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-900 mb-1">
                    ¿Tiene seguro IGSS?
                  </label>
                  <p className="text-xs text-gray-600 mb-3">
                    Instituto Guatemalteco de Seguridad Social
                  </p>

                  {formData.tiene_igss && (
                    <input
                      type="text"
                      name="numero_igss"
                      value={formData.numero_igss}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-blue-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white"
                      placeholder="Número de afiliación IGSS"
                    />
                  )}
                </div>
              </div>
            </div>

            {/* Seguro Privado */}
            <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  name="tiene_seguro_privado"
                  checked={formData.tiene_seguro_privado}
                  onChange={handleChange}
                  className="mt-1 h-5 w-5 text-purple-600 focus:ring-purple-500 border-gray-300 rounded"
                />
                <div className="flex-1">
                  <label className="block text-sm font-medium text-gray-900 mb-1">
                    ¿Tiene seguro médico privado?
                  </label>
                  <p className="text-xs text-gray-600 mb-3">
                    Ej: Seguros G&T, El Roble, etc.
                  </p>

                  {formData.tiene_seguro_privado && (
                    <input
                      type="text"
                      name="nombre_seguro"
                      value={formData.nombre_seguro}
                      onChange={handleChange}
                      className="w-full px-4 py-2 border border-purple-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white"
                      placeholder="Nombre del seguro"
                    />
                  )}
                </div>
              </div>
            </div>

            {!formData.tiene_igss && !formData.tiene_seguro_privado && (
              <div className="text-center py-8 text-gray-500">
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
                <p className="mt-2 text-sm">Sin seguro médico</p>
              </div>
            )}
          </div>
        )}

        {/* TAB: Contacto de Emergencia */}
        {activeTab === 'emergencia' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="md:col-span-2 bg-red-50 p-4 rounded-lg border border-red-200">
              <div className="flex items-center space-x-2 text-red-800">
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
                  />
                </svg>
                <span className="text-sm font-medium">
                  Persona a contactar en caso de emergencia
                </span>
              </div>
            </div>

            {/* Nombre */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nombre Completo <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="emergencia_nombre"
                value={formData.emergencia_nombre}
                onChange={handleChange}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.emergencia_nombre ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="Ej: María López"
              />
              {errors.emergencia_nombre && (
                <p className="mt-1 text-sm text-red-600">{errors.emergencia_nombre}</p>
              )}
            </div>

            {/* Teléfono */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Teléfono <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                name="emergencia_telefono"
                value={formData.emergencia_telefono}
                onChange={handleChange}
                maxLength={8}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent ${
                  errors.emergencia_telefono ? 'border-red-500' : 'border-gray-300'
                }`}
                placeholder="12345678"
              />
              {errors.emergencia_telefono && (
                <p className="mt-1 text-sm text-red-600">{errors.emergencia_telefono}</p>
              )}
            </div>

            {/* Parentesco */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Parentesco
              </label>
              <input
                type="text"
                name="emergencia_parentesco"
                value={formData.emergencia_parentesco}
                onChange={handleChange}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                placeholder="Ej: Madre, Esposo, Hermano"
              />
            </div>
          </div>
        )}
      </div>

      {/* Botones de acción */}
      <div className="flex justify-end space-x-4 pt-6 border-t border-gray-200">
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="px-6 py-2.5 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Cancelar
        </button>
        <button
          type="submit"
          disabled={isLoading}
          className="px-6 py-2.5 border border-transparent rounded-lg text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-purple-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors inline-flex items-center"
        >
          {isLoading ? (
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
              Guardando...
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
                  d="M5 13l4 4L19 7"
                />
              </svg>
              {paciente ? 'Actualizar Paciente' : 'Crear Paciente'}
            </>
          )}
        </button>
      </div>
    </form>
  );
}