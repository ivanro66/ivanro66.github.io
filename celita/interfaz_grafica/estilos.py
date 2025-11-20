import os
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from datetime import datetime

# 🎨 Color de fondo institucional
COLOR_FONDO = "#FFFFFF"  # Blanco puro
COLOR_AREA_DATOS = "#F0F0F0"  # Gris claro institucional

# 📁 Rutas absolutas a los logos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_FRENSA = os.path.join(BASE_DIR, "..", "recursos", "logo_frensa.png")
LOGO_TEC = os.path.join(BASE_DIR, "..", "recursos", "logo_tec.png")

# 🖼️ Encabezado institucional con logos y título
def crear_encabezado(ventana):
    encabezado = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    encabezado.pack(fill="x", pady=10)

    try:
        logo_frensa = CTkImage(light_image=Image.open(LOGO_FRENSA), size=(80, 80))
        logo_tec = CTkImage(light_image=Image.open(LOGO_TEC), size=(80, 80))

        lbl_logo1 = ctk.CTkLabel(encabezado, image=logo_frensa, text="")
        lbl_logo1.pack(side="left", padx=20)

        texto_frame = ctk.CTkFrame(encabezado, fg_color="transparent")
        texto_frame.pack(side="left", expand=True, fill="both")  # ✅ Centrado real

        ctk.CTkLabel(texto_frame, text="Sistema de Asistencia Celita",
                     font=("Segoe UI Semibold", 16), text_color="#003366").pack(anchor="center")

        ctk.CTkLabel(texto_frame, text="Desarrollado para nuestras Casas de los Niños del Estado Apure",
                     font=("Segoe UI", 12), text_color="#555").pack(anchor="center")

        lbl_logo2 = ctk.CTkLabel(encabezado, image=logo_tec, text="")
        lbl_logo2.pack(side="right", padx=20)

    except Exception:
        ctk.CTkLabel(encabezado, text="Sistema de Asistencia Celita",
                     font=("Segoe UI Semibold", 16), text_color="#003366").pack(pady=10)

# 🧾 Pie de página institucional
def crear_pie_de_pagina(ventana, usuario=None):
    pie = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    pie.pack(side="bottom", fill="x", pady=(0, 8))  # ✅ margen inferior más preciso

    año_actual = datetime.now().year
    texto = f"© Celita {año_actual} | Sistema de Asistencia"
    if usuario:
        texto += f" | Usuario: {usuario}"

    etiqueta = ctk.CTkLabel(pie, text=texto,
                            font=("Segoe UI", 10),
                            text_color="#666",
                            fg_color=COLOR_FONDO)
    etiqueta.pack(anchor="center", pady=4)  # ✅ centrado y con espacio vertical