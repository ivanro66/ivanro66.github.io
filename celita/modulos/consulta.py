import os
import sqlite3

# 📁 Ruta absoluta a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "base_datos", "asistencia_frensa.db")

from base_datos.db import conectar

def obtener_empleados_registrados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cedula, nombre, cargo FROM empleados")
    empleados = cursor.fetchall()
    conn.close()
    return empleados

def obtener_registros_asistencia(desde, hasta, cedula=None):
    conn = conectar()
    cursor = conn.cursor()

    query = """
        SELECT h.cedula, h.fecha, h.hora_entrada, h.hora_salida, e.nombre, e.cargo
        FROM horarios h
        JOIN empleados e ON h.cedula = e.cedula
        WHERE h.fecha BETWEEN ? AND ?
    """
    params = [desde, hasta]

    if cedula:
        query += " AND h.cedula = ?"
        params.append(cedula)

    cursor.execute(query, params)
    registros = cursor.fetchall()
    conn.close()
    return registros