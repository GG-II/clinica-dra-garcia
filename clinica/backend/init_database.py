"""
Script para inicializar la base de datos con datos iniciales
Ejecutar: python init_database.py
"""

from app.db.database import SessionLocal
from app.db.init_db import init_db

def main():
    db = SessionLocal()
    try:
        init_db(db)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()