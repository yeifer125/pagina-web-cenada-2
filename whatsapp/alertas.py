from precios import obtener_precios
from whatsapp import enviar_whatsapp

PRODUCTO = "camote"
LIMITE = 700

def revisar_alertas():
    datos = obtener_precios()

    for item in datos:
        if item.get("producto", "").lower() == PRODUCTO:
            promedio = float(item.get("promedio", 0))

            if promedio <= LIMITE:
                mensaje = f"""
🔔 ALERTA DE PRECIOS

Producto: {item['producto']}
Precio promedio: ₡{promedio}
Fecha: {item['fecha']}

⚠️ Bajó del límite establecido
"""
                enviar_whatsapp(mensaje)
                return "Alerta enviada"

    return "Sin alertas"
