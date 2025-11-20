import sqlite3
import csv
import os

def exportar_empleados_a_csv():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ruta_db = os.path.join(BASE_DIR, "..", "base_datos", "asistencia_frensa.db")
    ruta_csv = os.path.join(BASE_DIR, "empleados_exportados.csv")

    conn = sqlite3.connect(ruta_db)
    cursor = conn.cursor()

    cursor.execute("SELECT cedula, nombre, cargo, dependencia FROM empleados")
    empleados = cursor.fetchall()

    with open(ruta_csv, mode="w", newline='', encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["cedula", "nombre", "cargo", "dependencia"])
        escritor.writerows(empleados)

    conn.close()
    print(f"✅ Empleados exportados correctamente a:\n{ruta_csv}")

# Ejecutar directamente
if __name__ == "__main__":
    exportar_empleados_a_csv()