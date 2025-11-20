import os, sys, re, time, sqlite3
from datetime import datetime
from colorama import init, Fore
from tabulate import tabulate
from PIL import Image, ImageTk
from base_datos.db import respaldar_base_de_datos, obtener_ruta_db
from base_datos.db import limpiar_respaldos_antiguos

# Crear respaldo al iniciar el sistema
respaldar_base_de_datos()
limpiar_respaldos_antiguos(dias=7)
import bcrypt

# Crear respaldo al iniciar el sistema
respaldar_base_de_datos()

# Rutas absolutas
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)  # Carpeta del ejecutable
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

RECURSOS_DIR = os.path.join(BASE_DIR, "recursos")
DB_PATH = obtener_ruta_db()  # Ruta oficial desde db.py
print(f"📍 Ruta actual de la base de datos: {obtener_ruta_db()}")
ICONO_PATH = os.path.join(RECURSOS_DIR, "logo_celita.ico")
def verificar_recursos():
    print(Fore.CYAN + "\n🔍 Verificando recursos del sistema...")

    recursos_obligatorios = [
        DB_PATH,
        os.path.join(RECURSOS_DIR, "logo_frensa.jpg"),
        os.path.join(RECURSOS_DIR, "logo_tec.png"),
        os.path.join(RECURSOS_DIR, "logo_celita.ico")
    ]

    errores = []
    for ruta in recursos_obligatorios:
        if not os.path.exists(ruta):
            errores.append(f"❌ Recurso faltante: {ruta}")

    if errores:
        print(Fore.RED + "\n🚨 ERROR: Faltan recursos esenciales para ejecutar el sistema.")
        for error in errores:
            print(Fore.YELLOW + error)
        print(Fore.RED + "\n💡 Solución: Verifica que todos los archivos estén presentes en la carpeta correcta.")
        sys.exit(1)
    else:
        print(Fore.GREEN + "✅ Todos los recursos están presentes.")

# Importaciones internas
from interfaz_grafica.interfaz_login import mostrar_login
from interfaz_grafica.interfaz_licencia import mostrar_activador_licencia
from modulos.reportes import generar_pdf_reporte

init(autoreset=True)

def conectar():
    return sqlite3.connect(DB_PATH)

def test_logo():
    ruta1 = os.path.join(RECURSOS_DIR, "logo_frensa.jpg")
    ruta2 = os.path.join(RECURSOS_DIR, "logo_tec.png")
    print("Logo 1 existe:", os.path.exists(ruta1))
    print("Logo 2 existe:", os.path.exists(ruta2))

def limpiar_consola():
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_encabezado():
    print(Fore.BLUE + "=" * 50)
    print(Fore.YELLOW + "🛠️  SISTEMA DE ASISTENCIA FRENSA".center(50))
    print(Fore.BLUE + "=" * 50)

def pedir_texto(mensaje):
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print(Fore.RED + "❌ Este campo no puede estar vacío.")

def pedir_cedula():
    while True:
        cedula = input("🔑 Cédula (solo números): ").strip()
        if cedula.isdigit() and 7 <= len(cedula) <= 9:
            return cedula
        print(Fore.RED + "❌ Cédula inválida. Usa solo números entre 7 y 9 dígitos.")

def pedir_hora(mensaje):
    hora = input(f"{mensaje} (HH:MM): ").strip()
    if re.match(r"^\d{2}:\d{2}$", hora):
        return hora + ":00"
    return ""

def pedir_fecha(mensaje):
    while True:
        fecha = input(f"{mensaje} (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(fecha, "%Y-%m-%d")
            return fecha
        except ValueError:
            print(Fore.RED + "❌ Formato inválido. Ejemplo: 2025-09-30")

def login():
    print(Fore.CYAN + "\n🔐 INICIO DE SESIÓN")
    usuario = input("👤 Usuario: ").strip()
    clave = input("🔒 Clave: ").strip()

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
    return None, None

def cedula_valida(cedula):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM empleados WHERE cedula = ?", (cedula,))
    existe = cursor.fetchone()
    conn.close()
    return bool(existe)

def registrar_empleado():
    print(Fore.CYAN + "\n🧾 REGISTRAR EMPLEADO")
    cedula = pedir_cedula()
    if cedula_valida(cedula):
        print(Fore.RED + "❌ Ya existe un empleado con esa cédula.")
        return
    nombre = pedir_texto("🧍 Nombre completo: ")
    cargo = pedir_texto("💼 Cargo: ")
    fecha_ingreso = datetime.now().strftime("%Y-%m-%d")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO empleados (cedula, nombre, cargo, fecha_ingreso) VALUES (?, ?, ?, ?)",
                   (cedula, nombre, cargo, fecha_ingreso))
    conn.commit()
    conn.close()
    print(Fore.GREEN + "✅ Empleado registrado exitosamente.")

def modificar_empleado():
    print(Fore.CYAN + "\n✏️ MODIFICAR EMPLEADO")
    cedula = pedir_cedula()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, cargo FROM empleados WHERE cedula = ?", (cedula,))
    resultado = cursor.fetchone()
    if not resultado:
        print(Fore.RED + "❌ No existe un empleado con esa cédula.")
    else:
        print(Fore.YELLOW + f"🧍 Nombre actual: {resultado[0]}")
        print(Fore.YELLOW + f"💼 Cargo actual: {resultado[1]}")
        nuevo_nombre = pedir_texto("🧍 Nuevo nombre (dejar vacío para mantener): ")
        nuevo_cargo = pedir_texto("💼 Nuevo cargo (dejar vacío para mantener): ")
        nombre_final = nuevo_nombre if nuevo_nombre else resultado[0]
        cargo_final = nuevo_cargo if nuevo_cargo else resultado[1]
        cursor.execute("UPDATE empleados SET nombre = ?, cargo = ? WHERE cedula = ?",
                       (nombre_final, cargo_final, cedula))
        conn.commit()
        print(Fore.GREEN + "✅ Empleado modificado exitosamente.")
    conn.close()

def eliminar_empleado():
    print(Fore.CYAN + "\n🗑️ ELIMINAR EMPLEADO")
    cedula = pedir_cedula()
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre FROM empleados WHERE cedula = ?", (cedula,))
    resultado = cursor.fetchone()
    if not resultado:
        print(Fore.RED + "❌ No existe un empleado con esa cédula.")
    else:
        confirmacion = input(Fore.RED + f"⚠️ ¿Seguro que deseas eliminar a {resultado[0]}? (s/n): ").strip().lower()
        if confirmacion == "s":
            cursor.execute("DELETE FROM empleados WHERE cedula = ?", (cedula,))
            conn.commit()
            print(Fore.GREEN + "✅ Empleado eliminado.")
        else:
            print(Fore.YELLOW + "🔙 Operación cancelada.")
    conn.close()
    
def registrar_entrada(cedula):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO horarios (cedula, fecha, hora_entrada) VALUES (?, ?, ?)",
                   (cedula, fecha, hora))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Entrada registrada: {cedula} a las {hora}")

def registrar_salida(cedula):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?",
                   (hora, cedula, fecha))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Salida registrada: {cedula} a las {hora}")

def modo_marcaje_rapido():
    print(Fore.CYAN + "\n🕘 MODO DE MARCAJE RÁPIDO ACTIVADO")
    print(Fore.YELLOW + "🔄 Presiona Ctrl+C para salir del modo.\n")
    try:
        while True:
            print(Fore.CYAN + "\n¿Qué deseas registrar?")
            print(Fore.GREEN + "1. Entrada")
            print("2. Salida")
            print(Fore.RED + "0. Salir del modo")
            opcion = input("👉 Elige una opción: ").strip()
            if opcion == "0":
                print(Fore.CYAN + "🔚 Modo finalizado.")
                break
            elif opcion not in ["1", "2"]:
                print(Fore.RED + "❌ Opción inválida.")
                continue
            cedula = pedir_cedula()
            if not cedula_valida(cedula):
                print(Fore.RED + "❌ Esta cédula no está registrada como empleado.")
                continue
            fecha = datetime.now().strftime("%Y-%m-%d")
            hora_actual = datetime.now().strftime("%H:%M:%S")
            conn = conectar()
            cursor = conn.cursor()
            if opcion == "1":
                cursor.execute("INSERT OR REPLACE INTO horarios (cedula, fecha, hora_entrada) VALUES (?, ?, ?)",
                               (cedula, fecha, hora_actual))
                print(Fore.GREEN + f"✅ Entrada registrada para {cedula} a las {hora_actual}")
            elif opcion == "2":
                cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?",
                               (hora_actual, cedula, fecha))
                print(Fore.GREEN + f"✅ Salida registrada para {cedula} a las {hora_actual}")
            conn.commit()
            conn.close()
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n🔚 Modo de marcaje rápido finalizado.")

def consultar_horarios(cedula=None, fecha=None):
    conn = conectar()
    cursor = conn.cursor()
    if cedula and fecha:
        cursor.execute("SELECT * FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
    elif cedula:
        cursor.execute("SELECT * FROM horarios WHERE cedula = ?", (cedula,))
    elif fecha:
        cursor.execute("SELECT * FROM horarios WHERE fecha = ?", (fecha,))
    else:
        cursor.execute("SELECT * FROM horarios")
    registros = cursor.fetchall()
    conn.close()
    print(Fore.CYAN + "\n📋 REGISTROS DE ASISTENCIA")
    print(Fore.MAGENTA + tabulate(registros, headers=["Cédula", "Fecha", "Entrada", "Salida"], tablefmt="grid"))

def editar_asistencia(cedula, fecha, nueva_entrada, nueva_salida, usuario_actual):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT hora_entrada, hora_salida FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
        actual = cursor.fetchone()
        if not actual:
            print(Fore.RED + "❌ No existe ese registro.")
            return
        entrada_ant, salida_ant = actual
        if nueva_entrada:
            cursor.execute("UPDATE horarios SET hora_entrada = ? WHERE cedula = ? AND fecha = ?",
                           (nueva_entrada, cedula, fecha))
        if nueva_salida:
            cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?",
                           (nueva_salida, cedula, fecha))
        conn.commit()
        print(Fore.GREEN + "✅ Asistencia actualizada.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al editar asistencia: {e}")
    finally:
        conn.close()

def ver_reportes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cedula, fecha, hora_entrada, hora_salida FROM horarios ORDER BY fecha DESC")
    registros = cursor.fetchall()
    conn.close()
    if registros:
        print(Fore.CYAN + "\n📊 REPORTE DE ASISTENCIA")
        print(Fore.MAGENTA + tabulate(registros, headers=["Cédula", "Fecha", "Entrada", "Salida"], tablefmt="grid"))
    else:
        print(Fore.YELLOW + "⚠️ No hay registros disponibles.")

def ver_auditoria():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cedula, fecha, campo, valor_anterior, valor_nuevo, usuario_editor, timestamp FROM auditoria ORDER BY timestamp DESC")
    registros = cursor.fetchall()
    conn.close()
    if registros:
        print(Fore.CYAN + "\n📋 HISTORIAL DE AUDITORÍA")
        print(Fore.MAGENTA + tabulate(registros, headers=["Cédula", "Fecha", "Campo", "Antes", "Después", "Editor", "Fecha edición"], tablefmt="grid"))
    else:
        print(Fore.YELLOW + "⚠️ No hay registros de auditoría.")

def cambiar_contraseña_usuario():
    print(Fore.CYAN + "\n🔒 CAMBIAR CONTRASEÑA DE USUARIO")
    usuario = input("👤 Usuario a modificar (admin/soporte): ").strip().lower()
    if usuario not in ["admin", "soporte"]:
        print(Fore.RED + "❌ Usuario inválido.")
        return
    nueva_clave = input("🆕 Nueva contraseña: ").strip()
    hashed = bcrypt.hashpw(nueva_clave.encode("utf-8"), bcrypt.gensalt())
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (hashed, usuario))
    conn.commit()
    conn.close()
    print(Fore.GREEN + f"✅ Contraseña actualizada para '{usuario}'.")

def iniciar_sistema():
    while True:
        verificar_recursos()
        verificar_estructura_base_datos()
        limpiar_consola()
        mostrar_encabezado()
        ...

def verificar_estructura_base_datos():
    estructura_requerida = {
        "usuarios": ["usuario", "clave", "rol"],
        "empleados": ["cedula", "nombre", "cargo", "fecha_ingreso"],
        "horarios": ["cedula", "fecha", "hora_entrada", "hora_salida"],
        "auditoria": ["cedula", "fecha", "campo", "valor_anterior", "valor_nuevo", "usuario_editor", "timestamp"]
    }
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tablas_existentes = set(row[0] for row in cursor.fetchall())
    errores = []
    for tabla, columnas in estructura_requerida.items():
        if tabla not in tablas_existentes:
            errores.append(f"❌ Tabla faltante: {tabla}")
            continue
        cursor.execute(f"PRAGMA table_info({tabla})")
        columnas_existentes = set(row[1] for row in cursor.fetchall())
        for columna in columnas:
            if columna not in columnas_existentes:
                errores.append(f"❌ Falta columna '{columna}' en tabla '{tabla}'")
    conn.close()
    if errores:
        print(Fore.RED + "\n🚨 ERROR DE ESTRUCTURA EN LA BASE DE DATOS:")
        for error in errores:
            print(Fore.YELLOW + error)
        print(Fore.RED + "\n💡 Solución: Corrige la estructura ejecutando el script SQL correspondiente.")
        sys.exit(1)
    else:
        print(Fore.GREEN + "✅ La estructura de la base de datos es válida.")
        
def generar_menu_reportes():
    print(Fore.CYAN + "\n📄 ¿Qué tipo de reporte deseas generar?")
    print(Fore.GREEN + "1. Reporte general")
    print("2. Reporte por cédula")
    print("3. Reporte por fecha")
    print("4. Reporte por rango de fechas")
    print(Fore.RED + "0. Cancelar")

    subopcion = input("👉 Elige una opción: ").strip()
    if subopcion == "1":
        generar_pdf_reporte()
    elif subopcion == "2":
        cedula = pedir_cedula()
        generar_pdf_reporte(filtro="cedula", valor=cedula)
    elif subopcion == "3":
        fecha = pedir_fecha("📅 Fecha del reporte")
        generar_pdf_reporte(filtro="fecha", valor=fecha)
    elif subopcion == "4":
        fecha_inicio = pedir_fecha("📅 Fecha inicio")
        fecha_fin = pedir_fecha("📅 Fecha fin")
        generar_pdf_reporte(filtro="rango", valor=(fecha_inicio, fecha_fin))
    elif subopcion == "0":
        print(Fore.YELLOW + "🔙 Cancelado.")
    else:
        print(Fore.RED + "❌ Opción inválida.")

def ejecutar_menu(usuario_actual, rol):
    while True:
        limpiar_consola()
        mostrar_encabezado()
        print(Fore.YELLOW + f"\n👤 Usuario: {usuario_actual} | Rol: {rol}")

        if rol == "admin":
            print(Fore.GREEN + "\n1. Registrar empleado")
            print("2. Modificar empleado")
            print("3. Registrar entrada")
            print("4. Registrar salida")
            print("5. Consultar horarios")
            print("6. Ver reporte en consola")
            print("7. Generar reporte PDF")
            print("8. Activar modo de marcaje rápido")
            print(Fore.RED + "\n0. Cerrar sesión")

            opcion = input("👉 Elige una opción: ").strip()
            if opcion == "1":
                registrar_empleado()
            elif opcion == "2":
                modificar_empleado()
            elif opcion == "3":
                cedula = pedir_cedula()
                registrar_entrada(cedula)
            elif opcion == "4":
                cedula = pedir_cedula()
                registrar_salida(cedula)
            elif opcion == "5":
                consultar_horarios()
            elif opcion == "6":
                ver_reportes()
            elif opcion == "7":
                generar_menu_reportes()
            elif opcion == "8":
                modo_marcaje_rapido()
            elif opcion == "0":
                print(Fore.CYAN + "🔒 Sesión cerrada.")
                break
            else:
                print(Fore.RED + "❌ Opción inválida.")
            input(Fore.CYAN + "\nPresiona Enter para continuar...")

        elif rol == "soporte":
            print(Fore.GREEN + "\n1. Registrar empleado")
            print("2. Modificar empleado")
            print("3. Eliminar empleado")
            print("4. Consultar horarios")
            print("5. Editar asistencia")
            print("6. Ver auditoría")
            print("7. Ver reporte en consola")
            print("8. Generar reporte PDF")
            print("9. Cambiar contraseña de usuarios")
            print(Fore.RED + "\n0. Cerrar sesión")

            opcion = input("👉 Elige una opción: ").strip()
            if opcion == "1":
                registrar_empleado()
            elif opcion == "2":
                modificar_empleado()
            elif opcion == "3":
                eliminar_empleado()
            elif opcion == "4":
                consultar_horarios()
            elif opcion == "5":
                cedula = pedir_cedula()
                fecha = pedir_fecha("📅 Fecha a editar")
                nueva_entrada = pedir_hora("🕘 Nueva hora de entrada (deja vacío para no cambiar)")
                nueva_salida = pedir_hora("🕔 Nueva hora de salida (deja vacío para no cambiar)")
                editar_asistencia(cedula, fecha, nueva_entrada, nueva_salida, usuario_actual)
            elif opcion == "6":
                ver_auditoria()
            elif opcion == "7":
                ver_reportes()
            elif opcion == "8":
                generar_menu_reportes()
            elif opcion == "9":
                cambiar_contraseña_usuario()
            elif opcion == "0":
                print(Fore.CYAN + "🔒 Sesión cerrada.")
                break
            else:
                print(Fore.RED + "❌ Opción inválida.")
            input(Fore.CYAN + "\nPresiona Enter para continuar...")

def iniciar_sistema():
    while True:
        verificar_estructura_base_datos()
        limpiar_consola()
        mostrar_encabezado()
        print(Fore.CYAN + "\n🔐 ¿Qué deseas hacer?")
        print(Fore.GREEN + "1. Iniciar sesión")
        print(Fore.RED + "0. Salir")
        opcion_inicio = input("👉 Elige una opción: ").strip()
        if opcion_inicio == "1":
            usuario_actual, rol = login()
            if rol:
                ejecutar_menu(usuario_actual, rol)
        elif opcion_inicio == "0":
            print(Fore.CYAN + "👋 Saliendo del sistema. ¡Hasta pronto!")
            break
        else:
            print(Fore.RED + "❌ Opción inválida.")
            input(Fore.CYAN + "\nPresiona Enter para continuar...")

if __name__ == "__main__":
    from interfaz_grafica.interfaz_login import mostrar_login
    mostrar_login()