import customtkinter as ctk
from tkinter import messagebox
from base_datos.db import conectar
import bcrypt
from interfaz_grafica.estilos import crear_encabezado, crear_pie_de_pagina, COLOR_FONDO

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_cambio_clave(usuario, rol, volver_callback):
    ventana = ctk.CTk()
    ventana.title("Cambio de Clave")
    ventana.geometry("500x500")
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=30)

    ctk.CTkLabel(cuerpo, text="Selecciona el usuario:", font=("Arial", 12)).pack(pady=5)
    combo_usuario = ctk.CTkComboBox(cuerpo, values=["admin", "soporte"], font=("Arial", 12), width=200)
    combo_usuario.pack(pady=5)

    ctk.CTkLabel(cuerpo, text="Nueva clave:", font=("Arial", 12)).pack(pady=5)
    entrada_clave = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=200, show="*")
    entrada_clave.pack(pady=5)

    def cambiar_clave():
        usuario_seleccionado = combo_usuario.get().strip()
        nueva_clave = entrada_clave.get().strip()

        if not usuario_seleccionado:
            messagebox.showwarning("Usuario no seleccionado", "Debes seleccionar un usuario.")
            return

        if not nueva_clave:
            messagebox.showwarning("Campo vacío", "La nueva clave no puede estar vacía.")
            return

        clave_encriptada = bcrypt.hashpw(nueva_clave.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (clave_encriptada, usuario_seleccionado))
            conn.commit()
            conn.close()
            messagebox.showinfo("Clave actualizada", f"La clave de '{usuario_seleccionado}' fue cambiada exitosamente.")
            entrada_clave.delete(0, "end")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cambiar la clave.\n{e}")

    ctk.CTkButton(cuerpo, text="🔑 Cambiar clave", font=("Arial", 12), width=200, height=35,
                  fg_color="#4CAF50", text_color="white", command=cambiar_clave).pack(pady=15)

    ctk.CTkButton(ventana, text="← Volver al menú", font=("Arial", 11), width=180, height=35,
                  fg_color="#3F51B5", text_color="white",
                  command=lambda: [ventana.destroy(), volver_callback()]).pack(pady=10)

    crear_pie_de_pagina(ventana)
    ventana.mainloop()