import os
from base_datos.db import conectar

def crear_tabla_empleados(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        cedula TEXT PRIMARY KEY,
        nombre TEXT NOT NULL,
        cargo TEXT NOT NULL,
        fecha_ingreso TEXT NOT NULL
    )
    """)
    print("✅ Tabla 'empleados' lista.")

def crear_tabla_usuarios(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        usuario TEXT PRIMARY KEY,
        clave TEXT NOT NULL,
        rol TEXT NOT NULL
    )
    """)
    print("✅ Tabla 'usuarios' lista.")

def crear_tabla_horarios(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horarios (
        cedula TEXT NOT NULL,
        fecha TEXT NOT NULL,
        hora_entrada TEXT,
        hora_salida TEXT,
        PRIMARY KEY (cedula, fecha)
    )
    """)
    print("✅ Tabla 'horarios' lista.")

def crear_tabla_historial(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historial (
        cedula TEXT,
        fecha TEXT,
        entrada TEXT,
        salida TEXT
    )
    """)
    print("✅ Tabla 'historial' lista.")

def crear_tabla_auditoria(cursor):
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
    print("✅ Tabla 'auditoria' lista.")

def inicializar_todo():
    conn = conectar()
    cursor = conn.cursor()

    crear_tabla_empleados(cursor)
    crear_tabla_usuarios(cursor)
    crear_tabla_horarios(cursor)
    crear_tabla_historial(cursor)
    crear_tabla_auditoria(cursor)

    conn.commit()
    conn.close()
    print("\n🎉 Base de datos inicializada correctamente.")

if __name__ == "__main__":
    inicializar_todo()