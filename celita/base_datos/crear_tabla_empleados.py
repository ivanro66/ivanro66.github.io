from base_datos.db import conectar  # ✅ Conexión centralizada

def crear_tabla_empleados():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS empleados (
            cedula TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            cargo TEXT NOT NULL,
            fecha_ingreso TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tabla 'empleados' creada correctamente.")

if __name__ == "__main__":
    crear_tabla_empleados()