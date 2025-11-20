import sqlite3
import os

def borrar_todos_los_empleados():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_db = os.path.join(BASE_DIR, "..", "base_datos", "asistencia_frensa.db")

    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM empleados")
    conn.commit()
    conn.close()

    print(f"🧹 Todos los registros de empleados han sido eliminados de:\n{ruta_db}")

# Ejecutar directamente
if __name__ == "__main__":
    borrar_todos_los_empleados()