from sqlalchemy.orm import Session
from app.models.usuario import Rol, Permiso, RolPermiso, Usuario
from app.core.security import get_password_hash

def init_roles(db: Session):
    """Crear los 4 roles del sistema"""
    roles_data = [
        {
            "nombre": "Administrador",
            "descripcion": "Acceso total al sistema"
        },
        {
            "nombre": "Médico",
            "descripcion": "Acceso a pacientes, historia clínica, agenda propia, recetas, hospitalización y laboratorios"
        },
        {
            "nombre": "Enfermera",
            "descripcion": "Acceso a pacientes, signos vitales, medicamentos, notas de enfermería y hospitalización"
        },
        {
            "nombre": "Recepcionista",
            "descripcion": "Acceso a agenda, citas, caja y datos básicos de pacientes"
        }
    ]
    
    for rol_data in roles_data:
        # Verificar si ya existe
        existing = db.query(Rol).filter(Rol.nombre == rol_data["nombre"]).first()
        if not existing:
            rol = Rol(**rol_data)
            db.add(rol)
            print(f"✅ Rol creado: {rol_data['nombre']}")
        else:
            print(f"⏭️  Rol ya existe: {rol_data['nombre']}")
    
    db.commit()

def init_permisos(db: Session):
    """Crear permisos básicos del sistema"""
    permisos_data = [
        # Pacientes
        {"nombre": "pacientes.ver", "descripcion": "Ver lista de pacientes", "modulo": "pacientes"},
        {"nombre": "pacientes.crear", "descripcion": "Crear nuevo paciente", "modulo": "pacientes"},
        {"nombre": "pacientes.editar", "descripcion": "Editar paciente", "modulo": "pacientes"},
        {"nombre": "pacientes.eliminar", "descripcion": "Eliminar paciente", "modulo": "pacientes"},
        
        # Historia Clínica
        {"nombre": "historia.ver", "descripcion": "Ver historia clínica", "modulo": "historia"},
        {"nombre": "historia.crear", "descripcion": "Crear consulta", "modulo": "historia"},
        {"nombre": "historia.editar", "descripcion": "Editar historia clínica", "modulo": "historia"},
        
        # Agenda
        {"nombre": "agenda.ver", "descripcion": "Ver agenda", "modulo": "agenda"},
        {"nombre": "agenda.crear", "descripcion": "Crear citas", "modulo": "agenda"},
        {"nombre": "agenda.editar", "descripcion": "Editar/cancelar citas", "modulo": "agenda"},
        
        # Usuarios
        {"nombre": "usuarios.ver", "descripcion": "Ver usuarios", "modulo": "usuarios"},
        {"nombre": "usuarios.crear", "descripcion": "Crear usuarios", "modulo": "usuarios"},
        {"nombre": "usuarios.editar", "descripcion": "Editar usuarios", "modulo": "usuarios"},
        {"nombre": "usuarios.eliminar", "descripcion": "Eliminar usuarios", "modulo": "usuarios"},
        
        # Configuración
        {"nombre": "config.ver", "descripcion": "Ver configuración", "modulo": "configuracion"},
        {"nombre": "config.editar", "descripcion": "Editar configuración", "modulo": "configuracion"},
    ]
    
    for permiso_data in permisos_data:
        existing = db.query(Permiso).filter(Permiso.nombre == permiso_data["nombre"]).first()
        if not existing:
            permiso = Permiso(**permiso_data)
            db.add(permiso)
            print(f"✅ Permiso creado: {permiso_data['nombre']}")
        else:
            print(f"⏭️  Permiso ya existe: {permiso_data['nombre']}")
    
    db.commit()

def init_usuario_admin(db: Session):
    """Crear usuario administrador inicial"""
    # Verificar si ya existe un admin
    existing = db.query(Usuario).filter(Usuario.username == "admin").first()
    if existing:
        print("⏭️  Usuario admin ya existe")
        return
    
    # Obtener rol de Administrador
    rol_admin = db.query(Rol).filter(Rol.nombre == "Administrador").first()
    if not rol_admin:
        print("❌ Error: Rol Administrador no existe")
        return
    
    # Crear usuario admin
    admin = Usuario(
        username="admin",
        email="admin@clinica.com",
        password_hash=get_password_hash("admin123"),
        nombres="Administrador",
        apellidos="Sistema",
        rol_id=rol_admin.id,
        activo=True
    )
    
    db.add(admin)
    db.commit()
    
    print("✅ Usuario administrador creado")
    print("   Username: admin")
    print("   Password: admin123")

def init_db(db: Session):
    """Inicializar toda la base de datos"""
    print("\n🚀 Inicializando base de datos...\n")
    
    print("📋 Creando roles...")
    init_roles(db)
    
    print("\n🔐 Creando permisos...")
    init_permisos(db)
    
    print("\n👤 Creando usuario administrador...")
    init_usuario_admin(db)
    
    print("\n✅ Base de datos inicializada correctamente\n")