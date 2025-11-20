from datetime import datetime
import shutil
import os
import sys
import sqlite3
import bcrypt

def obtener_ruta_db():
    if getattr(sys, 'frozen', False):
        # Ejecutable: usar la carpeta donde está el .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # Desarrollo: usar la carpeta actual
        base_path = os.path.abspath(os.getcwd())

    ruta_db = os.path.join(base_path, "base_datos", "asistencia_frensa.db")
    os.makedirs(os.path.dirname(ruta_db), exist_ok=True)
    return ruta_db

def conectar():
    ruta_db = obtener_ruta_db()
    if not os.path.exists(ruta_db):
        print("⚠️ Base de datos no encontrada. Creando nueva...")
        crear_base_de_datos(ruta_db)
    return sqlite3.connect(ruta_db)

def crear_base_de_datos(ruta_db):
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    # Crear tablas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            cargo TEXT NOT NULL,
            fecha_ingreso TEXT NOT NULL,
            dependencia TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS horarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora_entrada TEXT,
            hora_salida TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historial (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            fecha TEXT NOT NULL,
            entrada TEXT,
            salida TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cedula TEXT NOT NULL,
            fecha TEXT NOT NULL,
            campo TEXT NOT NULL,
            valor_anterior TEXT,
            valor_nuevo TEXT,
            usuario_editor TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            clave TEXT NOT NULL,
            rol TEXT NOT NULL CHECK(rol IN ('admin', 'soporte'))
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS licencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('temporal', 'permanente')),
            estado TEXT NOT NULL CHECK(estado IN ('disponible', 'activa', 'revocada')),
            fecha_activacion TEXT,
            fecha_expiracion TEXT
        )
    """)

    # Insertar usuarios iniciales
    usuarios = [
        ("admin", "admin123", "admin"),
        ("soporte", "soporte123", "soporte")
    ]
    for usuario, clave, rol in usuarios:
        clave_encriptada = bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt())
        try:
            cursor.execute(
                "INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)",
                (usuario, clave_encriptada, rol)
            )
        except sqlite3.IntegrityError:
            print(f"ℹ️ Usuario '{usuario}' ya existe.")

    # Insertar licencia de prueba
    cursor.execute("""
        INSERT OR IGNORE INTO licencia (codigo, tipo, estado)
        VALUES ('CELITA-PRUEBA-001', 'temporal', 'disponible')
    """)

    conn.commit()
    conn.close()
    print(f"✅ Base de datos creada exitosamente en:\n{ruta_db}")

def respaldar_base_de_datos():
    ruta_original = obtener_ruta_db()
    carpeta_respaldo = os.path.join(os.path.dirname(ruta_original), "respaldos")
    os.makedirs(carpeta_respaldo, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_respaldo = f"respaldo_{timestamp}.db"
    ruta_respaldo = os.path.join(carpeta_respaldo, nombre_respaldo)

    try:
        shutil.copy2(ruta_original, ruta_respaldo)
        print(f"🗂️ Respaldo creado: {ruta_respaldo}")
    except Exception as e:
        print(f"❌ Error al crear respaldo: {e}")
        
def limpiar_respaldos_antiguos(dias=7):
    ruta_original = obtener_ruta_db()
    carpeta_respaldo = os.path.join(os.path.dirname(ruta_original), "respaldos")

    if not os.path.exists(carpeta_respaldo):
        return

    ahora = datetime.now()
    eliminados = 0

    for archivo in os.listdir(carpeta_respaldo):
        ruta_archivo = os.path.join(carpeta_respaldo, archivo)
        if os.path.isfile(ruta_archivo) and archivo.startswith("respaldo_") and archivo.endswith(".db"):
            fecha_str = archivo.replace("respaldo_", "").replace(".db", "")
            try:
                fecha_archivo = datetime.strptime(fecha_str, "%Y-%m-%d_%H-%M-%S")
                diferencia = (ahora - fecha_archivo).days
                if diferencia > dias:
                    os.remove(ruta_archivo)
                    eliminados += 1
            except ValueError:
                continue  # Ignora archivos mal nombrados

    if eliminados > 0:
        print(f"🧹 Se eliminaron {eliminados} respaldos antiguos.")
