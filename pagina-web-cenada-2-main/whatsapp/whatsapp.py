import requests

PHONE_NUMBER_ID = "1781438779236702"
ACCESS_TOKEN = "TU_ACCESS_TOKEN"
MI_NUMERO = "506XXXXXXXX"  # con código país, sin +

def enviar_whatsapp(mensaje):
    url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": MI_NUMERO,
        "type": "text",
        "text": {
            "body": mensaje
        }
    }

    r = requests.post(url, headers=headers, json=payload)
    return r.json()
