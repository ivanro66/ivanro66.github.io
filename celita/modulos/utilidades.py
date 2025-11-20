import re
from datetime import datetime
from colorama import Fore

def pedir_cedula():
    while True:
        cedula = input("🔑 Cédula (solo números): ").strip()
        if cedula.isdigit() and 7 <= len(cedula) <= 9:
            return cedula
        print(Fore.RED + "❌ Cédula inválida. Usa solo números entre 7 y 9 dígitos.")

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print(Fore.RED + "❌ Este campo no puede estar vacío.")

def pedir_fecha(mensaje):
    while True:
        fecha = input(f"{mensaje} (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print(Fore.RED + "❌ Formato inválido. Ejemplo: 2025-09-30")

def pedir_hora(mensaje):
    hora = input(f"{mensaje} (HH:MM): ").strip()
    if re.match(r"^\d{2}:\d{2}$", hora):
        return hora + ":00"
    print(Fore.RED + "❌ Formato inválido. Ejemplo: 08:30")
    return ""