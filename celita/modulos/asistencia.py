from datetime import datetime
from base_datos.db import conectar

# 🕘 Registrar entrada
def registrar_entrada(cedula):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM empleados WHERE cedula = ?", (cedula,))
        empleado = cursor.fetchone()
        if not empleado:
            conn.close()
            return "no_empleado", None

        nombre = empleado[0]

        cursor.execute("SELECT hora_entrada FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
        existente = cursor.fetchone()

        if existente:
            cursor.execute("UPDATE horarios SET hora_entrada = ? WHERE cedula = ? AND fecha = ?", (hora, cedula, fecha))
        else:
            cursor.execute("INSERT INTO horarios (cedula, fecha, hora_entrada) VALUES (?, ?, ?)", (cedula, fecha, hora))

        conn.commit()
        conn.close()
        return "ok", nombre

    except Exception as e:
        print(f"Error al registrar entrada: {e}")
        return "error", None

# 🕔 Registrar salida
def registrar_salida(cedula):
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    try:
        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM empleados WHERE cedula = ?", (cedula,))
        empleado = cursor.fetchone()
        if not empleado:
            conn.close()
            return "no_empleado", None

        nombre = empleado[0]

        cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?", (hora, cedula, fecha))

        conn.commit()
        conn.close()
        return "ok", nombre

    except Exception as e:
        print(f"Error al registrar salida: {e}")
        return "error", None

# 📋 Consultar horarios con datos completos
def consultar_horarios(cedula=None, fecha=None):
    conn = conectar()
    cursor = conn.cursor()

    base_query = """
        SELECT h.cedula, h.fecha, h.hora_entrada, h.hora_salida,
               e.nombre, e.cargo, e.dependencia,
               CASE
                   WHEN h.hora_entrada IS NOT NULL OR h.hora_salida IS NOT NULL THEN 'ASISTENTE'
                   ELSE 'INASISTENTE'
               END AS estado
        FROM horarios h
        JOIN empleados e ON h.cedula = e.cedula
    """

    condiciones = []
    parametros = []

    if cedula:
        condiciones.append("h.cedula = ?")
        parametros.append(cedula)
    if fecha:
        condiciones.append("h.fecha = ?")
        parametros.append(fecha)

    if condiciones:
        base_query += " WHERE " + " AND ".join(condiciones)

    base_query += " ORDER BY h.fecha ASC"

    cursor.execute(base_query, tuple(parametros))
    registros = cursor.fetchall()
    conn.close()
    return registros if registros else []

# ✏️ Editar asistencia
def editar_asistencia(cedula, fecha, nueva_entrada=None, nueva_salida=None):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT hora_entrada, hora_salida FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
    actual = cursor.fetchone()
    if not actual:
        conn.close()
        return False

    if nueva_entrada:
        cursor.execute("UPDATE horarios SET hora_entrada = ? WHERE cedula = ? AND fecha = ?", (nueva_entrada, cedula, fecha))
    if nueva_salida:
        cursor.execute("UPDATE horarios SET hora_salida = ? WHERE cedula = ? AND fecha = ?", (nueva_salida, cedula, fecha))

    conn.commit()
    conn.close()
    return True