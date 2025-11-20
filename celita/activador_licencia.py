import os, sys
from modulos.licencia import activar_licencia

# Asegurar que el sistema encuentre los módulos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

print("=" * 50)
print("🔐 ACTIVADOR DE LICENCIA CELITA".center(50))
print("=" * 50)

codigo = input("🔑 Ingrese su código de licencia: ").strip()
mensaje = activar_licencia(codigo)
print(mensaje)