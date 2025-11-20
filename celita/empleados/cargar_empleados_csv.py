import csv
import sqlite3
import os

def cargar_empleados_desde_csv():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_db = os.path.join(BASE_DIR, "..", "base_datos", "asistencia_frensa.db")
    ruta_csv = os.path.join(BASE_DIR, "empleados_exportados.csv")

    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    with open(ruta_csv, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        registros_insertados = 0

        for fila in lector:
            cedula = fila.get("cedula", "").strip()
            nombre = fila.get("nombre", "").strip()
            cargo = fila.get("cargo", "").strip()
            dependencia = fila.get("dependencia", "").strip()

            if cedula.isdigit() and nombre:
                cursor.execute("""
                    INSERT OR IGNORE INTO empleados (cedula, nombre, cargo, dependencia)
                    VALUES (?, ?, ?, ?)
                """, (cedula, nombre, cargo, dependencia))
                registros_insertados += 1

    conn.commit()
    conn.close()
    print(f"✅ {registros_insertados} empleados cargados correctamente desde:\n{ruta_csv}")

# Ejecutar directamente
if __name__ == "__main__":
    cargar_empleados_desde_csv()