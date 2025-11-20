import sqlite3
import os

# Ruta a tu base de datos
DB_PATH = os.path.join("base_datos", "asistencia_frensa.db")

def limpiar_base_de_datos():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Lista de tablas que deseas limpiar
        tablas = ["empleados", "horarios", "historial", "auditoria"]

        for tabla in tablas:
            cursor.execute(f"DELETE FROM {tabla};")
            cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{tabla}';")  # Reinicia autoincremento si aplica

        conn.commit()
        print("✅ Base de datos limpiada correctamente.")
    except Exception as e:
        print(f"❌ Error al limpiar la base de datos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    limpiar_base_de_datos()