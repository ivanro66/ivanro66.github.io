import sqlite3
import os
import random
import string

def generar_codigo(longitud=12):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=longitud))

# Ruta a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_db = os.path.join(BASE_DIR, "base_datos", "asistencia_frensa.db")
conn = sqlite3.connect(ruta_db)
cursor = conn.cursor()

licencias = []

print("🎟️ Generando licencias definitivas...")
for _ in range(10):
    codigo = generar_codigo()
    licencias.append((codigo, "definitiva"))
    cursor.execute("INSERT INTO licencia (codigo, tipo, estado) VALUES (?, ?, ?)",
                   (codigo, "definitiva", "disponible"))

print("⏳ Generando licencias temporales (3 meses)...")
for _ in range(10):
    codigo = generar_codigo()
    licencias.append((codigo, "temporal"))
    cursor.execute("INSERT INTO licencia (codigo, tipo, estado) VALUES (?, ?, ?)",
                   (codigo, "temporal", "disponible"))

conn.commit()
conn.close()

# Guardar en archivo de respaldo
archivo_txt = "licencias_generadas.txt"
with open(archivo_txt, "w") as f:
    for codigo, tipo in licencias:
        f.write(f"{codigo} - {tipo}\n")

print(f"✅ Licencias generadas y guardadas en '{archivo_txt}'")