import sqlite3
import bcrypt
from datetime import datetime

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "base_datos", "asistencia_frensa.db")

estructura = {
    "usuarios": ["usuario", "clave", "rol"],
    "empleados": ["cedula", "nombre", "cargo", "fecha_ingreso"],
    "horarios": ["cedula", "fecha", "hora_entrada", "hora_salida"],
    "auditoria": ["usuario", "accion", "fecha", "hora"]
}

def conectar():
    return sqlite3.connect(DB_PATH)

def verificar_tablas_y_columnas():
    print("🔍 Verificando estructura de la base de datos...")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas = set(row[0] for row in cursor.fetchall())

    errores = []
    for tabla, columnas in estructura.items():
        if tabla not in tablas:
            errores.append(f"❌ Tabla faltante: {tabla}")
            continue
        cursor.execute(f"PRAGMA table_info({tabla})")
        existentes = set(row[1] for row in cursor.fetchall())
        for col in columnas:
            if col not in existentes:
                errores.append(f"❌ Falta columna '{col}' en tabla '{tabla}'")

    conn.close()
    if errores:
        print("\n🚨 ERRORES DETECTADOS:")
        for e in errores:
            print(e)
        return False
    print("✅ Estructura válida.")
    return True

def verificar_login(usuario, clave):
    print(f"\n🔐 Verificando login para usuario '{usuario}'...")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT clave, rol FROM usuarios WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if not resultado:
        print(f"❌ Usuario '{usuario}' no existe.")
        return False

    clave_hash, rol = resultado
    if bcrypt.checkpw(clave.encode("utf-8"), clave_hash):
        print(f"✅ Login exitoso como '{rol}'.")
        return True
    else:
        print("❌ Contraseña incorrecta.")
        return False

def verificar_registro_empleado():
    print("\n🧾 Verificando registro de empleado...")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO empleados (cedula, nombre, cargo, fecha_ingreso)
            VALUES (?, ?, ?, ?)
        """, ("99999999", "Empleado Test", "Tester", datetime.now().strftime("%Y-%m-%d")))
        conn.commit()
        print("✅ Registro exitoso.")
    except Exception as e:
        print(f"❌ Error al registrar empleado: {e}")
    finally:
        conn.close()

def verificar_entrada_salida():
    print("\n🕘 Verificando registro de entrada/salida...")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO horarios (cedula, fecha, hora_entrada, hora_salida)
            VALUES (?, ?, ?, ?)
        """, ("99999999", datetime.now().strftime("%Y-%m-%d"), "08:00:00", "12:00:00"))
        conn.commit()
        print("✅ Registro de asistencia exitoso.")
    except Exception as e:
        print(f"❌ Error en asistencia: {e}")
    finally:
        conn.close()

def verificar_auditoria():
    print("\n📋 Verificando inserción en auditoría...")
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO auditoria (usuario, accion, fecha, hora)
            VALUES (?, ?, ?, ?)
        """, ("admin", "diagnostico", datetime.now().strftime("%Y-%m-%d"), datetime.now().strftime("%H:%M:%S")))
        conn.commit()
        print("✅ Auditoría registrada.")
    except Exception as e:
        print(f"❌ Error en auditoría: {e}")
    finally:
        conn.close()

# 🔁 Flujo completo
if verificar_tablas_y_columnas():
    verificar_login("admin", "admin123")
    verificar_login("soporte", "soporte123")
    verificar_registro_empleado()
    verificar_entrada_salida()
    verificar_auditoria()