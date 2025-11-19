from database import engine, Base

# IMPORTANTE: Importar TODOS los modelos en el ORDEN CORRECTO
# Primero las tablas sin dependencias, luego las que dependen de otras

print("📦 Importando modelos...")

# 1. Tablas base (sin dependencias de otras tablas)
from app.models.usuario import Usuario, Rol
from app.models.medicamento import Medicamento

# 2. Paciente (depende solo de enums)
from app.models.paciente import Paciente

# 3. Tablas que dependen de paciente y/o usuario
from app.models.archivos_paciente import ArchivosPaciente
from app.models.cita import Cita
from app.models.antecedente import Antecedente
from app.models.consulta import Consulta

# 4. Tablas que dependen de consulta y medicamento
from app.models.receta import Receta, RecetaDetalle

# 5. Hospitalización (depende de usuario y paciente)
from app.models.hospitalizacion import Hospitalizacion, Cama

print("✅ Todos los modelos importados correctamente")

def create_all_tables():
    """Crear todas las tablas del sistema"""
    print("\n🚀 Creando TODAS las tablas del sistema clínico...")
    print("-" * 60)
    
    # Crear todas las tablas
    Base.metadata.create_all(bind=engine)
    
    print("✅ ¡Todas las tablas creadas exitosamente!")
    print("-" * 60)
    print("\n📋 Tablas creadas:")
    print("  ✅ roles")
    print("  ✅ usuarios")
    print("  ✅ medicamentos")
    print("  ✅ pacientes")
    print("  ✅ archivos_paciente")
    print("  ✅ citas")
    print("  ✅ antecedentes")
    print("  ✅ consultas")
    print("  ✅ recetas")
    print("  ✅ receta_detalle")
    print("  ✅ camas")
    print("  ✅ hospitalizaciones")
    print("\n🎉 Base de datos completa lista para usar!")

if __name__ == "__main__":
    create_all_tables()