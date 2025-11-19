from sqlalchemy.orm import Session
from database import SessionLocal
from create_simple_tables import Medicamento, Cama, EstadoCamaEnum
from datetime import datetime

def init_medicamentos():
    """Agregar medicamentos de ejemplo"""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay medicamentos
        if db.query(Medicamento).count() > 0:
            print("⚠️  Ya existen medicamentos en la base de datos")
            return
        
        print("📝 Creando medicamentos de ejemplo...")
        
        medicamentos = [
            # Analgésicos
            Medicamento(
                nombre_generico="Paracetamol",
                nombre_comercial="Tylenol",
                presentacion="Tableta",
                concentracion="500 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Ibuprofeno",
                nombre_comercial="Advil",
                presentacion="Tableta",
                concentracion="400 mg",
                via_administracion="Oral",
                contraindicaciones="Úlcera péptica, insuficiencia renal"
            ),
            Medicamento(
                nombre_generico="Diclofenaco",
                nombre_comercial="Voltaren",
                presentacion="Tableta",
                concentracion="50 mg",
                via_administracion="Oral"
            ),
            
            # Antibióticos
            Medicamento(
                nombre_generico="Amoxicilina",
                nombre_comercial="Amoxil",
                presentacion="Cápsula",
                concentracion="500 mg",
                via_administracion="Oral",
                contraindicaciones="Alergia a penicilinas"
            ),
            Medicamento(
                nombre_generico="Azitromicina",
                nombre_comercial="Zithromax",
                presentacion="Tableta",
                concentracion="500 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Ciprofloxacino",
                nombre_comercial="Cipro",
                presentacion="Tableta",
                concentracion="500 mg",
                via_administracion="Oral"
            ),
            
            # Antihipertensivos
            Medicamento(
                nombre_generico="Enalapril",
                nombre_comercial="Vasotec",
                presentacion="Tableta",
                concentracion="10 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Losartán",
                nombre_comercial="Cozaar",
                presentacion="Tableta",
                concentracion="50 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Amlodipino",
                nombre_comercial="Norvasc",
                presentacion="Tableta",
                concentracion="5 mg",
                via_administracion="Oral"
            ),
            
            # Antidiabéticos
            Medicamento(
                nombre_generico="Metformina",
                nombre_comercial="Glucophage",
                presentacion="Tableta",
                concentracion="850 mg",
                via_administracion="Oral",
                contraindicaciones="Insuficiencia renal severa"
            ),
            Medicamento(
                nombre_generico="Glibenclamida",
                nombre_comercial="Daonil",
                presentacion="Tableta",
                concentracion="5 mg",
                via_administracion="Oral"
            ),
            
            # Antiácidos
            Medicamento(
                nombre_generico="Omeprazol",
                nombre_comercial="Prilosec",
                presentacion="Cápsula",
                concentracion="20 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Ranitidina",
                nombre_comercial="Zantac",
                presentacion="Tableta",
                concentracion="150 mg",
                via_administracion="Oral"
            ),
            
            # Antihistamínicos
            Medicamento(
                nombre_generico="Loratadina",
                nombre_comercial="Claritin",
                presentacion="Tableta",
                concentracion="10 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Cetirizina",
                nombre_comercial="Zyrtec",
                presentacion="Tableta",
                concentracion="10 mg",
                via_administracion="Oral"
            ),
            
            # Vitaminas
            Medicamento(
                nombre_generico="Ácido Fólico",
                nombre_comercial="",
                presentacion="Tableta",
                concentracion="5 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Complejo B",
                nombre_comercial="Bedoyecta",
                presentacion="Cápsula",
                concentracion="",
                via_administracion="Oral"
            ),
            
            # Otros
            Medicamento(
                nombre_generico="Salbutamol",
                nombre_comercial="Ventolin",
                presentacion="Inhalador",
                concentracion="100 mcg/dosis",
                via_administracion="Inhalatoria"
            ),
            Medicamento(
                nombre_generico="Prednisona",
                nombre_comercial="",
                presentacion="Tableta",
                concentracion="5 mg",
                via_administracion="Oral"
            ),
            Medicamento(
                nombre_generico="Diazepam",
                nombre_comercial="Valium",
                presentacion="Tableta",
                concentracion="5 mg",
                via_administracion="Oral"
            ),
        ]
        
        for med in medicamentos:
            db.add(med)
        
        db.commit()
        print(f"✅ {len(medicamentos)} medicamentos creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

def init_camas():
    """Crear las 8 camas del hospital"""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay camas
        if db.query(Cama).count() > 0:
            print("⚠️  Ya existen camas en la base de datos")
            return
        
        print("🛏️  Creando las 8 camas...")
        
        for i in range(1, 9):
            cama = Cama(
                numero=i,
                estado=EstadoCamaEnum.disponible,
                ubicacion=f"Habitación {i}"
            )
            db.add(cama)
        
        db.commit()
        print("✅ 8 camas creadas exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Inicializando datos de ejemplo...")
    print("-" * 60)
    
    init_medicamentos()
    init_camas()
    
    print("-" * 60)
    print("🎉 Datos de ejemplo inicializados!")