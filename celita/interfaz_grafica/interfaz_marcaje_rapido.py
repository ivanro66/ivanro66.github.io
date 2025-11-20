import customtkinter as ctk
from tkinter import messagebox
from base_datos.db import conectar
from datetime import datetime

def registrar_marcaje(cedula, tipo):
    conn = conectar()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    if tipo == "entrada":
        cursor.execute("""
            INSERT OR IGNORE INTO horarios (cedula, fecha, hora_entrada)
            VALUES (?, ?, ?)
        """, (cedula, fecha, hora))
        cursor.execute("""
            UPDATE horarios SET hora_entrada = ?
            WHERE cedula = ? AND fecha = ?
        """, (hora, cedula, fecha))

    elif tipo == "salida":
        cursor.execute("SELECT hora_salida FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
        resultado = cursor.fetchone()

        if resultado:
            if resultado[0]:  # Ya hay salida registrada
                conn.close()
                return "ya_registrada", hora
            else:
                cursor.execute("""
                    UPDATE horarios SET hora_salida = ?
                    WHERE cedula = ? AND fecha = ?
                """, (hora, cedula, fecha))
        else:
            # No existe registro: insertamos con entrada vacía
            cursor.execute("""
                INSERT INTO horarios (cedula, fecha, hora_entrada, hora_salida)
                VALUES (?, ?, ?, ?)
            """, (cedula, fecha, None, hora))

    conn.commit()
    conn.close()
    return "ok", hora

def mostrar_marcaje_rapido(volver_callback):
    ventana = ctk.CTk()
    ventana.title("Marcaje Rápido")
    ventana.geometry("400x300")
    ventana.resizable(False, False)

    ctk.CTkLabel(ventana, text="🕘 Marcaje Rápido", font=("Arial", 16, "bold")).pack(pady=10)

    entrada_frame = ctk.CTkFrame(ventana)
    entrada_frame.pack(pady=10)

    ctk.CTkLabel(entrada_frame, text="Cédula:", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
    cedula_entry = ctk.CTkEntry(entrada_frame, width=200)
    cedula_entry.grid(row=0, column=1, padx=5, pady=5)

    def marcar(tipo):
        cedula = cedula_entry.get().strip()
        if not cedula.isdigit():
            messagebox.showerror("Error", "La cédula debe contener solo números.")
            cedula_entry.delete(0, "end")
            return

        conn = conectar()
        cursor = conn.cursor()

        cursor.execute("SELECT nombre FROM empleados WHERE cedula = ?", (cedula,))
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            messagebox.showerror("Error", "Cédula no registrada.")
            cedula_entry.delete(0, "end")
            return

        nombre = resultado[0]
        fecha = datetime.now().strftime("%Y-%m-%d")

        if tipo == "entrada":
            cursor.execute("SELECT hora_entrada FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
            if cursor.fetchone():
                conn.close()
                messagebox.showwarning("Ya registrada", f"La entrada ya fue registrada para {nombre} hoy.")
                cedula_entry.delete(0, "end")
                return

        elif tipo == "salida":
            cursor.execute("SELECT hora_salida FROM horarios WHERE cedula = ? AND fecha = ?", (cedula, fecha))
            resultado = cursor.fetchone()
            if resultado and resultado[0]:
                conn.close()
                messagebox.showwarning("Ya registrada", f"La salida ya fue registrada para {nombre} hoy.")
                cedula_entry.delete(0, "end")
                return

        conn.close()
        estado, hora = registrar_marcaje(cedula, tipo)

        if estado == "ya_registrada":
            messagebox.showwarning("Ya registrada", f"La salida ya fue registrada para {nombre} hoy.")
        else:
            messagebox.showinfo("Marcaje exitoso", f"{tipo.capitalize()} registrada para {nombre} a las {hora}")

        cedula_entry.delete(0, "end")

    botones_frame = ctk.CTkFrame(ventana)
    botones_frame.pack(pady=10)

    ctk.CTkButton(
        botones_frame,
        text="🟢 Registrar Entrada",
        font=("Arial", 11),
        width=160,
        height=35,
        fg_color="#4CAF50",
        text_color="white",
        command=lambda: marcar("entrada")
    ).grid(row=0, column=0, padx=10, pady=5)

    ctk.CTkButton(
        botones_frame,
        text="🔴 Registrar Salida",
        font=("Arial", 11),
        width=160,
        height=35,
        fg_color="#F44336",
        text_color="white",
        command=lambda: marcar("salida")
    ).grid(row=0, column=1, padx=10, pady=5)

    ctk.CTkButton(
        ventana,
        text="← Volver al menú",
        font=("Arial", 11),
        width=180,
        height=35,
        fg_color="#3F51B5",
        text_color="white",
        command=lambda: [ventana.destroy(), volver_callback()]
    ).pack(pady=20)

    ventana.mainloop()