import os
import customtkinter as ctk
from PIL import Image, ImageTk
from tkinter import messagebox
from base_datos.db import conectar
from interfaz_grafica.menu_lateral import mostrar_menu_lateral
import bcrypt

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_CELITA = os.path.join(BASE_DIR, "..", "recursos", "logo_celita.png")
LOGO_FRENSA = os.path.join(BASE_DIR, "..", "recursos", "logo_frensa.png")
LOGO_TEC = os.path.join(BASE_DIR, "..", "recursos", "logo_tec.png")

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_login():
    def iniciar_sesion():
        usuario = entrada_usuario.get().strip().lower()
        clave_ingresada = entrada_clave.get().strip()

        if not usuario or not clave_ingresada:
            messagebox.showwarning("Campos vacíos", "Por favor ingresa usuario y clave.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT clave, rol FROM usuarios WHERE usuario = ?", (usuario,))
            resultado = cursor.fetchone()
            conn.close()

            if resultado and resultado[0]:
                clave_guardada = str(resultado[0]).encode("utf-8")
                rol = resultado[1]

                if bcrypt.checkpw(clave_ingresada.encode("utf-8"), clave_guardada):
                    ventana.destroy()
                    mostrar_menu_lateral(usuario, rol=rol, volver_a_login=mostrar_login)
                    return

            messagebox.showerror("Acceso denegado", "Usuario o clave incorrectos.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo validar el acceso.\n{e}")

    def confirmar_salida():
        if messagebox.askyesno("Confirmar salida", "¿Deseas cerrar el sistema?"):
            ventana.destroy()

    def fade_in(window, steps=20, delay=20):
        for i in range(steps):
            window.attributes("-alpha", i / steps)
            window.update()
            window.after(delay)

    ventana = ctk.CTk()
    ventana.title("Sistema de Asistencia Celita")
    centrar_ventana(ventana, 900, 500)
    ventana.configure(fg_color="white")
    ventana.resizable(False, False)
    ventana.attributes("-alpha", 0.0)

    contenedor = ctk.CTkFrame(ventana, fg_color="white", corner_radius=10)
    contenedor.pack(expand=True, fill="both", padx=20, pady=20)

    # 🔵 Panel izquierdo
    panel_izquierdo = ctk.CTkFrame(contenedor, width=450, fg_color="white")
    panel_izquierdo.pack(side="left", fill="both", expand=True)

    contenido_izquierdo = ctk.CTkFrame(panel_izquierdo, fg_color="transparent")
    contenido_izquierdo.pack(expand=True)

    try:
        logo_celita = Image.open(LOGO_CELITA).resize((250, 250))
        logo_celita_tk = ImageTk.PhotoImage(logo_celita)
        ctk.CTkLabel(contenido_izquierdo, image=logo_celita_tk, text="").pack(pady=(5, 0))
    except:
        ctk.CTkLabel(contenido_izquierdo, text="[Logo Celita]", font=("Segoe UI", 14)).pack(pady=(5, 0))

    ctk.CTkLabel(contenido_izquierdo, text="Bienvenido a Celita",
                 font=("Segoe UI Black", 20), text_color="#003366").pack(pady=(3, 8))

    ctk.CTkLabel(contenido_izquierdo, text=(
        "Este sistema ha sido desarrollado por la Dirección de Tecnología e Informática "
        "de la Fundación Regional El Niño Simón Apure, con el propósito de fortalecer el control "
        "de asistencia en nuestras Casas de los Niños.\n\n"
        "Celita representa un compromiso con la transparencia, la eficiencia y el bienestar infantil."
    ), font=("Segoe UI", 13), text_color="#333", wraplength=400, justify="center").pack(pady=(0, 8))

    ctk.CTkLabel(contenido_izquierdo, text=(
        "Versión 1.0 del sistema\n"
        "Desarrollado por T.S.U. Iván Romero\n"
        "Dirección de Tecnología e Informática\n"
        "Fundación Regional El Niño Simón Apure"
    ), font=("Segoe UI", 12, "italic"), text_color="#555", justify="center").pack(pady=(0, 8))

    ctk.CTkLabel(contenido_izquierdo, text="“Cada niño cuenta. Cada asistencia construye futuro.”",
                 font=("Segoe UI Italic", 12), text_color="#1A237E", justify="center").pack(pady=(5, 0))

    # 🟢 Panel derecho
    panel_derecho = ctk.CTkFrame(contenedor, width=450, fg_color="white")
    panel_derecho.pack(side="right", fill="both", expand=True)

    logos_frame = ctk.CTkFrame(panel_derecho, fg_color="transparent")
    logos_frame.pack(pady=(10, 5))

    try:
        logo_frensa = Image.open(LOGO_FRENSA).resize((140, 140))
        logo_frensa_tk = ImageTk.PhotoImage(logo_frensa)
        ctk.CTkLabel(logos_frame, image=logo_frensa_tk, text="").pack(side="left", padx=20)
    except:
        ctk.CTkLabel(logos_frame, text="[Logo FRENSA]", font=("Segoe UI", 12)).pack(side="left", padx=20)

    try:
        logo_tec = Image.open(LOGO_TEC).resize((150, 150))
        logo_tec_tk = ImageTk.PhotoImage(logo_tec)
        ctk.CTkLabel(logos_frame, image=logo_tec_tk, text="").pack(side="left", padx=20)
    except:
        ctk.CTkLabel(logos_frame, text="[Logo Tecnología]", font=("Segoe UI", 12)).pack(side="left", padx=20)

    ctk.CTkLabel(panel_derecho, text="Sistema de Asistencia Celita",
                 font=("Segoe UI Semibold", 17), text_color="#003366").pack(pady=(5, 5))

    ctk.CTkLabel(panel_derecho, text="Desarrollado para nuestras Casas de los Niños del Estado Apure",
                 font=("Segoe UI", 13), text_color="#444", wraplength=400, justify="center").pack(pady=(0, 10))

    ctk.CTkLabel(panel_derecho, text="👤 Usuario", font=("Segoe UI Semibold", 13), text_color="#222").pack(pady=(10, 0))
    entrada_usuario = ctk.CTkEntry(panel_derecho, width=220, font=("Segoe UI", 12), corner_radius=8)
    entrada_usuario.pack(pady=5)

    ctk.CTkLabel(panel_derecho, text="🔒 Clave", font=("Segoe UI Semibold", 13), text_color="#222").pack(pady=(10, 0))
    entrada_clave = ctk.CTkEntry(panel_derecho, width=220, font=("Segoe UI", 12), show="*", corner_radius=8)
    entrada_clave.pack(pady=5)

    boton_frame = ctk.CTkFrame(panel_derecho, fg_color="transparent")
    boton_frame.pack(pady=20)

    ctk.CTkButton(boton_frame, text="Acceder", font=("Segoe UI", 12), width=100,
                  fg_color="#3F51B5", hover_color="#5C6BC0", text_color="white",
                  command=iniciar_sesion).grid(row=0, column=0, padx=10)

    ctk.CTkButton(boton_frame, text="Salir", font=("Segoe UI", 12), width=100,
                  fg_color="#f44336", hover_color="#e57373", text_color="white",
                  command=confirmar_salida).grid(row=0, column=1, padx=10)

    fade_in(ventana)
    ventana.mainloop()