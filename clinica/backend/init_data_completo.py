from sqlalchemy.orm import Session
from database import SessionLocal
from create_simple_tables import (
    Medicamento, Cama, EstadoCamaEnum, TipoEstudio, CategoriaLaboratorioEnum
)
from datetime import datetime

def init_medicamentos():
    """Agregar medicamentos de ejemplo"""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay medicamentos
        if db.query(Medicamento).count() > 0:
            print("⚠️  Ya existen medicamentos en la base de datos")
            return
        
        print("💊 Creando medicamentos de ejemplo...")
        
        medicamentos = [
            # Analgésicos y Antiinflamatorios
            Medicamento(nombre_generico="Paracetamol", nombre_comercial="Tylenol", presentacion="Tableta", concentracion="500 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Ibuprofeno", nombre_comercial="Advil", presentacion="Tableta", concentracion="400 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Diclofenaco", nombre_comercial="Voltaren", presentacion="Tableta", concentracion="50 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Naproxeno", nombre_comercial="Naprosyn", presentacion="Tableta", concentracion="250 mg", via_administracion="Oral"),
            
            # Antibióticos
            Medicamento(nombre_generico="Amoxicilina", nombre_comercial="Amoxil", presentacion="Cápsula", concentracion="500 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Azitromicina", nombre_comercial="Zithromax", presentacion="Tableta", concentracion="500 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Ciprofloxacino", nombre_comercial="Cipro", presentacion="Tableta", concentracion="500 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Cefalexina", nombre_comercial="Keflex", presentacion="Cápsula", concentracion="500 mg", via_administracion="Oral"),
            
            # Antihipertensivos
            Medicamento(nombre_generico="Enalapril", nombre_comercial="Vasotec", presentacion="Tableta", concentracion="10 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Losartán", nombre_comercial="Cozaar", presentacion="Tableta", concentracion="50 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Amlodipino", nombre_comercial="Norvasc", presentacion="Tableta", concentracion="5 mg", via_administracion="Oral"),
            
            # Antidiabéticos
            Medicamento(nombre_generico="Metformina", nombre_comercial="Glucophage", presentacion="Tableta", concentracion="850 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Glibenclamida", nombre_comercial="Daonil", presentacion="Tableta", concentracion="5 mg", via_administracion="Oral"),
            
            # Antiácidos
            Medicamento(nombre_generico="Omeprazol", nombre_comercial="Prilosec", presentacion="Cápsula", concentracion="20 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Ranitidina", nombre_comercial="Zantac", presentacion="Tableta", concentracion="150 mg", via_administracion="Oral"),
            
            # Antihistamínicos
            Medicamento(nombre_generico="Loratadina", nombre_comercial="Claritin", presentacion="Tableta", concentracion="10 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Cetirizina", nombre_comercial="Zyrtec", presentacion="Tableta", concentracion="10 mg", via_administracion="Oral"),
            
            # Broncodilatadores
            Medicamento(nombre_generico="Salbutamol", nombre_comercial="Ventolin", presentacion="Inhalador", concentracion="100 mcg/dosis", via_administracion="Inhalatoria"),
            
            # Corticoides
            Medicamento(nombre_generico="Prednisona", nombre_comercial="", presentacion="Tableta", concentracion="5 mg", via_administracion="Oral"),
            Medicamento(nombre_generico="Dexametasona", nombre_comercial="", presentacion="Ampolla", concentracion="8 mg/2ml", via_administracion="Parenteral"),
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

def init_tipos_estudio():
    """Crear catálogo de tipos de estudios de laboratorio"""
    db = SessionLocal()
    
    try:
        # Verificar si ya hay tipos de estudio
        if db.query(TipoEstudio).count() > 0:
            print("⚠️  Ya existen tipos de estudio en la base de datos")
            return
        
        print("🔬 Creando catálogo de estudios de laboratorio...")
        
        estudios = [
            # Hematología
            TipoEstudio(nombre="Hemograma Completo", categoria=CategoriaLaboratorioEnum.hematologia),
            TipoEstudio(nombre="Velocidad de Sedimentación", categoria=CategoriaLaboratorioEnum.hematologia),
            TipoEstudio(nombre="Tiempo de Protrombina (TP)", categoria=CategoriaLaboratorioEnum.hematologia),
            TipoEstudio(nombre="Tiempo de Tromboplastina (TPT)", categoria=CategoriaLaboratorioEnum.hematologia),
            
            # Química Sanguínea
            TipoEstudio(nombre="Glucosa en Ayunas", categoria=CategoriaLaboratorioEnum.quimica),
            TipoEstudio(nombre="Creatinina", categoria=CategoriaLaboratorioEnum.quimica),
            TipoEstudio(nombre="Urea", categoria=CategoriaLaboratorioEnum.quimica),
            TipoEstudio(nombre="Ácido Úrico", categoria=CategoriaLaboratorioEnum.quimica),
            TipoEstudio(nombre="Electrolitos (Na, K, Cl)", categoria=CategoriaLaboratorioEnum.quimica),
            
            # Función Hepática
            TipoEstudio(nombre="Bilirrubina Total y Directa", categoria=CategoriaLaboratorioEnum.funcion_hepatica),
            TipoEstudio(nombre="TGO (AST)", categoria=CategoriaLaboratorioEnum.funcion_hepatica),
            TipoEstudio(nombre="TGP (ALT)", categoria=CategoriaLaboratorioEnum.funcion_hepatica),
            TipoEstudio(nombre="Fosfatasa Alcalina", categoria=CategoriaLaboratorioEnum.funcion_hepatica),
            
            # Perfil Lipídico
            TipoEstudio(nombre="Colesterol Total", categoria=CategoriaLaboratorioEnum.perfil_lipidico),
            TipoEstudio(nombre="HDL", categoria=CategoriaLaboratorioEnum.perfil_lipidico),
            TipoEstudio(nombre="LDL", categoria=CategoriaLaboratorioEnum.perfil_lipidico),
            TipoEstudio(nombre="Triglicéridos", categoria=CategoriaLaboratorioEnum.perfil_lipidico),
            
            # Tiroides
            TipoEstudio(nombre="TSH", categoria=CategoriaLaboratorioEnum.tiroides),
            TipoEstudio(nombre="T3", categoria=CategoriaLaboratorioEnum.tiroides),
            TipoEstudio(nombre="T4 Libre", categoria=CategoriaLaboratorioEnum.tiroides),
            
            # Diabetes
            TipoEstudio(nombre="Hemoglobina Glucosilada", categoria=CategoriaLaboratorioEnum.diabetes),
            TipoEstudio(nombre="Curva de Tolerancia a la Glucosa", categoria=CategoriaLaboratorioEnum.diabetes),
            
            # Orina y Heces
            TipoEstudio(nombre="Examen General de Orina", categoria=CategoriaLaboratorioEnum.orina_heces),
            TipoEstudio(nombre="Urocultivo", categoria=CategoriaLaboratorioEnum.orina_heces),
            TipoEstudio(nombre="Coproparasitoscópico", categoria=CategoriaLaboratorioEnum.orina_heces),
            
            # Inmunología
            TipoEstudio(nombre="VIH", categoria=CategoriaLaboratorioEnum.inmunologia),
            TipoEstudio(nombre="VDRL", categoria=CategoriaLaboratorioEnum.inmunologia),
            TipoEstudio(nombre="Hepatitis B", categoria=CategoriaLaboratorioEnum.inmunologia),
            TipoEstudio(nombre="Hepatitis C", categoria=CategoriaLaboratorioEnum.inmunologia),
            
            # Grupo Sanguíneo
            TipoEstudio(nombre="Grupo y Rh", categoria=CategoriaLaboratorioEnum.grupo_sanguineo),
            
            # Estudios de Imagen
            TipoEstudio(nombre="Radiografía de Tórax", categoria=CategoriaLaboratorioEnum.imagen),
            TipoEstudio(nombre="Ultrasonido Abdominal", categoria=CategoriaLaboratorioEnum.imagen),
            TipoEstudio(nombre="Electrocardiograma", categoria=CategoriaLaboratorioEnum.imagen),
        ]
        
        for estudio in estudios:
            db.add(estudio)
        
        db.commit()
        print(f"✅ {len(estudios)} tipos de estudio creados exitosamente")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 INICIALIZANDO DATOS COMPLETOS DEL SISTEMA CLÍNICO")
    print("=" * 80)
    print()
    
    init_medicamentos()
    print()
    
    init_camas()
    print()
    
    init_tipos_estudio()
    print()
    
    print("=" * 80)
    print("🎉 ¡INICIALIZACIÓN COMPLETA!")
    print("=" * 80)