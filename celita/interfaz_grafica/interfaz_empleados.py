import customtkinter as ctk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename

from modulos.consulta import obtener_empleados_registrados
from modulos.reportes import generar_pdf_empleados
from interfaz_grafica.estilos import crear_encabezado, crear_pie_de_pagina, COLOR_FONDO, COLOR_AREA_DATOS

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_empleados(usuario, volver_callback):
    ventana = ctk.CTk()
    ventana.title("Empleados Registrados")
    centrar_ventana(ventana, 700, 720)
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=10, fill="both", expand=True)

    ctk.CTkLabel(cuerpo, text="Empleados Registrados", font=("Arial", 16, "bold"), text_color="#003366").pack(pady=10)

    tabla_frame = ctk.CTkFrame(cuerpo, fg_color=COLOR_AREA_DATOS)
    tabla_frame.pack(pady=(0, 5))

    scroll_frame = ctk.CTkScrollableFrame(tabla_frame, fg_color=COLOR_AREA_DATOS, width=580, height=390)
    scroll_frame.pack(pady=5)

    for col in range(4):
        scroll_frame.grid_columnconfigure(col, weight=0)

    # Encabezado
    ctk.CTkLabel(scroll_frame, text="N°", width=40, font=("Segoe UI", 11, "bold"), text_color="#222").grid(row=0, column=0, sticky="w", pady=(0, 5))
    ctk.CTkLabel(scroll_frame, text="CÉDULA", width=120, font=("Segoe UI", 11, "bold"), text_color="#222").grid(row=0, column=1, sticky="w", pady=(0, 5))
    ctk.CTkLabel(scroll_frame, text="NOMBRE", width=180, font=("Segoe UI", 11, "bold"), text_color="#222").grid(row=0, column=2, sticky="w", pady=(0, 5))
    ctk.CTkLabel(scroll_frame, text="CARGO", width=130, font=("Segoe UI", 11, "bold"), text_color="#222").grid(row=0, column=3, sticky="w", pady=(0, 5))

    total_empleados = 0
    registros_empleados = []

    try:
        registros_empleados = obtener_empleados_registrados()
        total_empleados = len(registros_empleados)

        for i, emp in enumerate(registros_empleados, start=1):
            cedula, nombre, cargo = emp

            ctk.CTkLabel(scroll_frame, text=str(i), width=40, font=("Segoe UI", 11), text_color="#333").grid(row=i, column=0, sticky="w", pady=2)
            ctk.CTkLabel(scroll_frame, text=cedula, width=120, font=("Segoe UI", 11), text_color="#333").grid(row=i, column=1, sticky="w", pady=2)
            ctk.CTkLabel(scroll_frame, text=nombre, width=180, font=("Segoe UI", 11), text_color="#333").grid(row=i, column=2, sticky="w", pady=2)
            ctk.CTkLabel(scroll_frame, text=cargo, width=130, font=("Segoe UI", 11), text_color="#333").grid(row=i, column=3, sticky="w", pady=2)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la lista de empleados.\n{e}")

    ctk.CTkLabel(cuerpo, text=f"Total de empleados registrados: {total_empleados}",
                 font=("Arial", 12), text_color="#444").pack(pady=(5, 0))

    botones = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    botones.pack(pady=(5, 10))

    def exportar_pdf():
        if not registros_empleados:
            messagebox.showwarning("Sin datos", "No hay empleados para exportar.")
            return

        ruta_pdf = asksaveasfilename(
            defaultextension=".pdf",
            initialfile="empleados_registrados",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar reporte como..."
        )
        if not ruta_pdf:
            return

        try:
            generar_pdf_empleados(registros_empleados, ruta_pdf)
            messagebox.showinfo("PDF generado", "El reporte fue exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF.\n{e}")

    ctk.CTkButton(botones, text="🖨️ Generar PDF", font=("Arial", 12), width=180, height=35,
                  fg_color="#FF9800", text_color="white", command=exportar_pdf).pack(side="left", padx=10)

    ctk.CTkButton(botones, text="← Volver al menú", font=("Arial", 12), width=180, height=35,
                  fg_color="#3F51B5", text_color="white", command=lambda: [ventana.destroy(), volver_callback()]).pack(side="left", padx=10)

    crear_pie_de_pagina(ventana, usuario)
    ventana.mainloop()