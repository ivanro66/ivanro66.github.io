import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from base_datos.db import conectar  # ✅ Corrección de importación

from interfaz_grafica.estilos import crear_encabezado, crear_pie_de_pagina, COLOR_FONDO

DEPENDENCIAS_VALIDAS = [
    "Casa de los niños", "Presidencia", "Rrhh", "Administración", "Dirección de Tecnología",
    "Coordinación de Cultura", "Coordinación de Insumos y Logística",
    "Coordinación de Salud", "Coordinación de Deporte", "Asesoría Legal",
    "Defensoría del N.N.A.", "Coordinación de Atención Integral",
    "Coordinación de Mantenimiento", "Prensa", "Dirección Técnica",
    "Bienes Nacionales", "Dirección de Planificación y Presupuesto"
]

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_registro_empleado(usuario, rol, volver_callback):
    ventana = ctk.CTk()
    ventana.title("Registro de Empleado")
    centrar_ventana(ventana, 600, 500)
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=20)

    campos = {
        "cedula": "Cédula:",
        "nombre": "Nombre completo:",
        "cargo": "Cargo:"
    }
    entradas = {}

    for i, (key, label) in enumerate(campos.items()):
        ctk.CTkLabel(cuerpo, text=label, font=("Arial", 12), text_color="#333").grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=220)
        entrada.grid(row=i, column=1, pady=5)
        entradas[key] = entrada

    # 🔽 ComboBox para dependencia
    ctk.CTkLabel(cuerpo, text="Dependencia:", font=("Arial", 12), text_color="#333").grid(row=len(campos), column=0, padx=10, pady=5, sticky="e")
    combo_dependencia = ctk.CTkComboBox(cuerpo, values=DEPENDENCIAS_VALIDAS, font=("Arial", 12), width=220)
    combo_dependencia.grid(row=len(campos), column=1, pady=5)

    def registrar():
        cedula = entradas["cedula"].get().strip()
        nombre = entradas["nombre"].get().strip()
        cargo = entradas["cargo"].get().strip()
        dependencia = combo_dependencia.get().strip()
        fecha_ingreso = datetime.now().strftime("%Y-%m-%d")

        if not cedula or not nombre or not cargo or not dependencia:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if not cedula.isdigit():
            messagebox.showerror("Cédula inválida", "La cédula debe contener solo números.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM empleados WHERE cedula = ?", (cedula,))
            if cursor.fetchone():
                messagebox.showerror("Duplicado", f"La cédula '{cedula}' ya está registrada.")
                conn.close()
                return

            cursor.execute("""
                INSERT INTO empleados (cedula, nombre, cargo, fecha_ingreso, dependencia)
                VALUES (?, ?, ?, ?, ?)
            """, (cedula, nombre, cargo, fecha_ingreso, dependencia))
            conn.commit()
            conn.close()

            messagebox.showinfo("Registro exitoso", f"Empleado '{nombre}' registrado correctamente.")
            for entrada in entradas.values():
                entrada.delete(0, "end")
            combo_dependencia.set("")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el empleado.\n{e}")

    ctk.CTkButton(
        cuerpo,
        text="Registrar empleado",
        font=("Arial", 12),
        width=200,
        height=35,
        fg_color="#4CAF50",
        text_color="white",
        command=registrar
    ).grid(row=len(campos)+1, column=0, columnspan=2, pady=15)

    ctk.CTkButton(
        ventana,
        text="← Volver al menú",
        font=("Arial", 11),
        width=180,
        height=35,
        fg_color="#3F51B5",
        text_color="white",
        command=lambda: [ventana.destroy(), volver_callback()]
    ).pack(pady=10)

    crear_pie_de_pagina(ventana)
    ventana.mainloop()