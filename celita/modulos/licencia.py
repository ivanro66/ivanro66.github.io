from base_datos.db import conectar
from datetime import datetime, timedelta

def licencia_valida():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT fecha_expiracion, estado FROM licencia WHERE estado = 'activa' ORDER BY id DESC LIMIT 1")
    resultado = cursor.fetchone()
    conn.close()

    if not resultado:
        return False

    fecha_expiracion, estado = resultado
    hoy = datetime.now().strftime("%Y-%m-%d")
    return estado == "activa" and hoy <= fecha_expiracion

def activar_licencia(codigo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT tipo, estado FROM licencia WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return "❌ Código inválido."

    tipo, estado_actual = resultado

    if estado_actual != "disponible":
        conn.close()
        return f"⚠️ Esta licencia ya fue usada o está revocada ({estado_actual})."

    fecha_activacion = datetime.now().strftime("%Y-%m-%d")
    if tipo == "temporal":
        fecha_expiracion = (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    else:
        fecha_expiracion = "2099-12-31"

    cursor.execute("""
        UPDATE licencia
        SET fecha_activacion = ?, fecha_expiracion = ?, estado = 'activa'
        WHERE codigo = ?
    """, (fecha_activacion, fecha_expiracion, codigo))

    conn.commit()
    conn.close()
    return f"✅ Licencia activada correctamente. Expira el {fecha_expiracion}."

def revocar_licencia(codigo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT estado FROM licencia WHERE codigo = ?", (codigo,))
    resultado = cursor.fetchone()

    if not resultado:
        conn.close()
        return "❌ Código no encontrado."

    cursor.execute("UPDATE licencia SET estado = 'revocada' WHERE codigo = ?", (codigo,))
    conn.commit()
    conn.close()
    return "🔒 Licencia revocada correctamente."