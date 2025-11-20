import sqlite3
import os

def obtener_empleados():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_db = os.path.join(BASE_DIR, "..", "base_datos", "asistencia_frensa.db")
    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    cursor.execute("SELECT cedula, nombre, cargo, dependencia FROM empleados ORDER BY nombre ASC")
    empleados = cursor.fetchall()
    conn.close()
    return empleados