import sqlite3
import bcrypt
import os

# 📁 Ruta absoluta a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "asistencia_frensa.db")

def conectar():
    return sqlite3.connect(DB_PATH)

def crear_tablas_si_faltan():
    conn = conectar()
    cursor = conn.cursor()

    tablas_sql = {
        "usuarios": """
            CREATE TABLE IF NOT EXISTS usuarios (
                usuario TEXT PRIMARY KEY,
                clave TEXT NOT NULL,
                rol TEXT NOT NULL
            );
        """,
        "empleados": """
            CREATE TABLE IF NOT EXISTS empleados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT NOT NULL UNIQUE,
                nombre TEXT NOT NULL,
                cargo TEXT NOT NULL,
                fecha_ingreso TEXT NOT NULL
            );
        """,
        "horarios": """
            CREATE TABLE IF NOT EXISTS horarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora_entrada TEXT,
                hora_salida TEXT
            );
        """,
        "auditoria": """
            CREATE TABLE IF NOT EXISTS auditoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                accion TEXT NOT NULL,
                fecha TEXT NOT NULL,
                hora TEXT NOT NULL
            );
        """
    }

    for nombre, sql in tablas_sql.items():
        cursor.execute(sql)
        print(f"✅ Tabla '{nombre}' verificada o creada.")

    conn.commit()
    conn.close()

def insertar_usuarios_de_prueba():
    conn = conectar()
    cursor = conn.cursor()

    usuarios = [
        ("admin", "admin123", "admin"),
        ("soporte", "soporte123", "soporte")
    ]

    for usuario, clave_plana, rol in usuarios:
        cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
        if cursor.fetchone():
            print(f"ℹ️ Usuario '{usuario}' ya existe.")
            continue
        clave_hash = bcrypt.hashpw(clave_plana.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("INSERT INTO usuarios (usuario, clave, rol) VALUES (?, ?, ?)", (usuario, clave_hash, rol))
        print(f"✅ Usuario '{usuario}' creado.")

    conn.commit()
    conn.close()

def ejecutar_verificacion():
    print("\n🔧 INICIO DE VERIFICACIÓN AUTOMÁTICA\n")
    crear_tablas_si_faltan()
    insertar_usuarios_de_prueba()
    print(f"\n✅ VERIFICACIÓN COMPLETA EN:\n{DB_PATH}\n")

if __name__ == "__main__":
    ejecutar_verificacion()