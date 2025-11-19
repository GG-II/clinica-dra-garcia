from sqlalchemy import inspect
from database import engine

def check_tables():
    """Verificar qué tablas existen"""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    print("📋 Tablas en la base de datos:")
    for table in tables:
        print(f"  ✅ {table}")
        
    if "pacientes" in tables:
        print("\n✅ La tabla 'pacientes' existe!")
    else:
        print("\n❌ La tabla 'pacientes' NO existe")

if __name__ == "__main__":
    check_tables()