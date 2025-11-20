import bcrypt
import sqlite3
import os

# 🔐 Nuevas claves en texto plano
claves = {
    "admin": "admin123",
    "soporte": "soporte123"
}

# 📁 Ruta absoluta a la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ruta_base = os.path.join(BASE_DIR, "base_datos", "asistencia_frensa.db")

def conectar():
    return sqlite3.connect(ruta_base)

def actualizar_claves():
    try:
        conn = conectar()
        cursor = conn.cursor()

        for usuario, clave_plana in claves.items():
            hash = bcrypt.hashpw(clave_plana.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            cursor.execute("UPDATE usuarios SET clave = ? WHERE usuario = ?", (hash, usuario))
            print(f"✅ Clave actualizada para '{usuario}'")

        conn.commit()
        conn.close()
        print("🎉 Todas las claves fueron actualizadas correctamente.")
    except Exception as e:
        print(f"❌ Error al actualizar claves: {e}")

# ▶️ Ejecutar
if __name__ == "__main__":
    actualizar_claves()