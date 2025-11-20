import os
import json

def cargar_configuracion():
    try:
        # Ruta absoluta al archivo config.json
        base_dir = os.path.dirname(os.path.abspath(__file__))
        ruta_config = os.path.join(base_dir, "config.json")

        # Cargar y devolver el contenido como diccionario
        with open(ruta_config, "r", encoding="utf-8") as f:
            return json.load(f)

    except FileNotFoundError:
        print("⚠️ Archivo 'config.json' no encontrado.")
    except json.JSONDecodeError:
        print("❌ Error de formato en 'config.json'. Verifica que sea JSON válido.")
    except Exception as e:
        print("❌ Error inesperado al cargar configuración:", e)

    return {}