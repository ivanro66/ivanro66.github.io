from base_datos.db import conectar

def crear_tabla_empleados(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS empleados (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT UNIQUE NOT NULL,
        nombre TEXT NOT NULL,
        cargo TEXT NOT NULL,
        fecha_ingreso TEXT NOT NULL
    )
    """)
    print("✅ Tabla 'empleados' lista.")

def crear_tabla_usuarios(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario TEXT UNIQUE NOT NULL,
        clave TEXT NOT NULL,
        rol TEXT NOT NULL CHECK(rol IN ('admin', 'soporte'))
    )
    """)
    print("✅ Tabla 'usuarios' lista.")

def crear_tabla_horarios(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT NOT NULL,
        fecha TEXT NOT NULL,
        hora_entrada TEXT,
        hora_salida TEXT
    )
    """)
    print("✅ Tabla 'horarios' lista.")

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

def crear_tabla_licencia(cursor):
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
    print("✅ Tabla 'licencia' lista.")

def inicializar_todo():
    conn = conectar()
    cursor = conn.cursor()

    crear_tabla_empleados(cursor)
    crear_tabla_usuarios(cursor)
    crear_tabla_horarios(cursor)
    crear_tabla_auditoria(cursor)
    crear_tabla_licencia(cursor)

    conn.commit()
    conn.close()
    print("\n🎉 Base de datos inicializada correctamente.")

if __name__ == "__main__":
    print("=" * 50)
    print("🛠️ INICIALIZADOR DE BASE DE DATOS CELITA".center(50))
    print("=" * 50)
    inicializar_todo()