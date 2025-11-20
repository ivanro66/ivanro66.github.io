from colorama import Fore
from base_datos.db import conectar
from modulos.utilidades import pedir_cedula, pedir_texto
from datetime import datetime

DEPENDENCIAS_VALIDAS = [
    "Presidencia", "Rrhh", "Administración", "Tecnología",
    "Coordinación de Cultura", "Coordinación de Insumos y Logística",
    "Coordinación de Salud", "Coordinación de Deporte", "Asesoría Legal",
    "Prensa", "Atención Integral", "Mantenimiento", "Seguridad",
    "Infraestructura", "Escolarización", "Dirección Técnica","Casa de los Niños"
]

def mostrar_dependencias():
    print(Fore.YELLOW + "\n📋 Dependencias disponibles:")
    for dep in DEPENDENCIAS_VALIDAS:
        print(" -", dep)

# 🧾 Registrar nuevo empleado
def registrar_empleado():
    print(Fore.CYAN + "\n🧾 REGISTRAR EMPLEADO")
    cedula = pedir_cedula()
    nombre = pedir_texto("🧍 Nombre completo: ")
    cargo = pedir_texto("💼 Cargo: ")

    mostrar_dependencias()
    dependencia = pedir_texto("🏢 Dependencia: ")
    if dependencia not in DEPENDENCIAS_VALIDAS:
        print(Fore.RED + "❌ Dependencia no válida. Registro cancelado.")
        return

    fecha_ingreso = datetime.now().strftime("%Y-%m-%d")

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 1 FROM empleados WHERE cedula = ?", (cedula,))
        if cursor.fetchone():
            print(Fore.RED + "❌ Ya existe un empleado con esa cédula.")
            return

        cursor.execute("""
            INSERT INTO empleados (cedula, nombre, cargo, fecha_ingreso, dependencia)
            VALUES (?, ?, ?, ?, ?)
        """, (cedula, nombre, cargo, fecha_ingreso, dependencia))
        conn.commit()
        print(Fore.GREEN + "✅ Empleado registrado exitosamente.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al registrar empleado: {e}")
    finally:
        conn.close()

# ✏️ Modificar empleado
def modificar_empleado():
    print(Fore.CYAN + "\n✏️ MODIFICAR EMPLEADO")
    cedula = pedir_cedula()

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre, cargo, dependencia FROM empleados WHERE cedula = ?", (cedula,))
        resultado = cursor.fetchone()

        if not resultado:
            print(Fore.RED + "❌ No se encontró un empleado con esa cédula.")
            return

        print(Fore.YELLOW + f"\nEmpleado actual:")
        print(f"🧍 Nombre: {resultado[0]}")
        print(f"💼 Cargo: {resultado[1]}")
        print(f"🏢 Dependencia: {resultado[2]}")

        nuevo_nombre = input("🧍 Nuevo nombre (dejar vacío para mantener): ").strip()
        nuevo_cargo = input("💼 Nuevo cargo (dejar vacío para mantener): ").strip()

        mostrar_dependencias()
        nueva_dependencia = input("🏢 Nueva dependencia (dejar vacío para mantener): ").strip()

        nombre_final = nuevo_nombre if nuevo_nombre else resultado[0]
        cargo_final = nuevo_cargo if nuevo_cargo else resultado[1]
        dependencia_final = nueva_dependencia if nueva_dependencia else resultado[2]

        if nueva_dependencia and nueva_dependencia not in DEPENDENCIAS_VALIDAS:
            print(Fore.RED + "❌ Dependencia no válida. Modificación cancelada.")
            return

        cursor.execute("""
            UPDATE empleados
            SET nombre = ?, cargo = ?, dependencia = ?
            WHERE cedula = ?
        """, (nombre_final, cargo_final, dependencia_final, cedula))
        conn.commit()
        print(Fore.GREEN + "✅ Empleado modificado exitosamente.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al modificar empleado: {e}")
    finally:
        conn.close()

# 🗑️ Eliminar empleado
def eliminar_empleado():
    print(Fore.CYAN + "\n🗑️ ELIMINAR EMPLEADO")
    cedula = pedir_cedula()

    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT nombre FROM empleados WHERE cedula = ?", (cedula,))
        resultado = cursor.fetchone()

        if not resultado:
            print(Fore.RED + "❌ No se encontró un empleado con esa cédula.")
            return

        confirmacion = input(Fore.YELLOW + f"⚠️ ¿Estás seguro de eliminar a '{resultado[0]}'? (s/n): ").strip().lower()
        if confirmacion == "s":
            cursor.execute("DELETE FROM empleados WHERE cedula = ?", (cedula,))
            conn.commit()
            print(Fore.GREEN + "✅ Empleado eliminado correctamente.")
        else:
            print(Fore.YELLOW + "ℹ️ Operación cancelada.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al eliminar empleado: {e}")
    finally:
        conn.close()