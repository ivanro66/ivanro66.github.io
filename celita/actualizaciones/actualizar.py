import shutil
import os

# 📁 Ruta absoluta del sistema principal
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_sistema = os.path.join(BASE_DIR, "sistema")
ruta_actualizaciones = os.path.join(BASE_DIR, "actualizaciones")

# 📦 Archivos que deseas actualizar
archivos = [
    "reportes.py",
    "config.json",
    "recursos/logo_celita.png"
]

actualizados = 0

for archivo in archivos:
    origen = os.path.join(ruta_actualizaciones, archivo)
    destino = os.path.join(ruta_sistema, archivo)

    if os.path.exists(origen):
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        shutil.copy2(origen, destino)
        print(f"✅ {archivo} actualizado.")
        actualizados += 1
    else:
        print(f"⚠️ {archivo} no encontrado en actualizaciones.")

print(f"\n📦 Archivos actualizados: {actualizados} de {len(archivos)}")
print(f"📁 Ruta del sistema: {ruta_sistema}")