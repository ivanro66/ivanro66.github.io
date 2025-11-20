import os
import customtkinter as ctk
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
from tkcalendar import DateEntry
from datetime import datetime

from modulos.consulta import obtener_registros_asistencia
from modulos.reportes import generar_pdf_reporte
from interfaz_grafica.estilos import crear_encabezado, crear_pie_de_pagina, COLOR_FONDO

def centrar_ventana(ventana, ancho, alto):
    ventana.update_idletasks()
    x = (ventana.winfo_screenwidth() // 2) - (ancho // 2)
    y = (ventana.winfo_screenheight() // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def mostrar_reportes(usuario, rol, volver_callback):
    ventana = ctk.CTk()
    ventana.title("Reportes y Consulta de Asistencia")
    centrar_ventana(ventana, 700, 720)
    ventana.configure(fg_color=COLOR_FONDO)
    ventana.resizable(False, False)

    crear_encabezado(ventana)

    cuerpo = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    cuerpo.pack(pady=20)

    # 🎯 Filtros
    ctk.CTkLabel(cuerpo, text="Cédula (opcional):", font=("Arial", 12), text_color="#333").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entrada_cedula = ctk.CTkEntry(cuerpo, font=("Arial", 12), width=180)
    entrada_cedula.grid(row=0, column=1, pady=5)

    ctk.CTkLabel(cuerpo, text="Desde:", font=("Arial", 12), text_color="#333").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entrada_desde = DateEntry(cuerpo, width=18, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", maxdate=datetime.today())
    entrada_desde.grid(row=1, column=1, pady=5)

    ctk.CTkLabel(cuerpo, text="Hasta:", font=("Arial", 12), text_color="#333").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entrada_hasta = DateEntry(cuerpo, width=18, background="darkblue", foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd", maxdate=datetime.today())
    entrada_hasta.grid(row=2, column=1, pady=5)

    resultado_texto = ctk.CTkTextbox(ventana, font=("Consolas", 11), width=640, height=250)
    resultado_texto.pack(pady=10)

    registros_filtrados = []

    def generar():
        nonlocal registros_filtrados
        cedula = entrada_cedula.get().strip()
        desde = entrada_desde.get_date().strftime("%Y-%m-%d")
        hasta = entrada_hasta.get_date().strftime("%Y-%m-%d")
        resultado_texto.delete("1.0", "end")

        try:
            registros_filtrados = obtener_registros_asistencia(desde, hasta, cedula if cedula else None)

            if registros_filtrados:
                resultado_texto.insert("end", f"{'Cédula':<15}{'Fecha':<15}{'Entrada':<15}{'Salida':<15}\n")
                resultado_texto.insert("end", "-"*60 + "\n")
                for r in registros_filtrados:
                    entrada = r[2] if r[2] else "--"
                    salida = r[3] if r[3] else "--"
                    resultado_texto.insert("end", f"{r[0]:<15}{r[1]:<15}{entrada:<15}{salida:<15}\n")
                resultado_texto.insert("end", f"\nTotal de registros: {len(registros_filtrados)}")
            else:
                resultado_texto.insert("end", "No se encontraron registros en ese rango.")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def consulta_rapida_hoy():
        cedula = entrada_cedula.get().strip()
        hoy = datetime.today().strftime("%Y-%m-%d")

        if not cedula or not cedula.isdigit():
            messagebox.showwarning("Cédula requerida", "Debes ingresar una cédula válida.")
            return

        resultado_texto.delete("1.0", "end")
        registros = obtener_registros_asistencia(hoy, hoy, cedula)

        if registros:
            entrada = registros[0][2] if registros[0][2] else "--"
            salida = registros[0][3] if registros[0][3] else "--"
            estado = "ASISTENTE" if registros[0][2] else "INASISTENTE"
            resultado_texto.insert("end", f"📅 Asistencia de hoy ({hoy}) para cédula {cedula}:\n")
            resultado_texto.insert("end", f"Entrada: {entrada}\nSalida: {salida}\nEstado: {estado}")
        else:
            resultado_texto.insert("end", f"⚠️ No hay registro de asistencia para hoy ({hoy}) para la cédula {cedula}.")

    def exportar_pdf():
        if resultado_texto.get("1.0", "end").strip() == "":
            messagebox.showwarning("Sin vista previa", "Primero genera el reporte en pantalla para verificar los datos.")
            return

        confirmacion = messagebox.askyesno("Confirmar exportación", "¿Deseas exportar este reporte a PDF?")
        if not confirmacion:
            return

        cedula = entrada_cedula.get().strip()
        desde = entrada_desde.get_date().strftime("%Y-%m-%d")
        hasta = entrada_hasta.get_date().strftime("%Y-%m-%d")

        nombre_sugerido = "reporte"
        if cedula:
            nombre_sugerido += f"_{cedula}"
        elif desde and hasta:
            nombre_sugerido += f"_{desde}_a_{hasta}"
        else:
            nombre_sugerido += f"_{datetime.today().strftime('%Y-%m-%d')}"

        ruta_pdf = asksaveasfilename(
            defaultextension=".pdf",
            initialfile=nombre_sugerido,
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar reporte como..."
        )
        if not ruta_pdf:
            return

        filtros = {
            "cedula": cedula if cedula else None,
            "desde": desde,
            "hasta": hasta
        }

        try:
            generar_pdf_reporte(registros_filtrados, filtros, ruta_pdf)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF.\n{e}")

    botones_accion = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    botones_accion.pack(pady=10)

    ctk.CTkButton(botones_accion, text="📋 Ver en pantalla", font=("Arial", 12), width=180, height=35,
                  fg_color="#4CAF50", text_color="white", command=generar).pack(side="left", padx=10)

    ctk.CTkButton(botones_accion, text="🖨️ Generar PDF", font=("Arial", 12), width=180, height=35,
                  fg_color="#2196F3", text_color="white", command=exportar_pdf).pack(side="left", padx=10)

    ctk.CTkButton(botones_accion, text="📅 Consulta rápida de hoy", font=("Arial", 12), width=180, height=35,
                  fg_color="#FF9800", text_color="white", command=consulta_rapida_hoy).pack(side="left", padx=10)

    boton_volver = ctk.CTkFrame(ventana, fg_color=COLOR_FONDO)
    boton_volver.pack(pady=10)

    ctk.CTkButton(
        boton_volver,
        text="← Volver al menú",
        font=("Arial", 11),
        width=180,
        height=35,
        fg_color="#3F51B5",
        text_color="white",
        command=lambda: [ventana.destroy(), volver_callback()]
    ).pack()

    crear_pie_de_pagina(ventana, usuario)
    ventana.mainloop()