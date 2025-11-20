from datetime import datetime
from colorama import init, Fore
from tabulate import tabulate
from base_datos.db import conectar  # ✅ Conexión centralizada

init(autoreset=True)

# ✅ Registrar entrada
def registrar_entrada(cedula):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT hora_entrada FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
        existente = cursor.fetchone()

        if existente and existente[0]:
            print(Fore.YELLOW + "⚠️ Ya se ha registrado la entrada para hoy.")
        else:
            if existente:
                cursor.execute("UPDATE horarios SET hora_entrada = ? WHERE cedula = ? AND fecha = ?", (hora, cedula, fecha))
            else:
                cursor.execute("INSERT INTO horarios (cedula, fecha, hora_entrada) VALUES (?, ?, ?)", (cedula, fecha, hora))

            cursor.execute("SELECT entrada FROM historial WHERE cedula = ? AND fecha = ?", (cedula, fecha))
            if cursor.fetchone():
                cursor.execute("UPDATE historial SET entrada = ? WHERE cedula = ? AND fecha = ?", (hora, cedula, fecha))
            else:
                cursor.execute("INSERT INTO historial (cedula, fecha, entrada) VALUES (?, ?, ?)", (cedula, fecha, hora))

            conn.commit()
            print(Fore.GREEN + "✅ Entrada registrada correctamente.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al registrar entrada: {e}")
    finally:
        conn.close()

# ✅ Registrar salida
def registrar_salida(cedula):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT hora_salida FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
        existente = cursor.fetchone()

        if existente and existente[0]:
            print(Fore.YELLOW + "⚠️ Ya se ha registrado la salida para hoy.")
        else:
            # Verificamos si existe un registro previo (aunque sea solo con entrada)
            cursor.execute("SELECT hora_entrada FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
            entrada_existente = cursor.fetchone()

            if entrada_existente:
                cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?", (hora, cedula, fecha))
            else:
                # Insertamos una fila completa con hora_entrada = NULL
                cursor.execute("INSERT INTO horarios (cedula, fecha, hora_entrada, hora_salida) VALUES (?, ?, ?, ?)", (cedula, fecha, None, hora))

            cursor.execute("SELECT salida FROM historial WHERE cedula = ? AND fecha = ?", (cedula, fecha))
            if cursor.fetchone():
                cursor.execute("UPDATE historial SET salida = ? WHERE cedula = ? AND fecha = ?", (hora, cedula, fecha))
            else:
                cursor.execute("INSERT INTO historial (cedula, fecha, salida) VALUES (?, ?, ?)", (cedula, fecha, hora))

            conn.commit()
            print(Fore.GREEN + "✅ Salida registrada correctamente.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al registrar salida: {e}")
    finally:
        conn.close()

# ✅ Consultar horarios con filtros
def consultar_horarios(cedula=None, fecha=None):
    conn = conectar()
    cursor = conn.cursor()

    base_query = """
    SELECT e.nombre, e.cargo, h.cedula, h.fecha, h.hora_entrada, h.hora_salida
    FROM horarios h
    JOIN empleados e ON h.cedula = e.cedula
    """

    try:
        if cedula and fecha:
            cursor.execute(base_query + " WHERE h.cedula = ? AND h.fecha = ?", (cedula, fecha))
        elif cedula:
            cursor.execute(base_query + " WHERE h.cedula = ? ORDER BY h.fecha DESC", (cedula,))
        elif fecha:
            cursor.execute(base_query + " WHERE h.fecha = ? ORDER BY h.cedula", (fecha,))
        else:
            cursor.execute(base_query + " ORDER BY h.fecha DESC")

        registros = cursor.fetchall()

        if registros:
            print(Fore.MAGENTA + tabulate(registros, headers=["Nombre", "Cargo", "Cédula", "Fecha", "Entrada", "Salida"], tablefmt="grid"))
        else:
            print(Fore.YELLOW + "⚠️ No se encontraron registros.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al consultar horarios: {e}")
    finally:
        conn.close()

# ✅ Validar si la cédula existe
def cedula_valida(cedula):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT cedula FROM empleados WHERE cedula = ?", (cedula,))
        existe = cursor.fetchone()
        return existe is not None
    except Exception as e:
        print(Fore.RED + f"❌ Error al validar cédula: {e}")
        return False
    finally:
        conn.close()

# ✅ Editar asistencia con auditoría
def editar_asistencia(cedula, fecha, nueva_entrada=None, nueva_salida=None, usuario_editor="soporte"):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT hora_entrada, hora_salida
            FROM horarios
            WHERE cedula = ? AND fecha = ?
        """, (cedula, fecha))
        registro = cursor.fetchone()

        if not registro:
            print(Fore.YELLOW + "⚠️ No existe un registro para esa cédula y fecha.")
            return

        print(Fore.CYAN + "\n📌 Registro actual:")
        print(Fore.YELLOW + f"Entrada: {registro[0] or '—'} | Salida: {registro[1] or '—'}")

        cambios = False

        if nueva_entrada and nueva_entrada != registro[0]:
            registrar_auditoria(cedula, fecha, "hora_entrada", registro[0], nueva_entrada, usuario_editor)
            cursor.execute("UPDATE horarios SET hora_entrada = ? WHERE cedula = ? AND fecha = ?", (nueva_entrada, cedula, fecha))
            cambios = True

        if nueva_salida and nueva_salida != registro[1]:
            registrar_auditoria(cedula, fecha, "hora_salida", registro[1], nueva_salida, usuario_editor)
            cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?", (nueva_salida, cedula, fecha))
            cambios = True

        if cambios:
            conn.commit()
            print(Fore.GREEN + "✅ Asistencia actualizada correctamente.")
            print(Fore.MAGENTA + f"📝 Editado manualmente por {usuario_editor} en {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print(Fore.YELLOW + "⚠️ No se realizaron cambios.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al editar asistencia: {e}")
    finally:
        conn.close()

# ✅ Registrar auditoría
def registrar_auditoria(cedula, fecha, campo, valor_anterior, valor_nuevo, usuario_editor):
    conn = conectar()
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        cursor.execute("""
            INSERT INTO auditoria (cedula, fecha, campo, valor_anterior, valor_nuevo, usuario_editor, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (cedula, fecha, campo, valor_anterior, valor_nuevo, usuario_editor, timestamp))
        conn.commit()
    except Exception as e:
        print(Fore.RED + f"❌ Error al registrar auditoría: {e}")
    finally:
        conn.close()

# ✅ Ver reportes de asistencia
def ver_reportes():
    conn = conectar()
    cursor = conn.cursor()

    print(Fore.CYAN + "\n📊 REPORTES DE ASISTENCIA")
    filtro = input("🔍 Filtrar por (cedula/fecha/todo): ").strip().lower()

    base_query = """
        SELECT e.nombre, e.cargo, h.cedula, h.fecha, h.hora_entrada, h.hora_salida
        FROM horarios h
        JOIN empleados e ON h.cedula = e.cedula
    """

    try:
        if filtro == "cedula":
            cedula = input("🔑 Cédula: ").strip().upper()
            cursor.execute(base_query + " WHERE h.cedula = ? ORDER BY h.fecha DESC", (cedula,))
        elif filtro == "fecha":
            fecha = input("📅 Fecha (YYYY-MM-DD): ").strip()
            datetime.strptime(fecha, "%Y-%m-%d")
            cursor.execute(base_query + " WHERE h.fecha = ? ORDER BY h.cedula", (fecha,))
        else:
            cursor.execute(base_query + " ORDER BY h.fecha DESC")

        registros = cursor.fetchall()

        if registros:
            print(Fore.MAGENTA + tabulate(registros, headers=["Nombre", "Cargo", "Cédula", "Fecha", "Entrada", "Salida"], tablefmt="grid"))
        else:
            print(Fore.YELLOW + "⚠️ No se encontraron registros.")
    except ValueError:
        print(Fore.RED + "❌ Formato de fecha inválido. Usa YYYY-MM-DD.")
    except Exception as e:
        print(Fore.RED + f"❌ Error al consultar reportes: {e}")
    finally:
        conn.close()