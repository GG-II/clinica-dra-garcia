'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation'; // ⬅️ AGREGAR ESTA LÍNEA
import { authService } from '@/lib/auth';
import { Usuario } from '@/types';

export default function DashboardPage() {
  const router = useRouter(); // ⬅️ AGREGAR ESTA LÍNEA
  const [user, setUser] = useState<Usuario | null>(null);

  useEffect(() => {
    const userData = authService.getUser();
    setUser(userData);
  }, []);

  const stats = [
    {
      name: 'Pacientes Registrados',
      value: '0',
      icon: '👥',
      color: 'bg-blue-500',
    },
    {
      name: 'Citas Hoy',
      value: '0',
      icon: '📅',
      color: 'bg-green-500',
    },
    {
      name: 'Hospitalizados',
      value: '0',
      icon: '🏥',
      color: 'bg-purple-500',
    },
    {
      name: 'Usuarios Activos',
      value: '1',
      icon: '👤',
      color: 'bg-orange-500',
    },
  ];

  const modules = [
    {
      name: 'Pacientes',
      description: 'Gestión de pacientes y expedientes',
      icon: '👥',
      color: 'bg-blue-100 text-blue-600',
      available: true, // ⬅️ CAMBIAR A true
      href: '/dashboard/pacientes', // ⬅️ AGREGAR
    },
    {
      name: 'Historia Clínica',
      description: 'Consultas y antecedentes médicos',
      icon: '📋',
      color: 'bg-green-100 text-green-600',
      available: false,
      href: '/dashboard/historia-clinica', // ⬅️ AGREGAR
    },
    {
      name: 'Agenda',
      description: 'Programación de citas médicas',
      icon: '📅',
      color: 'bg-purple-100 text-purple-600',
      available: false,
      href: '/dashboard/agenda', // ⬅️ AGREGAR
    },
    {
      name: 'Recetas',
      description: 'Prescripción de medicamentos',
      icon: '💊',
      color: 'bg-pink-100 text-pink-600',
      available: false,
      href: '/dashboard/recetas', // ⬅️ AGREGAR
    },
    {
      name: 'Hospitalización',
      description: 'Gestión de camas y notas médicas',
      icon: '🏥',
      color: 'bg-red-100 text-red-600',
      available: false,
      href: '/dashboard/hospitalizacion', // ⬅️ AGREGAR
    },
    {
      name: 'Laboratorios',
      description: 'Resultados de estudios',
      icon: '🔬',
      color: 'bg-yellow-100 text-yellow-600',
      available: false,
      href: '/dashboard/laboratorios', // ⬅️ AGREGAR
    },
    {
      name: 'Farmacia',
      description: 'Inventario y dispensación',
      icon: '💉',
      color: 'bg-indigo-100 text-indigo-600',
      available: false,
      href: '/dashboard/farmacia', // ⬅️ AGREGAR
    },
    {
      name: 'Caja',
      description: 'Control financiero y facturación',
      icon: '💰',
      color: 'bg-teal-100 text-teal-600',
      available: false,
      href: '/dashboard/caja', // ⬅️ AGREGAR
    },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome */}
      <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-2xl shadow-lg p-8">
        <h2 className="text-3xl font-bold mb-2 text-white">
          ¡Bienvenido, {user?.nombres}! 👋
        </h2>
        <p className="text-purple-100">
          Sistema de Gestión Clínica - Sprint 2: Gestión de Pacientes
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white rounded-xl shadow-sm p-6 border border-gray-200"
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">{stat.name}</p>
                <p className="text-3xl font-bold text-gray-900 mt-1">
                  {stat.value}
                </p>
              </div>
              <div
                className={`${stat.color} h-12 w-12 rounded-lg flex items-center justify-center text-2xl`}
              >
                {stat.icon}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Sprint Progress */}
      <div className="bg-white rounded-xl shadow-sm p-6 border border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          📊 Progreso del Sprint 2
        </h3>
        <div className="space-y-3">
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Infraestructura Base</span>
              <span className="text-primary-600 font-medium">100%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-primary-600 h-2 rounded-full w-full"></div>
            </div>
          </div>
          <div>
            <div className="flex justify-between text-sm mb-1">
              <span className="text-gray-600">Gestión de Pacientes</span>
              <span className="text-purple-600 font-medium">En Progreso</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div className="bg-purple-600 h-2 rounded-full w-3/4"></div>
            </div>
          </div>
        </div>
      </div>

      {/* Modules */}
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          🚀 Módulos del Sistema
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {modules.map((module) => (
            <div
              key={module.name}
              onClick={() => module.available && module.href && router.push(module.href)}
              className={`bg-white rounded-xl shadow-sm p-6 border border-gray-200 ${
                module.available ? 'hover:shadow-md hover:border-purple-300 cursor-pointer' : 'opacity-50'
              } transition-all`}
            >
              <div
                className={`${module.color} h-12 w-12 rounded-lg flex items-center justify-center text-2xl mb-4`}
              >
                {module.icon}
              </div>
              <h4 className="font-semibold text-gray-900 mb-1">
                {module.name}
              </h4>
              <p className="text-sm text-gray-600 mb-2">{module.description}</p>
              {module.available ? (
                <span className="inline-block bg-green-100 text-green-800 text-xs px-2 py-1 rounded">
                  ✓ Disponible
                </span>
              ) : (
                <span className="inline-block bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded">
                  Próximamente
                </span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}