import os
import json
import webbrowser
import sqlite3
from datetime import datetime
from base_datos.db import conectar
from collections import defaultdict
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# 📁 Rutas internas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECURSOS_DIR = os.path.join(BASE_DIR, "..", "recursos")
DB_PATH = os.path.join(BASE_DIR, "..", "base_datos", "asistencia_frensa.db")
CONFIG_PATH = os.path.join(BASE_DIR, "..", "config.json")

# ⚙️ Cargar configuración institucional
def cargar_configuracion():
    if not os.path.exists(CONFIG_PATH):
        return {}
    with open(CONFIG_PATH, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

# 👥 Obtener empleados registrados
def obtener_empleados():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT cedula, nombre, cargo FROM empleados")
    empleados = cursor.fetchall()
    conn.close()
    return empleados

# 🏛️ Encabezado institucional
def encabezado(canvas, doc, sede, año):
    canvas.saveState()
    canvas.setFont("Helvetica-Bold", 9)
    try:
        canvas.drawImage(os.path.join(RECURSOS_DIR, "logo_frensa.jpg"), 30, 700, 80, 80)
        canvas.drawImage(os.path.join(RECURSOS_DIR, "logo_celita.png"), 480, 700, 100, 100)
    except:
        pass
    texto = [
        "REPÚBLICA BOLIVARIANA DE VENEZUELA",
        "GOBERNACIÓN DEL ESTADO APURE",
        "FUNDACIÓN REGIONAL EL NIÑO SIMÓN APURE",
        "SISTEMA DE ASISTENCIA CELITA 1.0",
        f"SEDE: {sede} - AÑO: {año}"
    ]
    for i, linea in enumerate(texto):
        canvas.drawCentredString(300, 760 - (i * 14), linea)
    canvas.restoreState()

# 🧱 Pie de página institucional
def pie_de_pagina(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    y = 40
    try:
        canvas.drawImage(os.path.join(RECURSOS_DIR, "logo_tec.png"), 60, y - 10, 50, 58)
    except:
        pass
    canvas.drawCentredString(300, y + 18, "DIRECCIÓN DE TECNOLOGÍA E INFORMÁTICA")
    canvas.drawCentredString(300, y + 10, "T.S.U. IVAN ROMERO")
    canvas.drawCentredString(300, y + 2, "(C) Derechos Reservados")
    canvas.drawRightString(550, y + 2, f"Página {doc.page}")
    canvas.restoreState()

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# 📄 Generar PDF de empleados
def generar_pdf_empleados(registros, ruta_pdf):
    config = cargar_configuracion()
    sede = config.get("sede", "Carmen R. de Colmenares").upper()
    año = config.get("año", "2025")
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    estilos = getSampleStyleSheet()
    estilo_titulo = estilos["Title"]
    estilo_normal = estilos["Normal"]

    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter, topMargin=100, bottomMargin=60)
    elementos = []

    elementos.append(Paragraph("REPORTE DE EMPLEADOS REGISTRADOS", estilo_titulo))
    elementos.append(Paragraph(f"Generado el: {fecha_generacion}", estilo_normal))
    elementos.append(Paragraph(f"Sede: {sede}", estilo_normal))
    elementos.append(Spacer(1, 10))

    # 🧾 Datos de empleados
    datos = [["N°", "Cédula", "Nombre", "Cargo"]]
    for i, emp in enumerate(registros, start=1):
        cedula, nombre, cargo = emp
        datos.append([str(i), cedula, nombre, cargo])

    tabla = Table(datos, colWidths=[40, 100, 200, 160])
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#FF9800")),  # 🟧 Naranja institucional
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ]))

    elementos.append(tabla)
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"✔ Total de empleados registrados: {len(registros)}", estilo_normal))
    elementos.append(Spacer(1, 20))

    doc.build(
        elementos,
        onFirstPage=lambda c, d: [encabezado(c, d, sede, año), pie_de_pagina(c, d)],
        onLaterPages=lambda c, d: [encabezado(c, d, sede, año), pie_de_pagina(c, d)]
    )

    ruta_absoluta = os.path.abspath(ruta_pdf)
    webbrowser.open_new(ruta_absoluta)

# 📄 Generar PDF de asistencia
def generar_pdf_reporte(registros=[], filtros=None, ruta_pdf=None):
    if not ruta_pdf:
        return  # Ruta no proporcionada, no se genera nada

    config = cargar_configuracion()
    sede = config.get("sede", "Carmen R. de Colmenares").upper()
    año = config.get("año", "2025")
    fecha_generacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    estilos = getSampleStyleSheet()
    estilo_titulo = estilos["Title"]
    estilo_normal = estilos["Normal"]
    estilo_fecha = estilos["Heading3"]

    # 🔍 Aplicar filtros si se proporcionan
    filtro = None
    valor = None
    if filtros:
        if filtros.get("cedula"):
            filtro = "cedula"
            valor = filtros["cedula"]
        elif filtros.get("desde") and filtros.get("hasta"):
            filtro = "rango"
            valor = (filtros["desde"], filtros["hasta"])
        elif filtros.get("desde"):
            filtro = "fecha"
            valor = filtros["desde"]

    # 🗃️ Obtener registros si no se pasan
    if not registros:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.cedula, h.fecha, h.hora_entrada, h.hora_salida, e.nombre, e.cargo
            FROM horarios h
            LEFT JOIN empleados e ON h.cedula = e.cedula
            ORDER BY h.fecha ASC
        """)
        registros = cursor.fetchall()
        conn.close()

    # 🔍 Aplicar filtros
    if filtro == "cedula":
        registros = [r for r in registros if r[0] == valor]
    elif filtro == "fecha":
        registros = [r for r in registros if r[1] == valor]
    elif filtro == "rango" and isinstance(valor, tuple):
        desde, hasta = valor
        registros = [r for r in registros if desde <= r[1] <= hasta]

    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter, topMargin=100, bottomMargin=60)
    elementos = []

    elementos.append(Paragraph("REPORTE DE ASISTENCIA", estilo_titulo))
    elementos.append(Paragraph(f"Generado el: {fecha_generacion}", estilo_normal))
    if filtro == "rango":
        elementos.append(Paragraph(f"Rango de fechas: {valor[0]} a {valor[1]}", estilo_normal))
    elif filtro == "fecha":
        elementos.append(Paragraph(f"Fecha: {valor}", estilo_normal))
    elif filtro == "cedula":
        elementos.append(Paragraph(f"Cédula: {valor}", estilo_normal))
    elementos.append(Paragraph(f"Sede: {sede}", estilo_normal))
    elementos.append(Spacer(1, 10))

    agrupados = defaultdict(list)
    for r in registros:
        agrupados[r[1]].append(r)

    empleados = obtener_empleados()
    total_asistencias = 0
    total_inasistencias = 0

    for fecha in sorted(agrupados.keys()):
        datos = [["Nombre", "Cargo", "Cédula", "Entrada", "Salida", "Estado"]]
        asistencias_dia = 0
        inasistencias_dia = 0
        cedulas_con_registro = set()

        for r in agrupados[fecha]:
            cedulas_con_registro.add(r[0])
            nombre = r[4] or "—"
            cargo = r[5] or "—"
            entrada = r[2] or "--"
            salida = r[3] or "--"
            estado = "ASISTENTE" if r[2] else "INASISTENTE"
            if estado == "ASISTENTE":
                asistencias_dia += 1
                total_asistencias += 1
            else:
                inasistencias_dia += 1
                total_inasistencias += 1
            datos.append([nombre, cargo, r[0], entrada, salida, estado])

        if filtro != "cedula":
            for cedula, nombre, cargo in empleados:
                if cedula not in cedulas_con_registro:
                    datos.append([nombre, cargo, cedula, "--", "--", "INASISTENTE"])
                    inasistencias_dia += 1
                    total_inasistencias += 1

        tabla = Table(datos, colWidths=[140, 110, 70, 50, 50, 60])
        tabla.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2196F3")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.gray),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ]))

        bloque_dia = [
            Paragraph(f"☒ Fecha: {fecha}", estilo_fecha),
            tabla,
            Spacer(1, 4),
            Paragraph(f"Total de asistencias registradas: {asistencias_dia}", estilo_normal),
            Paragraph(f"Total de inasistencias registradas: {inasistencias_dia}", estilo_normal),
            Spacer(1, 10)
        ]
        elementos.append(KeepTogether(bloque_dia))

    elementos.append(Paragraph(f"✔ Total general de asistencias: {total_asistencias}", estilo_normal))
    elementos.append(Paragraph(f"✘ Total general de inasistencias: {total_inasistencias}", estilo_normal))
    elementos.append(Spacer(1, 20))

    doc.build(
        elementos,
        onFirstPage=lambda c, d: [encabezado(c, d, sede, año), pie_de_pagina(c, d)],
        onLaterPages=lambda c, d: [encabezado(c, d, sede, año), pie_de_pagina(c, d)]
    )

    # 🌐 Abrir el PDF generado automáticamente
    ruta_absoluta = os.path.abspath(ruta_pdf)
    webbrowser.open_new(ruta_absoluta)