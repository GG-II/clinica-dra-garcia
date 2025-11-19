print("Probando imports...")

try:
    from database import Base, engine
    print("✅ database importado")
except Exception as e:
    print(f"❌ Error en database: {e}")

try:
    from app.models.usuario import Usuario, Rol
    print("✅ usuario importado")
except Exception as e:
    print(f"❌ Error en usuario: {e}")

try:
    from app.models.paciente import Paciente
    print("✅ paciente importado")
except Exception as e:
    print(f"❌ Error en paciente: {e}")

try:
    from app.models.cita import Cita
    print("✅ cita importado")
except Exception as e:
    print(f"❌ Error en cita: {e}")

print("\n✅ Todos los imports funcionan!")