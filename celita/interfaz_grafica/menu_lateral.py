import os
import customtkinter as ctk
from PIL import Image
from customtkinter import CTkImage
from tkinter import messagebox
from base_datos.db import conectar
from interfaz_grafica.estilos import crear_encabezado, crear_pie_de_pagina, COLOR_FONDO
from interfaz_grafica.interfaz_registro_empleado import mostrar_registro_empleado
from interfaz_grafica.interfaz_marcaje_rapido import mostrar_marcaje_rapido
from interfaz_grafica.interfaz_editar_asistencia import mostrar_edicion_asistencia
from interfaz_grafica.interfaz_reportes import mostrar_reportes
from interfaz_grafica.interfaz_editar_empleados import mostrar_edicion_empleado
from interfaz_grafica.interfaz_cambio_clave import mostrar_cambio_clave
from interfaz_grafica.interfaz_empleados import mostrar_empleados
from configuracion import cargar_configuracion

# 📁 Ruta absoluta al mapa
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAPA_PATH = os.path.join(BASE_DIR, "..", "recursos", "mapa_apure.png")

config = cargar_configuracion()
sede = config.get("sede", "Carmen R. de Colmenares")
institucion = config.get("institucion", "Sistema")
año = config.get("año", "2025")

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_menu_lateral(usuario, rol, volver_a_login):
    ventana = ctk.CTk()
    titulo = f"Menú Principal - {usuario}" if usuario != rol else f"Menú Principal - {rol.capitalize()}"
    ventana.title(titulo)
    centrar_ventana(ventana, 600, 700)
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=10, fill="both", expand=True)

    datos_frame = ctk.CTkFrame(cuerpo, fg_color="transparent")
    datos_frame.pack(pady=10)

    try:
        mapa = Image.open(MAPA_PATH).resize((260, 180))
        mapa_tk = CTkImage(light_image=mapa, size=(260, 180))
        mapa_label = ctk.CTkLabel(datos_frame, image=mapa_tk, text="")
        mapa_label.image = mapa_tk
        mapa_label.grid(row=0, column=0, rowspan=4, padx=(0, 0), sticky="wens")
    except:
        ctk.CTkLabel(datos_frame, text="[Mapa de Apure]", font=("Segoe UI", 12)).grid(row=0, column=0, rowspan=4, padx=10)

    datos_frame.grid_columnconfigure(0, weight=1)
    datos_frame.grid_columnconfigure(1, weight=1)

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM empleados")
    total_empleados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT fecha) FROM horarios")
    dias_laborados = cursor.fetchone()[0]
    conn.close()

    ctk.CTkLabel(datos_frame, text=f"📍 Sede: {sede}", font=("Segoe UI", 12), text_color="#555").grid(row=0, column=1, sticky="w", padx=(60, 10), pady=2)
    ctk.CTkLabel(datos_frame, text=f"👥 Empleados registrados: {total_empleados}", font=("Segoe UI", 12), text_color="#333").grid(row=1, column=1, sticky="w", padx=(60, 10), pady=2)
    ctk.CTkLabel(datos_frame, text=f"📅 Días laborados: {dias_laborados}", font=("Segoe UI", 12), text_color="#333").grid(row=2, column=1, sticky="w", padx=(60, 10), pady=2)
    ctk.CTkLabel(datos_frame, text=f"🏫 Institución: {institucion}", font=("Segoe UI", 12), text_color="#555").grid(row=3, column=1, sticky="w", padx=(60, 10), pady=2)

    botones = [
        ("👤 Registrar empleado", lambda: mostrar_registro_empleado(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login)))
    ]

    if rol == "admin":
        botones.extend([
            ("📊 Generar reportes", lambda: mostrar_reportes(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("✏️ Editar empleado", lambda: mostrar_edicion_empleado(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("🕘 Marcaje rápido", lambda: mostrar_marcaje_rapido(lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("👥 Ver empleados registrados", lambda: mostrar_empleados(usuario, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login)))  # ✅ corregido
        ])
    elif rol == "soporte":
        botones.extend([
            ("✏️ Editar asistencia", lambda: mostrar_edicion_asistencia(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("📊 Generar reportes", lambda: mostrar_reportes(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("✏️ Editar empleado", lambda: mostrar_edicion_empleado(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("🔑 Cambiar clave de usuario", lambda: mostrar_cambio_clave(usuario, rol, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login))),
            ("👥 Ver empleados registrados", lambda: mostrar_empleados(usuario, lambda: mostrar_menu_lateral(usuario, rol, volver_a_login)))  # ✅ corregido
        ])

    boton_frame = ctk.CTkFrame(cuerpo, fg_color="transparent")
    boton_frame.pack(pady=10)

    for i, (texto, accion) in enumerate(botones):
        fila = i // 2
        columna = i % 2
        btn = ctk.CTkButton(
            boton_frame,
            text=texto,
            font=("Segoe UI", 12),
            width=240,
            height=40,
            fg_color="#3F51B5",
            hover_color="#5C6BC0",
            text_color="white",
            corner_radius=10,
            command=lambda a=accion: ventana.after(100, lambda: [ventana.destroy(), a()])
        )
        btn.grid(row=fila, column=columna, padx=10, pady=10)

    botonera = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    botonera.pack(pady=(20, 5))

    ctk.CTkButton(
        botonera,
        text="🔄 Cambiar de usuario",
        font=("Segoe UI", 11),
        width=180,
        height=35,
        fg_color="#2196F3",
        hover_color="#42A5F5",
        text_color="white",
        command=lambda: ventana.after(100, lambda: [ventana.destroy(), volver_a_login()])
    ).grid(row=0, column=0, padx=10)

    ctk.CTkButton(
        botonera,
        text="❌ Salir del sistema",
        font=("Segoe UI", 11),
        width=180,
        height=35,
        fg_color="#f44336",
        hover_color="#e57373",
        text_color="white",
        command=ventana.destroy
    ).grid(row=0, column=1, padx=10)

    crear_pie_de_pagina(ventana, usuario)
    ventana.mainloop()