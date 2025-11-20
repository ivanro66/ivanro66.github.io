import os
import customtkinter as ctk
from PIL import Image, ImageTk

# 📁 Ruta absoluta al logo institucional
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_CELITA = os.path.join(BASE_DIR, "..", "recursos", "logo_celita.png")

def crear_pie_institucional(ventana, usuario=""):
    pie = ctk.CTkFrame(ventana, fg_color="transparent")
    pie.pack(side="bottom", pady=(10, 5), fill="x")

    # 🖼️ Contenedor del logo
    logo_frame = ctk.CTkFrame(pie, fg_color="transparent")
    logo_frame.pack()

    # 🧩 Función para actualizar el logo
    def actualizar_logo(ancho):
        for widget in logo_frame.winfo_children():
            widget.destroy()
        try:
            logo = Image.open(LOGO_CELITA)
            proporcion = logo.height / logo.width
            alto = int(ancho * proporcion)
            logo = logo.resize((int(ancho), alto))
            logo_tk = ImageTk.PhotoImage(logo)
            logo_label = ctk.CTkLabel(logo_frame, image=logo_tk, text="")
            logo_label.image = logo_tk
            logo_label.pack()
        except:
            ctk.CTkLabel(logo_frame, text="[Logo CELITA]", font=("Segoe UI", 12)).pack()

    # 🎚️ Slider para controlar el ancho del logo
    slider = ctk.CTkSlider(
        pie,
        from_=80,
        to=200,
        number_of_steps=12,
        command=actualizar_logo
    )
    slider.set(140)  # valor inicial
    slider.pack(pady=(5, 2))

    # 🔴 Texto institucional
    ctk.CTkLabel(
        pie,
        text="CELITA 1.0 - Sistema de asistencia",
        font=("Segoe UI", 11),
        text_color="#D32F2F"
    ).pack()

    # 👤 Usuario activo
    ctk.CTkLabel(
        pie,
        text=f"Usuario: {usuario}",
        font=("Segoe UI", 11),
        text_color="#555"
    ).pack()

    # 🧩 Inicializa el logo
    actualizar_logo(slider.get())