import customtkinter as ctk
from tkinter import messagebox
from base_datos.db import conectar
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

def mostrar_edicion_empleado(usuario, rol, volver_callback):
    ventana = ctk.CTk()
    ventana.title("Editar Empleado")
    centrar_ventana(ventana, 600, 520)
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=20)

    ctk.CTkLabel(cuerpo, text="Cédula del empleado:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entrada_cedula = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=220)
    entrada_cedula.grid(row=0, column=1, pady=5)

    campos = {
        "nombre": "Nombre completo:",
        "cargo": "Cargo:"
    }
    entradas = {}

    for i, (key, label) in enumerate(campos.items(), start=1):
        ctk.CTkLabel(cuerpo, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        entrada = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=220)
        entrada.grid(row=i, column=1, pady=5)
        entradas[key] = entrada

    ctk.CTkLabel(cuerpo, text="Dependencia:", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    combo_dependencia = ctk.CTkComboBox(cuerpo, values=DEPENDENCIAS_VALIDAS, font=("Arial", 12), width=220)
    combo_dependencia.grid(row=3, column=1, pady=5)

    def buscar_empleado():
        cedula = entrada_cedula.get().strip()
        if not cedula.isdigit():
            messagebox.showwarning("Cédula inválida", "La cédula debe contener solo números.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cargo, dependencia FROM empleados WHERE cedula = ?", (cedula,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            entradas["nombre"].delete(0, "end")
            entradas["nombre"].insert(0, resultado[0])
            entradas["cargo"].delete(0, "end")
            entradas["cargo"].insert(0, resultado[1])
            combo_dependencia.set(resultado[2])
        else:
            messagebox.showerror("No encontrado", f"No se encontró un empleado con la cédula '{cedula}'.")

    def guardar_cambios():
        cedula = entrada_cedula.get().strip()
        nombre = entradas["nombre"].get().strip()
        cargo = entradas["cargo"].get().strip()
        dependencia = combo_dependencia.get().strip()

        if not cedula or not nombre or not cargo or not dependencia:
            messagebox.showwarning("Campos vacíos", "Todos los campos son obligatorios.")
            return

        if dependencia not in DEPENDENCIAS_VALIDAS:
            messagebox.showerror("Dependencia inválida", "Selecciona una dependencia válida.")
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE empleados
                SET nombre = ?, cargo = ?, dependencia = ?
                WHERE cedula = ?
            """, (nombre, cargo, dependencia, cedula))
            conn.commit()
            conn.close()
            messagebox.showinfo("Modificación exitosa", "Empleado modificado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar el empleado.\n{e}")

    def eliminar_empleado():
        cedula = entrada_cedula.get().strip()
        if not cedula.isdigit():
            messagebox.showwarning("Cédula inválida", "Debes ingresar una cédula válida.")
            return

        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT nombre, cargo, dependencia FROM empleados WHERE cedula = ?", (cedula,))
        resultado = cursor.fetchone()
        conn.close()

        if not resultado:
            messagebox.showerror("No encontrado", f"No se encontró un empleado con la cédula '{cedula}'.")
            return

        nombre, cargo, dependencia = resultado
        mensaje = (
            f"¿Deseas eliminar al siguiente empleado?\n\n"
            f"Cédula: {cedula}\n"
            f"Nombre: {nombre}\n"
            f"Cargo: {cargo}\n"
            f"Dependencia: {dependencia}"
        )
        confirmacion = messagebox.askyesno("Confirmar eliminación", mensaje)
        if not confirmacion:
            return

        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM empleados WHERE cedula = ?", (cedula,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Eliminado", f"Empleado con cédula {cedula} eliminado correctamente.")
            limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el empleado.\n{e}")

    def limpiar_campos():
        entrada_cedula.delete(0, "end")
        for entrada in entradas.values():
            entrada.delete(0, "end")
        combo_dependencia.set("")

    ctk.CTkButton(cuerpo, text="🔍 Buscar", font=("Arial", 12), width=180, height=35,
                  fg_color="#2196F3", text_color="white", command=buscar_empleado).grid(row=4, column=0, pady=15)

    ctk.CTkButton(cuerpo, text="💾 Guardar cambios", font=("Arial", 12), width=180, height=35,
                  fg_color="#4CAF50", text_color="white", command=guardar_cambios).grid(row=4, column=1, pady=15)

    ctk.CTkButton(cuerpo, text="🧹 Limpiar campos", font=("Arial", 12), width=180, height=35,
                  fg_color="#9E9E9E", text_color="white", command=limpiar_campos).grid(row=5, column=0, columnspan=2, pady=5)

    if rol == "admin":
        ctk.CTkButton(cuerpo, text="🗑️ Eliminar empleado", font=("Arial", 12), width=180, height=35,
                      fg_color="#f44336", text_color="white", command=eliminar_empleado).grid(row=6, column=0, columnspan=2, pady=10)

    ctk.CTkButton(ventana, text="← Volver al menú", font=("Arial", 11), width=180, height=35,
                  fg_color="#3F51B5", text_color="white",
                  command=lambda: [ventana.destroy(), volver_callback()]).pack(pady=10)

    crear_pie_de_pagina(ventana)
    ventana.mainloop()