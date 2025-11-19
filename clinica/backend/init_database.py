from sqlalchemy.orm import Session
from database import SessionLocal, engine
from passlib.context import CryptContext

# Importar desde create_simple_tables para evitar problemas
from create_simple_tables import Rol, Usuario, Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_db():
    """Inicializar la base de datos con datos básicos"""
    db = SessionLocal()
    
    try:
        print("🚀 Inicializando base de datos...")
        print("-" * 60)
        
        # Verificar si ya existen roles
        roles_count = db.query(Rol).count()
        if roles_count > 0:
            print("⚠️  La base de datos ya tiene datos. Saltando inicialización.")
            return
        
        # Crear roles
        print("📝 Creando roles...")
        roles = [
            Rol(nombre="Administrador", descripcion="Acceso completo al sistema"),
            Rol(nombre="Médico", descripcion="Acceso a funciones médicas"),
            Rol(nombre="Enfermera", descripcion="Acceso a enfermería y hospitalización"),
            Rol(nombre="Recepcionista", descripcion="Gestión de citas y caja")
        ]
        
        for rol in roles:
            db.add(rol)
        
        db.commit()
        print("✅ Roles creados")
        
        # Obtener rol de administrador
        rol_admin = db.query(Rol).filter(Rol.nombre == "Administrador").first()
        
        # Crear usuario administrador
        print("👤 Creando usuario administrador...")
        admin = Usuario(
            username="admin",
            email="admin@clinica.com",
            hashed_password=pwd_context.hash("admin123"),
            nombres="Administrador",
            apellidos="Sistema",
            rol_id=rol_admin.id,
            activo=True
        )
        
        db.add(admin)
        db.commit()
        print("✅ Usuario administrador creado")
        
        print("-" * 60)
        print("🎉 Base de datos inicializada correctamente!")
        print("\n📋 Credenciales de acceso:")
        print("  Usuario: admin")
        print("  Contraseña: admin123")
        print("\n⚠️  IMPORTANTE: Cambiar la contraseña en producción")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()