import customtkinter as ctk
from tkinter import messagebox
from modulos.asistencia import editar_asistencia
from interfaz_grafica.estilos import crear_encabezado, crear_pie_de_pagina, COLOR_FONDO
import re

def mostrar_edicion_asistencia(usuario, rol, volver_callback):
    ventana = ctk.CTk()
    ventana.title("Editar Asistencia")
    ventana.geometry("700x520")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=20)

    # Campos de edición
    ctk.CTkLabel(cuerpo, text="Cédula:", font=("Arial", 12), text_color="#333").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entrada_cedula = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=180)
    entrada_cedula.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(cuerpo, text="Fecha (YYYY-MM-DD):", font=("Arial", 12), text_color="#333").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entrada_fecha = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=180)
    entrada_fecha.grid(row=1, column=1, pady=5)

    ctk.CTkLabel(cuerpo, text="Nueva hora de entrada (HH:MM):", font=("Arial", 12), text_color="#333").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entrada_nueva_entrada = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=180)
    entrada_nueva_entrada.grid(row=2, column=1, pady=5)

    ctk.CTkLabel(cuerpo, text="Nueva hora de salida (HH:MM):", font=("Arial", 12), text_color="#333").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    entrada_nueva_salida = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=180)
    entrada_nueva_salida.grid(row=3, column=1, pady=5)

    def aplicar_edicion():
        cedula = entrada_cedula.get().strip()
        fecha = entrada_fecha.get().strip()
        nueva_entrada = entrada_nueva_entrada.get().strip()
        nueva_salida = entrada_nueva_salida.get().strip()

        if not cedula or not fecha:
            messagebox.showwarning("Campos vacíos", "Debes ingresar cédula y fecha.")
            return

        if not cedula.isdigit():
            messagebox.showerror("Cédula inválida", "La cédula debe contener solo números.")
            return

        if not re.match(r"^\d{4}-\d{2}-\d{2}$", fecha):
            messagebox.showerror("Fecha inválida", "La fecha debe tener el formato YYYY-MM-DD.")
            return

        if nueva_entrada and not re.match(r"^\d{2}:\d{2}$", nueva_entrada):
            messagebox.showerror("Hora inválida", "La hora de entrada debe tener el formato HH:MM.")
            return

        if nueva_salida and not re.match(r"^\d{2}:\d{2}$", nueva_salida):
            messagebox.showerror("Hora inválida", "La hora de salida debe tener el formato HH:MM.")
            return

        try:
            resultado = editar_asistencia(cedula, fecha, nueva_entrada, nueva_salida)
            if resultado:
                messagebox.showinfo("Éxito", "✅ Asistencia actualizada correctamente.")
            else:
                messagebox.showerror("Error", "❌ No se encontró el registro para editar.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    ctk.CTkButton(cuerpo, text="Aplicar cambios", font=("Arial", 12), width=180, height=35,
                  fg_color="#4CAF50", text_color="white", command=aplicar_edicion).grid(row=4, column=0, columnspan=2, pady=15)

    ctk.CTkButton(ventana, text="← Volver al menú", font=("Arial", 11), width=180, height=35,
                  fg_color="#3F51B5", text_color="white",
                  command=lambda: [ventana.destroy(), volver_callback()]).pack(pady=10)

    crear_pie_de_pagina(ventana)
    ventana.mainloop()