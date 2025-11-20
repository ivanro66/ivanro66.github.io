from colorama import Fore
from base_datos.db import conectar
import bcrypt

# 🔐 Login con verificación de rol
def login():
    print(Fore.CYAN + "\n🔐 INICIO DE SESIÓN")
    usuario = input("👤 Usuario: ").strip()
    clave = input("🔒 Clave: ").strip()

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT clave, rol FROM usuarios WHERE usuario = ?", (usuario,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            hashed = resultado[0]
            if isinstance(hashed, str):
                hashed = hashed.encode("utf-8")
            if bcrypt.checkpw(clave.encode("utf-8"), hashed):
                print(Fore.GREEN + f"✅ Bienvenido {usuario} ({resultado[1]})")
                return usuario, resultado[1]
            else:
                print(Fore.RED + "❌ Clave incorrecta.")
        else:
            print(Fore.RED + "❌ Usuario no encontrado.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al iniciar sesión: {e}")
    return None, None

# 🔁 Restablecer contraseña (con código de seguridad)
def restablecer_contraseña():
    print(Fore.CYAN + "\n🔁 RESTABLECER CONTRASEÑA")
    usuario = input("👤 Nombre de usuario: ").strip()
    rol = input("🎯 Rol (admin/soporte): ").strip().lower()

    if rol not in ["admin", "soporte"]:
        print(Fore.RED + "❌ Solo se permite restablecer contraseña para admin o soporte.")
        return

    codigo = input("🔐 Código de seguridad: ").strip()
    if codigo != "frensa2025":
        print(Fore.RED + "❌ Código de seguridad incorrecto.")
        return

    nueva_clave = input("🆕 Nueva contraseña: ").strip()
    hashed = bcrypt.hashpw(nueva_clave.encode("utf-8"), bcrypt.gensalt())

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM usuarios WHERE usuario = ? AND rol = ?", (usuario, rol))
        if not cursor.fetchone():
            print(Fore.RED + "❌ Usuario no encontrado o rol incorrecto.")
            conn.close()
            return

        cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (hashed, usuario))
        conn.commit()
        conn.close()
        print(Fore.GREEN + f"✅ Contraseña actualizada para el usuario '{usuario}'.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al actualizar contraseña: {e}")

# 🔒 Cambiar contraseña desde sesión activa
def cambiar_contraseña(usuario_actual):
    print(Fore.CYAN + "\n🔒 CAMBIAR CONTRASEÑA")
    clave_actual = input("🔑 Clave actual: ").strip()

    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT clave FROM usuarios WHERE usuario = ?", (usuario_actual,))
        resultado = cursor.fetchone()

        if not resultado or not bcrypt.checkpw(clave_actual.encode("utf-8"), resultado[0]):
            print(Fore.RED + "❌ Clave actual incorrecta.")
            conn.close()
            return

        nueva_clave = input("🆕 Nueva contraseña: ").strip()
        hashed = bcrypt.hashpw(nueva_clave.encode("utf-8"), bcrypt.gensalt())
        cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (hashed, usuario_actual))
        conn.commit()
        conn.close()
        print(Fore.GREEN + "✅ Contraseña actualizada exitosamente.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al cambiar contraseña: {e}")

# 📋 Obtener nombre y cargo de un empleado por cédula (para reportes)
def obtener_datos_empleado(cedula):
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cargo FROM empleados WHERE cedula = ?", (cedula,))
        resultado = cursor.fetchone()
        conn.close()
        if resultado:
            return {"nombre": resultado[0], "cargo": resultado[1]}
    except Exception as e:
        print(Fore.RED + f"❌ Error al consultar datos del empleado: {e}")
    return {"nombre": "Desconocido", "cargo": "Sin cargo"}