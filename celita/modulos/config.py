import json
import os

# 📁 Ruta absoluta al archivo config.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.json")

def cargar_configuracion():
    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, "r", encoding="utf-8") as archivo:
        return json.load(archivo)