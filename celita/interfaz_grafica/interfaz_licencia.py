import tkinter as tk
from tkinter import messagebox
from modulos.licencia import activar_licencia, licencia_valida

def mostrar_activador_licencia():
    if licencia_valida():
        return  # Ya está activa

    ventana = tk.Toplevel()
    ventana.title("Activación de Licencia - CELITA")
    ventana.geometry("400x200")
    ventana.resizable(False, False)
    ventana.grab_set()
    ventana.focus_force()

    tk.Label(ventana, text="🔐 Ingrese su código de licencia:", font=("Arial", 12)).pack(pady=20)
    entrada_codigo = tk.Entry(ventana, font=("Arial", 12), width=30)
    entrada_codigo.pack()

    def activar():
        codigo = entrada_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Campo vacío", "Por favor ingresa el código de licencia.")
            return

        mensaje = activar_licencia(codigo)
        messagebox.showinfo("Resultado", mensaje)
        if "✅" in mensaje:
            ventana.destroy()

    tk.Button(ventana, text="Activar", font=("Arial", 12), command=activar).pack(pady=20)